import Foundation

/// Home screen state - featured courses, categories overview.
@MainActor
final class HomeViewModel: ObservableObject {
    @Published var featuredCourses: [Course] = []
    @Published var categories: [Category] = []
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let courseRepository: CourseRepository

    init(courseRepository: CourseRepository) {
        self.courseRepository = courseRepository
    }

    func loadData() async {
        isLoading = true
        errorMessage = nil

        do {
            // Parallel fetch for faster load
            async let featured = courseRepository.getFeaturedCourses()
            async let cats = courseRepository.getCategories()

            featuredCourses = try await featured
            categories = try await cats
        } catch {
            errorMessage = "Failed to load data. Pull to refresh."
        }

        isLoading = false
    }
}
