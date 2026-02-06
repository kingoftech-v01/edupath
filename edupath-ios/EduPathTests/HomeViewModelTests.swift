import XCTest
@testable import EduPath

/// Tests for HomeViewModel.
@MainActor
final class HomeViewModelTests: XCTestCase {

    // MARK: - loadData

    func testLoadData_success_populatesData() async {
        let mockRepo = MockCourseRepository()
        mockRepo.featuredCourses = [makeCourse(id: 1), makeCourse(id: 2)]
        mockRepo.categories = [makeCategory(id: 1)]

        let viewModel = HomeViewModel(courseRepository: mockRepo)
        await viewModel.loadData()

        XCTAssertEqual(viewModel.featuredCourses.count, 2)
        XCTAssertEqual(viewModel.categories.count, 1)
        XCTAssertNil(viewModel.errorMessage)
        XCTAssertFalse(viewModel.isLoading)
    }

    func testLoadData_failure_setsErrorMessage() async {
        let mockRepo = MockCourseRepository()
        mockRepo.shouldFail = true

        let viewModel = HomeViewModel(courseRepository: mockRepo)
        await viewModel.loadData()

        XCTAssertTrue(viewModel.featuredCourses.isEmpty)
        XCTAssertNotNil(viewModel.errorMessage)
    }

    func testLoadData_setsLoadingState() async {
        let mockRepo = MockCourseRepository()
        let viewModel = HomeViewModel(courseRepository: mockRepo)

        XCTAssertFalse(viewModel.isLoading)

        // Can't easily test intermediate loading state without delays
        await viewModel.loadData()

        XCTAssertFalse(viewModel.isLoading)
    }

    // MARK: - Helpers

    private func makeCourse(id: Int) -> Course {
        Course(
            id: id,
            title: "Course \(id)",
            slug: "course-\(id)",
            name: "",
            description: "Description",
            price: 0,
            isFree: true,
            imageURL: nil,
            videoURL: nil,
            lessons: 10,
            students: 100,
            durationHours: 5,
            category: nil,
            instructor: nil,
            isFeatured: true,
            createdAt: nil
        )
    }

    private func makeCategory(id: Int) -> Category {
        Category(
            id: id,
            name: "Category \(id)",
            slug: "category-\(id)",
            icon: "",
            description: "",
            courseCount: 10
        )
    }
}

// MARK: - Mock Repository

private class MockCourseRepository: CourseRepository {
    var courses: [Course] = []
    var featuredCourses: [Course] = []
    var freeCourses: [Course] = []
    var categories: [Category] = []
    var instructors: [Instructor] = []
    var reviews: [Review] = []
    var shouldFail = false

    func getCourses(category: String?, search: String?, isFree: Bool?) async throws -> [Course] {
        if shouldFail { throw TestError.failed }
        return courses
    }

    func getCourse(slug: String) async throws -> Course? {
        if shouldFail { throw TestError.failed }
        return courses.first { $0.slug == slug }
    }

    func getFeaturedCourses() async throws -> [Course] {
        if shouldFail { throw TestError.failed }
        return featuredCourses
    }

    func getFreeCourses() async throws -> [Course] {
        if shouldFail { throw TestError.failed }
        return freeCourses
    }

    func getCategories() async throws -> [Category] {
        if shouldFail { throw TestError.failed }
        return categories
    }

    func getInstructors() async throws -> [Instructor] {
        if shouldFail { throw TestError.failed }
        return instructors
    }

    func getReviews(courseId: Int) async throws -> [Review] {
        if shouldFail { throw TestError.failed }
        return reviews
    }

    func submitReview(courseId: Int, rating: Int, description: String) async throws -> Review {
        throw TestError.failed
    }
}

private enum TestError: Error {
    case failed
}
