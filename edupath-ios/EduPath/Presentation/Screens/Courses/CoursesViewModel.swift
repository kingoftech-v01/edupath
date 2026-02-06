import Foundation

/// Courses list screen state with search and filtering.
@MainActor
final class CoursesViewModel: ObservableObject {
    @Published var courses: [Course] = []
    @Published var categories: [Category] = []
    @Published var selectedCategory: Category?
    @Published var searchQuery = ""
    @Published var showFreeOnly = false
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let courseRepository: CourseRepository

    init(courseRepository: CourseRepository) {
        self.courseRepository = courseRepository
    }

    func loadCourses() async {
        isLoading = true
        errorMessage = nil

        do {
            courses = try await courseRepository.getCourses(
                category: selectedCategory?.slug,
                search: searchQuery.isEmpty ? nil : searchQuery,
                isFree: showFreeOnly ? true : nil
            )
        } catch {
            errorMessage = "Failed to load courses"
        }

        isLoading = false
    }

    func loadCategories() async {
        do {
            categories = try await courseRepository.getCategories()
        } catch {
            // Categories are optional for filtering, don't show error
        }
    }

    func selectCategory(_ category: Category?) {
        selectedCategory = category
        Task { await loadCourses() }
    }

    func search() {
        Task { await loadCourses() }
    }

    func toggleFreeOnly() {
        showFreeOnly.toggle()
        Task { await loadCourses() }
    }
}
