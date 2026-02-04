package com.edupath.data.api

import com.edupath.data.repository.TokenManager
import kotlinx.coroutines.runBlocking
import okhttp3.Interceptor
import okhttp3.Response
import javax.inject.Inject
import javax.inject.Singleton

/**
 * OkHttp interceptor that adds JWT authentication token to requests.
 *
 * This interceptor automatically adds the Bearer token from [TokenManager]
 * to the Authorization header of outgoing requests. It skips authentication
 * for login and token refresh endpoints.
 *
 * Note: TokenManager now uses EncryptedSharedPreferences (synchronous).
 * The suspend call is lightweight (no I/O wait), so the brief coroutine
 * bridge is acceptable here.
 *
 * @property tokenManager Manager for retrieving stored JWT tokens
 */
@Singleton
class AuthInterceptor @Inject constructor(
    private val tokenManager: TokenManager
) : Interceptor {

    /**
     * Intercepts the request chain to add authentication header.
     *
     * Workflow:
     * 1. Skip auth for login/refresh endpoints
     * 2. Retrieve access token from TokenManager
     * 3. Add Bearer token header if available
     * 4. Proceed with the request
     *
     * @param chain The interceptor chain
     * @return The response from proceeding with the (possibly modified) request
     */
    override fun intercept(chain: Interceptor.Chain): Response {
        val originalRequest = chain.request()

        // Skip auth for login and refresh endpoints
        val path = originalRequest.url.encodedPath
        if (path.contains("login") || path.contains("refresh")) {
            return chain.proceed(originalRequest)
        }

        // Get token — EncryptedSharedPreferences read is synchronous and fast,
        // so runBlocking here does not cause ANR. The suspend signature is kept
        // for API consistency with the rest of the coroutine-based codebase.
        val token = runBlocking { tokenManager.getAccessToken() }

        // If no token, proceed without auth header
        if (token.isNullOrBlank()) {
            return chain.proceed(originalRequest)
        }

        // Add auth header
        val authenticatedRequest = originalRequest.newBuilder()
            .header("Authorization", "Bearer $token")
            .build()

        return chain.proceed(authenticatedRequest)
    }
}
