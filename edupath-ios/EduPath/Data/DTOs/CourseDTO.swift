import Foundation

/// API response for course list with pagination.
struct PaginatedResponse<T: Decodable>: Decodable {
    let count: Int
    let next: URL?
    let previous: URL?
    let results: [T]
}

/// Course data from API.
struct CourseDTO: Decodable {
    let id: Int
    let title: String
    let slug: String
    let name: String?
    let desc: String
    let price: String
    let isFree: Bool
    let img: String?
    let videoUrl: String?
    let lessons: Int
    let students: Int
    let durationHours: Int
    let category: CategoryDTO?
    let instructor: InstructorDTO?
    let isFeatured: Bool
    let isActive: Bool
    let createdAt: Date?

    func toDomain() -> Course {
        Course(
            id: id,
            title: title,
            slug: slug,
            name: name ?? "",
            description: desc,
            price: Decimal(string: price) ?? 0,
            isFree: isFree,
            imageURL: img.flatMap { URL(string: $0) },
            videoURL: videoUrl.flatMap { URL(string: $0) },
            lessons: lessons,
            students: students,
            durationHours: durationHours,
            category: category?.toDomain(),
            instructor: instructor?.toDomain(),
            isFeatured: isFeatured,
            createdAt: createdAt
        )
    }
}

/// Category data from API.
struct CategoryDTO: Decodable {
    let id: Int
    let name: String
    let slug: String
    let icon: String?
    let description: String?
    let courseCount: Int

    func toDomain() -> Category {
        Category(
            id: id,
            name: name,
            slug: slug,
            icon: icon ?? "",
            description: description ?? "",
            courseCount: courseCount
        )
    }
}

/// Instructor data from API.
struct InstructorDTO: Decodable {
    let id: Int
    let name: String
    let slug: String
    let title: String?
    let bio: String?
    let img: String?
    let facebookUrl: String?
    let instagramUrl: String?
    let linkedinUrl: String?
    let twitterUrl: String?

    func toDomain() -> Instructor {
        Instructor(
            id: id,
            name: name,
            slug: slug,
            title: title ?? "",
            bio: bio ?? "",
            imageURL: img.flatMap { URL(string: $0) },
            socialLinks: SocialLinks(
                facebook: facebookUrl.flatMap { URL(string: $0) },
                instagram: instagramUrl.flatMap { URL(string: $0) },
                linkedin: linkedinUrl.flatMap { URL(string: $0) },
                twitter: twitterUrl.flatMap { URL(string: $0) }
            )
        )
    }
}

/// Review data from API.
struct ReviewDTO: Decodable {
    let id: Int
    let name: String
    let title: String?
    let desc: String
    let rating: Int
    let img: String?
    let course: Int?
    let user: Int?
    let createdAt: Date?

    func toDomain() -> Review {
        Review(
            id: id,
            name: name,
            title: title ?? "Student",
            description: desc,
            rating: rating,
            imageURL: img.flatMap { URL(string: $0) },
            courseId: course,
            userId: user,
            createdAt: createdAt
        )
    }
}

/// Request body for submitting a review.
struct ReviewCreateRequest: Encodable {
    let course: Int
    let rating: Int
    let desc: String
}
