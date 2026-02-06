import Foundation

/// Authentication operations.
protocol AuthRepository {
    /// Login with credentials. Returns user on success.
    func login(username: String, password: String) async throws -> User

    /// Clear tokens and local session.
    func logout() async

    /// Refresh access token using stored refresh token.
    func refreshToken() async throws -> Bool

    /// Check if user has valid session.
    var isAuthenticated: Bool { get }

    /// Get current user if authenticated.
    func getCurrentUser() async throws -> User?

    /// Get current user's profile.
    func getUserProfile() async throws -> UserProfile?
}

/// Authentication errors.
enum AuthError: LocalizedError {
    case invalidCredentials
    case tokenExpired
    case networkError(Error)
    case serverError(String)

    var errorDescription: String? {
        switch self {
        case .invalidCredentials:
            return "Invalid username or password"
        case .tokenExpired:
            return "Session expired. Please login again."
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .serverError(let message):
            return message
        }
    }
}
