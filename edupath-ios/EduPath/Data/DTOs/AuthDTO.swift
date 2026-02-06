import Foundation

/// Login request body.
struct LoginRequest: Encodable {
    let username: String
    let password: String
}

/// Token refresh request body.
struct RefreshTokenRequest: Encodable {
    let refresh: String
}

/// Authentication response containing JWT tokens.
struct AuthResponse: Decodable {
    let access: String
    let refresh: String?
}

/// User data from API.
struct UserDTO: Decodable {
    let id: Int
    let username: String
    let email: String
    let firstName: String
    let lastName: String
    let isStaff: Bool
    let isSuperuser: Bool
    let dateJoined: Date?

    func toDomain() -> User {
        User(
            id: id,
            username: username,
            email: email,
            firstName: firstName,
            lastName: lastName,
            isStaff: isStaff,
            isSuperuser: isSuperuser,
            dateJoined: dateJoined
        )
    }
}

/// User profile data from API.
struct UserProfileDTO: Decodable {
    let id: Int
    let user: Int
    let avatar: String?
    let bio: String?
    let phone: String?
    let website: String?
    let linkedinUrl: String?
    let twitterUrl: String?
    let githubUrl: String?
    let emailNotifications: Bool

    func toDomain() -> UserProfile {
        UserProfile(
            id: id,
            userId: user,
            avatarURL: avatar.flatMap { URL(string: $0) },
            bio: bio ?? "",
            phone: phone ?? "",
            website: website.flatMap { URL(string: $0) },
            linkedinURL: linkedinUrl.flatMap { URL(string: $0) },
            twitterURL: twitterUrl.flatMap { URL(string: $0) },
            githubURL: githubUrl.flatMap { URL(string: $0) },
            emailNotifications: emailNotifications
        )
    }
}
