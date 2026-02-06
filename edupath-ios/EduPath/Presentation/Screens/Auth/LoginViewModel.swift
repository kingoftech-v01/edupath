import Foundation
import SwiftUI

/// Login screen state and logic.
@MainActor
final class LoginViewModel: ObservableObject {
    @Published var username = ""
    @Published var password = ""
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var isLoggedIn = false

    private let authRepository: AuthRepository

    init(authRepository: AuthRepository) {
        self.authRepository = authRepository
        self.isLoggedIn = authRepository.isAuthenticated
    }

    var canLogin: Bool {
        !username.isEmpty && !password.isEmpty && !isLoading
    }

    func login() async {
        guard canLogin else { return }

        isLoading = true
        errorMessage = nil

        do {
            _ = try await authRepository.login(username: username, password: password)
            isLoggedIn = true
        } catch let error as AuthError {
            errorMessage = error.localizedDescription
        } catch {
            errorMessage = "An unexpected error occurred"
        }

        isLoading = false
    }

    func logout() async {
        await authRepository.logout()
        isLoggedIn = false
        username = ""
        password = ""
    }
}
