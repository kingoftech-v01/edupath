import Foundation

/// Course in the catalog - core business entity.
struct Course: Identifiable, Equatable, Hashable {
    let id: Int
    let title: String
    let slug: String
    let name: String
    let description: String
    let price: Decimal
    let isFree: Bool
    let imageURL: URL?
    let videoURL: URL?
    let lessons: Int
    let students: Int
    let durationHours: Int
    let category: Category?
    let instructor: Instructor?
    let isFeatured: Bool
    let createdAt: Date?

    /// Formatted price for display. Shows "Free" for zero-cost courses
    /// to match marketing language across platforms.
    var formattedPrice: String {
        if isFree || price == 0 {
            return "Free"
        }
        return "$\(price)"
    }
}

/// Course category for filtering and navigation.
struct Category: Identifiable, Equatable, Hashable {
    let id: Int
    let name: String
    let slug: String
    let icon: String
    let description: String
    let courseCount: Int
}

/// Course instructor with profile info.
struct Instructor: Identifiable, Equatable, Hashable {
    let id: Int
    let name: String
    let slug: String
    let title: String
    let bio: String
    let imageURL: URL?
    let socialLinks: SocialLinks
}

/// Social media links for instructors.
struct SocialLinks: Equatable, Hashable {
    let facebook: URL?
    let instagram: URL?
    let linkedin: URL?
    let twitter: URL?
}

/// User review for a course.
struct Review: Identifiable, Equatable {
    let id: Int
    let name: String
    let title: String
    let description: String
    let rating: Int
    let imageURL: URL?
    let courseId: Int?
    let userId: Int?
    let createdAt: Date?
}
