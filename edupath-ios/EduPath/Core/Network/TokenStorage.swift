import Foundation
import Security

/// Secure token storage using Keychain.
/// Keychain persists across app reinstalls, matching user expectations
/// for "remember me" behavior on mobile.
final class TokenStorage {
    private let service = "com.edupath.ios"
    private let accessTokenKey = "access_token"
    private let refreshTokenKey = "refresh_token"

    var accessToken: String? {
        get { read(key: accessTokenKey) }
        set { save(key: accessTokenKey, value: newValue) }
    }

    var refreshToken: String? {
        get { read(key: refreshTokenKey) }
        set { save(key: refreshTokenKey, value: newValue) }
    }

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

    // MARK: - Keychain Operations

    private func save(key: String, value: String?) {
        // Delete existing item first
        let deleteQuery: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key
        ]
        SecItemDelete(deleteQuery as CFDictionary)

        guard let value = value, let data = value.data(using: .utf8) else {
            return
        }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecValueData as String: data,
            // kSecAttrAccessible: Only accessible when device unlocked
            // Balances security with usability for background refresh
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        ]

        SecItemAdd(query as CFDictionary, nil)
    }

    private func read(key: String) -> String? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: key,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess,
              let data = result as? Data,
              let string = String(data: data, encoding: .utf8) else {
            return nil
        }

        return string
    }
}
