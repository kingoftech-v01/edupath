package com.edupath.data.repository

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore by preferencesDataStore(name = "auth_prefs")

/**
 * Manages JWT authentication tokens using DataStore.
 *
 * This class provides secure storage and retrieval of access and refresh
 * tokens for API authentication. Tokens are persisted in an encrypted
 * DataStore and survive app restarts.
 *
 * @property context Application context for DataStore access
 */
@Singleton
class TokenManager @Inject constructor(
    @ApplicationContext private val context: Context
) {
    companion object {
        private val ACCESS_TOKEN_KEY = stringPreferencesKey("access_token")
        private val REFRESH_TOKEN_KEY = stringPreferencesKey("refresh_token")
    }

    /**
     * Saves authentication tokens to secure storage.
     *
     * @param accessToken The JWT access token for API requests
     * @param refreshToken The JWT refresh token (optional)
     */
    suspend fun saveTokens(accessToken: String, refreshToken: String?) {
        context.dataStore.edit { prefs ->
            prefs[ACCESS_TOKEN_KEY] = accessToken
            refreshToken?.let { prefs[REFRESH_TOKEN_KEY] = it }
        }
    }

    /**
     * Retrieves the stored access token.
     *
     * @return The access token or null if not stored
     */
    suspend fun getAccessToken(): String? {
        return context.dataStore.data.map { prefs ->
            prefs[ACCESS_TOKEN_KEY]
        }.first()
    }

    /**
     * Retrieves the stored refresh token.
     *
     * @return The refresh token or null if not stored
     */
    suspend fun getRefreshToken(): String? {
        return context.dataStore.data.map { prefs ->
            prefs[REFRESH_TOKEN_KEY]
        }.first()
    }

    /**
     * Clears all stored tokens (logout).
     */
    suspend fun clearTokens() {
        context.dataStore.edit { prefs ->
            prefs.remove(ACCESS_TOKEN_KEY)
            prefs.remove(REFRESH_TOKEN_KEY)
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
