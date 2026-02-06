import SwiftUI

/// Login screen with username/password form.
struct LoginView: View {
    @ObservedObject var viewModel: LoginViewModel

    var body: some View {
        VStack(spacing: 24) {
            Spacer()

            // Logo
            VStack(spacing: 8) {
                Image(systemName: "book.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.accentColor)

                Text("EduPath")
                    .font(.largeTitle)
                    .fontWeight(.bold)

                Text("Learn anywhere, anytime")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            Spacer()

            // Form
            VStack(spacing: 16) {
                TextField("Username", text: $viewModel.username)
                    .textFieldStyle(.roundedBorder)
                    .textContentType(.username)
                    .autocapitalization(.none)
                    .disabled(viewModel.isLoading)

                SecureField("Password", text: $viewModel.password)
                    .textFieldStyle(.roundedBorder)
                    .textContentType(.password)
                    .disabled(viewModel.isLoading)

                if let error = viewModel.errorMessage {
                    Text(error)
                        .font(.caption)
                        .foregroundColor(.red)
                }

                Button(action: {
                    Task { await viewModel.login() }
                }) {
                    if viewModel.isLoading {
                        ProgressView()
                            .progressViewStyle(.circular)
                            .tint(.white)
                    } else {
                        Text("Sign In")
                            .fontWeight(.semibold)
                    }
                }
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(viewModel.canLogin ? Color.accentColor : Color.gray)
                .foregroundColor(.white)
                .cornerRadius(10)
                .disabled(!viewModel.canLogin)
            }
            .padding(.horizontal, 32)

            Spacer()
        }
        .padding()
    }
}

#Preview {
    // Preview with mock repository
    LoginView(viewModel: LoginViewModel(authRepository: MockAuthRepository()))
}

// Mock for previews
private class MockAuthRepository: AuthRepository {
    var isAuthenticated: Bool { false }
    func login(username: String, password: String) async throws -> User {
        throw AuthError.invalidCredentials
    }
    func logout() async {}
    func refreshToken() async throws -> Bool { false }
    func getCurrentUser() async throws -> User? { nil }
    func getUserProfile() async throws -> UserProfile? { nil }
}
