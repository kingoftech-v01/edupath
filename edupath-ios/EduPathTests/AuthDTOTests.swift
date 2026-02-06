import XCTest
@testable import EduPath

/// Tests for Auth DTOs and their domain mappings.
final class AuthDTOTests: XCTestCase {

    // MARK: - LoginRequest

    func testLoginRequest_encodesToJSON() throws {
        let request = LoginRequest(username: "testuser", password: "secret123")

        let encoder = JSONEncoder()
        let data = try encoder.encode(request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]

        XCTAssertEqual(json?["username"] as? String, "testuser")
        XCTAssertEqual(json?["password"] as? String, "secret123")
    }

    // MARK: - RefreshTokenRequest

    func testRefreshTokenRequest_encodesToJSON() throws {
        let request = RefreshTokenRequest(refresh: "refresh_token_value")

        let encoder = JSONEncoder()
        let data = try encoder.encode(request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]

        XCTAssertEqual(json?["refresh"] as? String, "refresh_token_value")
    }

    // MARK: - AuthResponse

    func testAuthResponse_decodesFromJSON() throws {
        let json = """
        {
            "access": "access_token_123",
            "refresh": "refresh_token_456"
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        let response = try decoder.decode(AuthResponse.self, from: json)

        XCTAssertEqual(response.access, "access_token_123")
        XCTAssertEqual(response.refresh, "refresh_token_456")
    }

    func testAuthResponse_decodesWithNilRefresh() throws {
        let json = """
        {
            "access": "access_token_123"
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        let response = try decoder.decode(AuthResponse.self, from: json)

        XCTAssertEqual(response.access, "access_token_123")
        XCTAssertNil(response.refresh)
    }

    // MARK: - UserDTO

    func testUserDTO_decodesFromJSON() throws {
        let json = """
        {
            "id": 42,
            "username": "johndoe",
            "email": "john@example.com",
            "firstName": "John",
            "lastName": "Doe",
            "isStaff": false,
            "isSuperuser": false
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        let dto = try decoder.decode(UserDTO.self, from: json)

        XCTAssertEqual(dto.id, 42)
        XCTAssertEqual(dto.username, "johndoe")
        XCTAssertEqual(dto.email, "john@example.com")
        XCTAssertEqual(dto.firstName, "John")
        XCTAssertEqual(dto.lastName, "Doe")
        XCTAssertFalse(dto.isStaff)
        XCTAssertFalse(dto.isSuperuser)
    }

    func testUserDTO_toDomain_mapsCorrectly() throws {
        let dto = UserDTO(
            id: 1,
            username: "testuser",
            email: "test@example.com",
            firstName: "Test",
            lastName: "User",
            isStaff: true,
            isSuperuser: false,
            dateJoined: nil
        )

        let user = dto.toDomain()

        XCTAssertEqual(user.id, 1)
        XCTAssertEqual(user.username, "testuser")
        XCTAssertEqual(user.email, "test@example.com")
        XCTAssertEqual(user.firstName, "Test")
        XCTAssertEqual(user.lastName, "User")
        XCTAssertTrue(user.isStaff)
        XCTAssertFalse(user.isSuperuser)
    }

    func testUserDTO_decodesWithDateJoined() throws {
        let json = """
        {
            "id": 1,
            "username": "user",
            "email": "user@example.com",
            "firstName": "First",
            "lastName": "Last",
            "isStaff": false,
            "isSuperuser": false,
            "dateJoined": "2024-01-15T10:30:00Z"
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        let dto = try decoder.decode(UserDTO.self, from: json)

        XCTAssertNotNil(dto.dateJoined)
    }

    // MARK: - UserProfileDTO

    func testUserProfileDTO_decodesFromJSON() throws {
        let json = """
        {
            "id": 1,
            "user": 42,
            "avatar": "https://example.com/avatar.jpg",
            "bio": "Software developer",
            "phone": "+1234567890",
            "website": "https://johndoe.com",
            "linkedinUrl": "https://linkedin.com/in/johndoe",
            "twitterUrl": "https://twitter.com/johndoe",
            "githubUrl": "https://github.com/johndoe",
            "emailNotifications": true
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        let dto = try decoder.decode(UserProfileDTO.self, from: json)

        XCTAssertEqual(dto.id, 1)
        XCTAssertEqual(dto.user, 42)
        XCTAssertEqual(dto.avatar, "https://example.com/avatar.jpg")
        XCTAssertEqual(dto.bio, "Software developer")
        XCTAssertEqual(dto.phone, "+1234567890")
        XCTAssertTrue(dto.emailNotifications)
    }

    func testUserProfileDTO_decodesWithNullOptionals() throws {
        let json = """
        {
            "id": 1,
            "user": 42,
            "avatar": null,
            "bio": null,
            "phone": null,
            "website": null,
            "linkedinUrl": null,
            "twitterUrl": null,
            "githubUrl": null,
            "emailNotifications": false
        }
        """.data(using: .utf8)!

        let decoder = JSONDecoder()
        let dto = try decoder.decode(UserProfileDTO.self, from: json)

        XCTAssertNil(dto.avatar)
        XCTAssertNil(dto.bio)
        XCTAssertNil(dto.phone)
        XCTAssertNil(dto.website)
        XCTAssertFalse(dto.emailNotifications)
    }

    func testUserProfileDTO_toDomain_mapsURLsCorrectly() throws {
        let dto = UserProfileDTO(
            id: 1,
            user: 42,
            avatar: "https://example.com/avatar.jpg",
            bio: "Bio text",
            phone: "123",
            website: "https://example.com",
            linkedinUrl: "https://linkedin.com/in/test",
            twitterUrl: "https://twitter.com/test",
            githubUrl: "https://github.com/test",
            emailNotifications: true
        )

        let profile = dto.toDomain()

        XCTAssertEqual(profile.id, 1)
        XCTAssertEqual(profile.userId, 42)
        XCTAssertEqual(profile.avatarURL?.absoluteString, "https://example.com/avatar.jpg")
        XCTAssertEqual(profile.bio, "Bio text")
        XCTAssertEqual(profile.website?.absoluteString, "https://example.com")
        XCTAssertEqual(profile.linkedinURL?.absoluteString, "https://linkedin.com/in/test")
        XCTAssertTrue(profile.emailNotifications)
    }

    func testUserProfileDTO_toDomain_handlesNilValues() throws {
        let dto = UserProfileDTO(
            id: 1,
            user: 42,
            avatar: nil,
            bio: nil,
            phone: nil,
            website: nil,
            linkedinUrl: nil,
            twitterUrl: nil,
            githubUrl: nil,
            emailNotifications: false
        )

        let profile = dto.toDomain()

        XCTAssertNil(profile.avatarURL)
        XCTAssertEqual(profile.bio, "")  // Defaults to empty string
        XCTAssertEqual(profile.phone, "")
        XCTAssertNil(profile.website)
        XCTAssertNil(profile.linkedinURL)
        XCTAssertNil(profile.twitterURL)
        XCTAssertNil(profile.githubURL)
    }
}
