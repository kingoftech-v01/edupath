import XCTest
@testable import EduPath

/// Tests for LoginViewModel.
@MainActor
final class LoginViewModelTests: XCTestCase {

    // MARK: - canLogin

    func testCanLogin_emptyFields_returnsFalse() {
        let viewModel = makeViewModel()
        XCTAssertFalse(viewModel.canLogin)
    }

    func testCanLogin_usernameOnly_returnsFalse() {
        let viewModel = makeViewModel()
        viewModel.username = "testuser"
        XCTAssertFalse(viewModel.canLogin)
    }

    func testCanLogin_passwordOnly_returnsFalse() {
        let viewModel = makeViewModel()
        viewModel.password = "password"
        XCTAssertFalse(viewModel.canLogin)
    }

    func testCanLogin_bothFields_returnsTrue() {
        let viewModel = makeViewModel()
        viewModel.username = "testuser"
        viewModel.password = "password"
        XCTAssertTrue(viewModel.canLogin)
    }

    func testCanLogin_whileLoading_returnsFalse() {
        let viewModel = makeViewModel()
        viewModel.username = "testuser"
        viewModel.password = "password"
        viewModel.isLoading = true
        XCTAssertFalse(viewModel.canLogin)
    }

    // MARK: - login

    func testLogin_success_setsIsLoggedIn() async {
        let mockRepo = MockAuthRepository()
        mockRepo.loginResult = .success(makeUser())

        let viewModel = makeViewModel(authRepository: mockRepo)
        viewModel.username = "testuser"
        viewModel.password = "password"

        await viewModel.login()

        XCTAssertTrue(viewModel.isLoggedIn)
        XCTAssertNil(viewModel.errorMessage)
    }

    func testLogin_failure_setsErrorMessage() async {
        let mockRepo = MockAuthRepository()
        mockRepo.loginResult = .failure(AuthError.invalidCredentials)

        let viewModel = makeViewModel(authRepository: mockRepo)
        viewModel.username = "testuser"
        viewModel.password = "wrongpassword"

        await viewModel.login()

        XCTAssertFalse(viewModel.isLoggedIn)
        XCTAssertNotNil(viewModel.errorMessage)
    }

    // MARK: - logout

    func testLogout_clearsState() async {
        let mockRepo = MockAuthRepository()
        mockRepo.isAuthenticated = true

        let viewModel = makeViewModel(authRepository: mockRepo)
        viewModel.username = "testuser"
        viewModel.password = "password"
        viewModel.isLoggedIn = true

        await viewModel.logout()

        XCTAssertFalse(viewModel.isLoggedIn)
        XCTAssertTrue(viewModel.username.isEmpty)
        XCTAssertTrue(viewModel.password.isEmpty)
    }

    // MARK: - Helpers

    private func makeViewModel(authRepository: AuthRepository? = nil) -> LoginViewModel {
        LoginViewModel(authRepository: authRepository ?? MockAuthRepository())
    }

    private func makeUser() -> User {
        User(
            id: 1,
            username: "testuser",
            email: "test@example.com",
            firstName: "Test",
            lastName: "User",
            isStaff: false,
            isSuperuser: false,
            dateJoined: nil
        )
    }
}

// MARK: - Mock Repository

private class MockAuthRepository: AuthRepository {
    var isAuthenticated: Bool = false
    var loginResult: Result<User, AuthError> = .failure(.invalidCredentials)
    var currentUser: User?

    func login(username: String, password: String) async throws -> User {
        switch loginResult {
        case .success(let user):
            isAuthenticated = true
            return user
        case .failure(let error):
            throw error
        }
    }

    func logout() async {
        isAuthenticated = false
    }

    func refreshToken() async throws -> Bool {
        return false
    }

    func getCurrentUser() async throws -> User? {
        return currentUser
    }

    func getUserProfile() async throws -> UserProfile? {
        return nil
    }
}
