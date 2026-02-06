import SwiftUI

/// Main app entry point.
@main
struct EduPathApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

/// Root view controller - handles auth state routing.
struct ContentView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        Group {
            if appState.isLoggedIn {
                MainTabView()
                    .environmentObject(appState)
            } else {
                LoginView(viewModel: appState.loginViewModel)
                    .onChange(of: appState.loginViewModel.isLoggedIn) { _, isLoggedIn in
                        appState.isLoggedIn = isLoggedIn
                    }
            }
        }
    }
}

/// Main tab bar for authenticated users.
struct MainTabView: View {
    @EnvironmentObject var appState: AppState
    @State private var selectedCourse: Course?

    var body: some View {
        TabView {
            HomeView(
                viewModel: appState.homeViewModel,
                onCourseSelected: { selectedCourse = $0 },
                onCategorySelected: { _ in /* TODO: Navigate to category */ }
            )
            .tabItem {
                Label("Home", systemImage: "house")
            }

            CoursesListView(
                viewModel: appState.coursesViewModel,
                onCourseSelected: { selectedCourse = $0 }
            )
            .tabItem {
                Label("Courses", systemImage: "book")
            }

            // Placeholder for profile
            Text("Profile")
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
        }
        .sheet(item: $selectedCourse) { course in
            NavigationStack {
                CourseDetailView(course: course)
                    .navigationBarItems(trailing: Button("Done") {
                        selectedCourse = nil
                    })
            }
        }
    }
}
