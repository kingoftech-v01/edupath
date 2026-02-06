import XCTest
@testable import EduPath

/// Tests for Course domain model.
final class CourseTests: XCTestCase {

    // MARK: - formattedPrice

    func testFormattedPrice_whenFree_returnsFree() {
        let course = makeCourse(price: 0, isFree: true)
        XCTAssertEqual(course.formattedPrice, "Free")
    }

    func testFormattedPrice_whenPriceZero_returnsFree() {
        let course = makeCourse(price: 0, isFree: false)
        XCTAssertEqual(course.formattedPrice, "Free")
    }

    func testFormattedPrice_whenPaid_returnsFormattedAmount() {
        let course = makeCourse(price: 99.99, isFree: false)
        XCTAssertEqual(course.formattedPrice, "$99.99")
    }

    // MARK: - Equatable

    func testEquality_sameId_areEqual() {
        let course1 = makeCourse(id: 1, title: "A")
        let course2 = makeCourse(id: 1, title: "B")
        XCTAssertEqual(course1, course2)
    }

    func testEquality_differentId_areNotEqual() {
        let course1 = makeCourse(id: 1)
        let course2 = makeCourse(id: 2)
        XCTAssertNotEqual(course1, course2)
    }

    // MARK: - Helpers

    private func makeCourse(
        id: Int = 1,
        title: String = "Test Course",
        price: Decimal = 0,
        isFree: Bool = true
    ) -> Course {
        Course(
            id: id,
            title: title,
            slug: "test-course",
            name: "",
            description: "Description",
            price: price,
            isFree: isFree,
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
}
