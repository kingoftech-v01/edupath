import Foundation

/// Authenticated user account.
struct User: Identifiable, Equatable {
    let id: Int
    let username: String
    let email: String
    let firstName: String
    let lastName: String
    let isStaff: Bool
    let isSuperuser: Bool
    let dateJoined: Date?

    /// Full display name, falls back to username if name fields empty.
    var fullName: String {
        let name = "\(firstName) \(lastName)".trimmingCharacters(in: .whitespaces)
        return name.isEmpty ? username : name
    }
}

/// Extended user profile with bio and social links.
struct UserProfile: Equatable {
    let id: Int
    let userId: Int
    let avatarURL: URL?
    let bio: String
    let phone: String
    let website: URL?
    let linkedinURL: URL?
    let twitterURL: URL?
    let githubURL: URL?
    let emailNotifications: Bool
}

/// JWT authentication tokens.
struct AuthTokens: Equatable {
    let accessToken: String
    let refreshToken: String?

    /// Access token lifetime is 1 hour per backend config.
    /// Refresh 5 minutes early to avoid mid-request expiration.
    static let refreshBuffer: TimeInterval = 5 * 60
}
