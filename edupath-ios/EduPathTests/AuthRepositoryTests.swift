import XCTest
@testable import EduPath

/// Tests for AuthRepository implementation.
final class AuthRepositoryTests: XCTestCase {

    var tokenStorage: TokenStorage!

    override func setUp() {
        super.setUp()
        tokenStorage = TokenStorage()
        tokenStorage.clearTokens()
    }

    override func tearDown() {
        tokenStorage.clearTokens()
        super.tearDown()
    }

    // MARK: - isAuthenticated

    func testIsAuthenticated_noTokens_returnsFalse() {
        XCTAssertFalse(tokenStorage.hasTokens)
    }

    func testIsAuthenticated_withTokens_returnsTrue() {
        tokenStorage.saveTokens(access: "test_token", refresh: "refresh_token")
        XCTAssertTrue(tokenStorage.hasTokens)
    }

    // MARK: - Token Storage

    func testSaveTokens_storesBothTokens() {
        tokenStorage.saveTokens(access: "access123", refresh: "refresh456")

        XCTAssertEqual(tokenStorage.accessToken, "access123")
        XCTAssertEqual(tokenStorage.refreshToken, "refresh456")
    }

    func testClearTokens_removesAllTokens() {
        tokenStorage.saveTokens(access: "access", refresh: "refresh")
        tokenStorage.clearTokens()

        XCTAssertNil(tokenStorage.accessToken)
        XCTAssertNil(tokenStorage.refreshToken)
    }

    func testSaveTokens_withNilRefresh_storesOnlyAccess() {
        tokenStorage.saveTokens(access: "access", refresh: nil)

        XCTAssertEqual(tokenStorage.accessToken, "access")
        XCTAssertNil(tokenStorage.refreshToken)
    }
}
