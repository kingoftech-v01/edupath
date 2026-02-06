import Foundation

/// Course data access - abstracts network vs cache source.
protocol CourseRepository {
    /// Fetch courses with optional filters.
    func getCourses(
        category: String?,
        search: String?,
        isFree: Bool?
    ) async throws -> [Course]

    /// Fetch single course by slug.
    func getCourse(slug: String) async throws -> Course?

    /// Featured courses for homepage hero section.
    func getFeaturedCourses() async throws -> [Course]

    /// Free courses for promotional display.
    func getFreeCourses() async throws -> [Course]

    /// All course categories.
    func getCategories() async throws -> [Category]

    /// All instructors.
    func getInstructors() async throws -> [Instructor]

    /// Reviews for a specific course.
    func getReviews(courseId: Int) async throws -> [Review]

    /// Submit a new review. Requires authentication.
    func submitReview(courseId: Int, rating: Int, description: String) async throws -> Review
}
