import Foundation

/// Auth repository implementation using API client and secure token storage.
final class AuthRepositoryImpl: AuthRepository {
    private let api: APIClient
    private let tokenStorage: TokenStorage

    init(api: APIClient, tokenStorage: TokenStorage) {
        self.api = api
        self.tokenStorage = tokenStorage
    }

    var isAuthenticated: Bool {
        tokenStorage.hasTokens
    }

    func login(username: String, password: String) async throws -> User {
        let request = LoginRequest(username: username, password: password)

        do {
            let response: AuthResponse = try await api.post(
                "accounts/api/v1/auth/login/",
                body: request
            )

            tokenStorage.saveTokens(access: response.access, refresh: response.refresh)

            // Fetch user data after successful login
            guard let user = try await getCurrentUser() else {
                throw AuthError.serverError("Failed to fetch user data")
            }

            return user
        } catch let error as APIError {
            switch error {
            case .serverError(statusCode: 400, _),
                 .serverError(statusCode: 401, _):
                throw AuthError.invalidCredentials
            default:
                throw AuthError.networkError(error)
            }
        }
    }

    func logout() async {
        tokenStorage.clearTokens()
    }

    func refreshToken() async throws -> Bool {
        guard let refreshToken = tokenStorage.refreshToken else {
            return false
        }

        let request = RefreshTokenRequest(refresh: refreshToken)

        do {
            let response: AuthResponse = try await api.post(
                "accounts/api/v1/auth/token/refresh/",
                body: request
            )

            tokenStorage.saveTokens(access: response.access, refresh: refreshToken)
            return true
        } catch {
            // Refresh failed - token likely expired, clear and require re-login
            tokenStorage.clearTokens()
            return false
        }
    }

    func getCurrentUser() async throws -> User? {
        guard isAuthenticated else { return nil }

        do {
            let dto: UserDTO = try await api.get("accounts/api/v1/me/")
            return dto.toDomain()
        } catch APIError.unauthorized {
            // Try token refresh once
            if try await refreshToken() {
                let dto: UserDTO = try await api.get("accounts/api/v1/me/")
                return dto.toDomain()
            }
            throw AuthError.tokenExpired
        }
    }

    func getUserProfile() async throws -> UserProfile? {
        guard isAuthenticated else { return nil }

        let dto: UserProfileDTO = try await api.get("accounts/api/v1/profiles/me/")
        return dto.toDomain()
    }
}
