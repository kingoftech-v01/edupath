import XCTest
@testable import EduPath

/// Tests for User domain model.
final class UserTests: XCTestCase {

    // MARK: - fullName

    func testFullName_withBothNames_returnsFullName() {
        let user = makeUser(firstName: "John", lastName: "Doe")
        XCTAssertEqual(user.fullName, "John Doe")
    }

    func testFullName_withFirstNameOnly_returnsFirstName() {
        let user = makeUser(firstName: "John", lastName: "")
        XCTAssertEqual(user.fullName, "John")
    }

    func testFullName_withLastNameOnly_returnsLastName() {
        let user = makeUser(firstName: "", lastName: "Doe")
        XCTAssertEqual(user.fullName, "Doe")
    }

    func testFullName_withEmptyNames_returnsUsername() {
        let user = makeUser(username: "johndoe", firstName: "", lastName: "")
        XCTAssertEqual(user.fullName, "johndoe")
    }

    func testFullName_withWhitespaceNames_returnsUsername() {
        let user = makeUser(username: "johndoe", firstName: "  ", lastName: "  ")
        XCTAssertEqual(user.fullName, "johndoe")
    }

    // MARK: - Helpers

    private func makeUser(
        username: String = "testuser",
        firstName: String = "",
        lastName: String = ""
    ) -> User {
        User(
            id: 1,
            username: username,
            email: "test@example.com",
            firstName: firstName,
            lastName: lastName,
            isStaff: false,
            isSuperuser: false,
            dateJoined: nil
        )
    }
}
