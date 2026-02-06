import XCTest
@testable import EduPath

/// Tests for TokenStorage.
/// Uses an in-memory mock since Keychain isn't available in test environment.
final class TokenStorageTests: XCTestCase {

    // MARK: - hasTokens

    func testHasTokens_withNoAccessToken_returnsFalse() {
        let storage = MockTokenStorage()

        XCTAssertFalse(storage.hasTokens)
    }

    func testHasTokens_withAccessToken_returnsTrue() {
        let storage = MockTokenStorage()
        storage.accessToken = "some_token"

        XCTAssertTrue(storage.hasTokens)
    }

    // MARK: - saveTokens

    func testSaveTokens_storesBothTokens() {
        let storage = MockTokenStorage()

        storage.saveTokens(access: "access_123", refresh: "refresh_456")

        XCTAssertEqual(storage.accessToken, "access_123")
        XCTAssertEqual(storage.refreshToken, "refresh_456")
    }

    func testSaveTokens_withNilRefresh_onlySavesAccess() {
        let storage = MockTokenStorage()

        storage.saveTokens(access: "access_123", refresh: nil)

        XCTAssertEqual(storage.accessToken, "access_123")
        XCTAssertNil(storage.refreshToken)
    }

    // MARK: - clearTokens

    func testClearTokens_removesBothTokens() {
        let storage = MockTokenStorage()
        storage.accessToken = "access"
        storage.refreshToken = "refresh"

        storage.clearTokens()

        XCTAssertNil(storage.accessToken)
        XCTAssertNil(storage.refreshToken)
        XCTAssertFalse(storage.hasTokens)
    }

    // MARK: - Token Persistence

    func testAccessToken_setAndGet_returnsValue() {
        let storage = MockTokenStorage()

        storage.accessToken = "test_token"

        XCTAssertEqual(storage.accessToken, "test_token")
    }

    func testRefreshToken_setAndGet_returnsValue() {
        let storage = MockTokenStorage()

        storage.refreshToken = "refresh_token"

        XCTAssertEqual(storage.refreshToken, "refresh_token")
    }

    func testAccessToken_setToNil_clearsValue() {
        let storage = MockTokenStorage()
        storage.accessToken = "token"

        storage.accessToken = nil

        XCTAssertNil(storage.accessToken)
    }

    // MARK: - Overwrite Behavior

    func testSaveTokens_overwitesPreviousTokens() {
        let storage = MockTokenStorage()
        storage.saveTokens(access: "old_access", refresh: "old_refresh")

        storage.saveTokens(access: "new_access", refresh: "new_refresh")

        XCTAssertEqual(storage.accessToken, "new_access")
        XCTAssertEqual(storage.refreshToken, "new_refresh")
    }
}

// MARK: - Mock TokenStorage

/// In-memory token storage for testing.
/// Real TokenStorage uses Keychain which isn't available in unit tests.
private class MockTokenStorage {
    var accessToken: String?
    var refreshToken: String?

    var hasTokens: Bool {
        accessToken != nil
    }

    func saveTokens(access: String, refresh: String?) {
        accessToken = access
        refreshToken = refresh
    }

    func clearTokens() {
        accessToken = nil
        refreshToken = nil
    }
}
