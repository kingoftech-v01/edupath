package com.edupath.data.repository

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKeys
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Manages JWT authentication tokens using EncryptedSharedPreferences.
 *
 * Tokens are stored encrypted at rest using Android Keystore-backed keys,
 * protecting them even on rooted devices or when backups are extracted.
 *
 * @property context Application context for storage access
 */
@Singleton
class TokenManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        private const val PREFS_NAME = "auth_encrypted_prefs"
        private const val ACCESS_TOKEN_KEY = "access_token"
        private const val REFRESH_TOKEN_KEY = "refresh_token"
    }

    private val prefs: SharedPreferences by lazy {
        val masterKeyAlias = MasterKeys.getOrCreate(MasterKeys.AES256_GCM_SPEC)
        EncryptedSharedPreferences.create(
            PREFS_NAME,
            masterKeyAlias,
            context,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    /**
     * Saves authentication tokens to encrypted storage.
     *
     * @param accessToken The JWT access token for API requests
     * @param refreshToken The JWT refresh token (optional)
     */
    suspend fun saveTokens(accessToken: String, refreshToken: String?) {
        prefs.edit().apply {
            putString(ACCESS_TOKEN_KEY, accessToken)
            refreshToken?.let { putString(REFRESH_TOKEN_KEY, it) }
            apply()
        }
    }

    /**
     * Retrieves the stored access token.
     *
     * @return The access token or null if not stored
     */
    suspend fun getAccessToken(): String? {
        return prefs.getString(ACCESS_TOKEN_KEY, null)
    }

    /**
     * Retrieves the stored refresh token.
     *
     * @return The refresh token or null if not stored
     */
    suspend fun getRefreshToken(): String? {
        return prefs.getString(REFRESH_TOKEN_KEY, null)
    }

    /**
     * Clears all stored tokens (logout).
     */
    suspend fun clearTokens() {
        prefs.edit().apply {
            remove(ACCESS_TOKEN_KEY)
            remove(REFRESH_TOKEN_KEY)
            apply()
        }
    }

    /**
     * Checks if the user is logged in.
     *
     * @return true if an access token is stored, false otherwise
     */
    suspend fun isLoggedIn(): Boolean {
        return getAccessToken() != null
    }
}
