import XCTest
@testable import EduPath

/// Tests for DTO to Domain model mapping.
final class CourseDTOTests: XCTestCase {

    // MARK: - CourseDTO.toDomain

    func testCourseDTO_toDomain_mapsAllFields() {
        let dto = makeCourseDTO()
        let course = dto.toDomain()

        XCTAssertEqual(course.id, 1)
        XCTAssertEqual(course.title, "Test Course")
        XCTAssertEqual(course.slug, "test-course")
        XCTAssertEqual(course.description, "Description")
        XCTAssertEqual(course.price, 99.99)
        XCTAssertFalse(course.isFree)
        XCTAssertEqual(course.lessons, 10)
        XCTAssertEqual(course.students, 100)
    }

    func testCourseDTO_toDomain_handlesOptionalFields() {
        let dto = makeCourseDTO(
            name: nil,
            img: nil,
            videoUrl: nil,
            category: nil,
            instructor: nil
        )
        let course = dto.toDomain()

        XCTAssertEqual(course.name, "")
        XCTAssertNil(course.imageURL)
        XCTAssertNil(course.videoURL)
        XCTAssertNil(course.category)
        XCTAssertNil(course.instructor)
    }

    func testCourseDTO_toDomain_parsesValidURLs() {
        let dto = makeCourseDTO(
            img: "https://example.com/image.jpg",
            videoUrl: "https://example.com/video.mp4"
        )
        let course = dto.toDomain()

        XCTAssertEqual(course.imageURL?.absoluteString, "https://example.com/image.jpg")
        XCTAssertEqual(course.videoURL?.absoluteString, "https://example.com/video.mp4")
    }

    // MARK: - CategoryDTO.toDomain

    func testCategoryDTO_toDomain_mapsAllFields() {
        let dto = CategoryDTO(
            id: 1,
            name: "Development",
            slug: "development",
            icon: "code",
            description: "Learn to code",
            courseCount: 50
        )
        let category = dto.toDomain()

        XCTAssertEqual(category.id, 1)
        XCTAssertEqual(category.name, "Development")
        XCTAssertEqual(category.slug, "development")
        XCTAssertEqual(category.icon, "code")
        XCTAssertEqual(category.courseCount, 50)
    }

    // MARK: - InstructorDTO.toDomain

    func testInstructorDTO_toDomain_mapsAllFields() {
        let dto = InstructorDTO(
            id: 1,
            name: "John Doe",
            slug: "john-doe",
            title: "Senior Developer",
            bio: "10 years experience",
            img: "https://example.com/avatar.jpg",
            facebookUrl: nil,
            instagramUrl: nil,
            linkedinUrl: "https://linkedin.com/in/johndoe",
            twitterUrl: nil
        )
        let instructor = dto.toDomain()

        XCTAssertEqual(instructor.id, 1)
        XCTAssertEqual(instructor.name, "John Doe")
        XCTAssertEqual(instructor.title, "Senior Developer")
        XCTAssertNotNil(instructor.imageURL)
        XCTAssertNotNil(instructor.socialLinks.linkedin)
        XCTAssertNil(instructor.socialLinks.twitter)
    }

    // MARK: - Helpers

    private func makeCourseDTO(
        name: String? = "Course Name",
        img: String? = "https://example.com/image.jpg",
        videoUrl: String? = nil,
        category: CategoryDTO? = nil,
        instructor: InstructorDTO? = nil
    ) -> CourseDTO {
        CourseDTO(
            id: 1,
            title: "Test Course",
            slug: "test-course",
            name: name,
            desc: "Description",
            price: "99.99",
            isFree: false,
            img: img,
            videoUrl: videoUrl,
            lessons: 10,
            students: 100,
            durationHours: 5,
            category: category,
            instructor: instructor,
            isFeatured: true,
            isActive: true,
            createdAt: nil
        )
    }
}
