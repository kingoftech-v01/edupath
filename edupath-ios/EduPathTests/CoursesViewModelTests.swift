import XCTest
@testable import EduPath

/// Tests for CoursesViewModel.
@MainActor
final class CoursesViewModelTests: XCTestCase {

    // MARK: - Initial State

    func testInitialState_isEmpty() {
        let viewModel = CoursesViewModel(courseRepository: MockCourseRepository())

        XCTAssertTrue(viewModel.courses.isEmpty)
        XCTAssertTrue(viewModel.categories.isEmpty)
        XCTAssertNil(viewModel.selectedCategory)
        XCTAssertTrue(viewModel.searchQuery.isEmpty)
        XCTAssertFalse(viewModel.showFreeOnly)
        XCTAssertFalse(viewModel.isLoading)
        XCTAssertNil(viewModel.errorMessage)
    }

    // MARK: - loadCourses

    func testLoadCourses_success_populatesCourses() async {
        let mockRepo = MockCourseRepository()
        mockRepo.courses = [makeCourse(id: 1), makeCourse(id: 2), makeCourse(id: 3)]

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        await viewModel.loadCourses()

        XCTAssertEqual(viewModel.courses.count, 3)
        XCTAssertNil(viewModel.errorMessage)
        XCTAssertFalse(viewModel.isLoading)
    }

    func testLoadCourses_failure_setsErrorMessage() async {
        let mockRepo = MockCourseRepository()
        mockRepo.shouldFail = true

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        await viewModel.loadCourses()

        XCTAssertTrue(viewModel.courses.isEmpty)
        XCTAssertNotNil(viewModel.errorMessage)
    }

    func testLoadCourses_withSearchQuery_passesQueryToRepository() async {
        let mockRepo = MockCourseRepository()
        mockRepo.courses = [makeCourse(id: 1)]

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.searchQuery = "swift"
        await viewModel.loadCourses()

        XCTAssertEqual(mockRepo.lastSearchQuery, "swift")
    }

    func testLoadCourses_withEmptySearchQuery_passesNilToRepository() async {
        let mockRepo = MockCourseRepository()

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.searchQuery = ""
        await viewModel.loadCourses()

        XCTAssertNil(mockRepo.lastSearchQuery)
    }

    func testLoadCourses_withSelectedCategory_passesCategoryToRepository() async {
        let mockRepo = MockCourseRepository()
        let category = makeCategory(id: 1)

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.selectedCategory = category
        await viewModel.loadCourses()

        XCTAssertEqual(mockRepo.lastCategorySlug, category.slug)
    }

    func testLoadCourses_withFreeOnlyEnabled_passesTrueToRepository() async {
        let mockRepo = MockCourseRepository()

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.showFreeOnly = true
        await viewModel.loadCourses()

        XCTAssertEqual(mockRepo.lastIsFree, true)
    }

    func testLoadCourses_withFreeOnlyDisabled_passesNilToRepository() async {
        let mockRepo = MockCourseRepository()

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.showFreeOnly = false
        await viewModel.loadCourses()

        XCTAssertNil(mockRepo.lastIsFree)
    }

    // MARK: - loadCategories

    func testLoadCategories_success_populatesCategories() async {
        let mockRepo = MockCourseRepository()
        mockRepo.categories = [makeCategory(id: 1), makeCategory(id: 2)]

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        await viewModel.loadCategories()

        XCTAssertEqual(viewModel.categories.count, 2)
    }

    func testLoadCategories_failure_doesNotSetError() async {
        let mockRepo = MockCourseRepository()
        mockRepo.shouldFail = true

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        await viewModel.loadCategories()

        // Categories failure should be silent - they're optional for filtering
        XCTAssertNil(viewModel.errorMessage)
    }

    // MARK: - selectCategory

    func testSelectCategory_updatesSelectedCategory() async {
        let mockRepo = MockCourseRepository()
        let category = makeCategory(id: 1)

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.selectCategory(category)

        XCTAssertEqual(viewModel.selectedCategory?.id, category.id)
    }

    func testSelectCategory_nil_clearsSelection() async {
        let mockRepo = MockCourseRepository()
        let category = makeCategory(id: 1)

        let viewModel = CoursesViewModel(courseRepository: mockRepo)
        viewModel.selectedCategory = category
        viewModel.selectCategory(nil)

        XCTAssertNil(viewModel.selectedCategory)
    }

    // MARK: - toggleFreeOnly

    func testToggleFreeOnly_togglesValue() {
        let mockRepo = MockCourseRepository()
        let viewModel = CoursesViewModel(courseRepository: mockRepo)

        XCTAssertFalse(viewModel.showFreeOnly)

        viewModel.toggleFreeOnly()
        XCTAssertTrue(viewModel.showFreeOnly)

        viewModel.toggleFreeOnly()
        XCTAssertFalse(viewModel.showFreeOnly)
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
            isFeatured: false,
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

    // Capture parameters for verification
    var lastCategorySlug: String?
    var lastSearchQuery: String?
    var lastIsFree: Bool?

    func getCourses(category: String?, search: String?, isFree: Bool?) async throws -> [Course] {
        lastCategorySlug = category
        lastSearchQuery = search
        lastIsFree = isFree

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
