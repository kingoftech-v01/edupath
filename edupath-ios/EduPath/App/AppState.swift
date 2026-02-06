import Foundation
import SwiftUI

/// App-wide state and dependency container.
/// Central point for service instantiation to simplify DI
/// without requiring a full framework like Swinject.
@MainActor
final class AppState: ObservableObject {
    @Published var isLoggedIn: Bool

    // Services
    private let tokenStorage: TokenStorage
    private let apiClient: APIClient
    private let authRepository: AuthRepository
    private let courseRepository: CourseRepository

    // ViewModels - lazy initialized to avoid circular deps
    lazy var loginViewModel: LoginViewModel = {
        LoginViewModel(authRepository: authRepository)
    }()

    lazy var homeViewModel: HomeViewModel = {
        HomeViewModel(courseRepository: courseRepository)
    }()

    lazy var coursesViewModel: CoursesViewModel = {
        CoursesViewModel(courseRepository: courseRepository)
    }()

    init() {
        // Initialize services
        tokenStorage = TokenStorage()

        // API base URL - would come from config in production
        let baseURL = URL(string: "http://localhost:8000")!
        apiClient = APIClient(baseURL: baseURL, tokenStorage: tokenStorage)

        authRepository = AuthRepositoryImpl(api: apiClient, tokenStorage: tokenStorage)
        courseRepository = CourseRepositoryImpl(api: apiClient)

        // Check initial auth state
        isLoggedIn = tokenStorage.hasTokens
    }
}

/// Configuration for different environments.
enum AppConfig {
    case development
    case staging
    case production

    var apiBaseURL: URL {
        switch self {
        case .development:
            return URL(string: "http://localhost:8000")!
        case .staging:
            return URL(string: "https://staging-api.edupath.com")!
        case .production:
            return URL(string: "https://api.edupath.com")!
        }
    }
}
