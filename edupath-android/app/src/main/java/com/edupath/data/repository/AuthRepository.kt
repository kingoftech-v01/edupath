package com.edupath.data.repository

import com.edupath.data.api.EduPathApi
import com.edupath.data.api.dto.LoginRequest
import com.edupath.domain.model.User
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Sealed class representing authentication operation results.
 *
 * @param T The type of data on success
 */
sealed class AuthResult<out T> {
    /**
     * Successful authentication with data.
     *
     * @property data The resulting data from the operation
     */
    data class Success<T>(val data: T) : AuthResult<T>()

    /**
     * Authentication error with message.
     *
     * @property message Human-readable error description
     */
    data class Error(val message: String) : AuthResult<Nothing>()

    /**
     * Loading state for async operations.
     */
    object Loading : AuthResult<Nothing>()
}

/**
 * Repository interface for authentication operations.
 *
 * Provides methods for user authentication, session management,
 * and token refresh.
 */
interface AuthRepository {
    /**
     * Authenticates a user with credentials.
     *
     * @param username User's username or email
     * @param password User's password
     * @return AuthResult containing User on success, error message on failure
     */
    suspend fun login(username: String, password: String): AuthResult<User>

    /**
     * Logs out the current user and clears tokens.
     */
    suspend fun logout()

    /**
     * Refreshes the access token using the refresh token.
     *
     * @return true if refresh succeeded, false otherwise
     */
    suspend fun refreshToken(): Boolean

    /**
     * Checks if a user is currently logged in.
     *
     * @return true if logged in, false otherwise
     */
    suspend fun isLoggedIn(): Boolean

    /**
     * Gets the currently authenticated user's information.
     *
     * @return User object or null if not authenticated
     */
    suspend fun getCurrentUser(): User?
}

/**
 * Implementation of [AuthRepository] using Retrofit and TokenManager.
 *
 * Handles authentication with the backend API and manages JWT tokens
 * using [TokenManager] for secure storage.
 *
 * @property api EduPath API interface
 * @property tokenManager Token storage manager
 */
@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val api: EduPathApi,
    private val tokenManager: TokenManager
) : AuthRepository {

    /**
     * Authenticates user and stores tokens on success.
     *
     * Workflow:
     * 1. Send login request to API
     * 2. Store returned tokens in TokenManager
     * 3. Fetch and return user data
     */
    override suspend fun login(username: String, password: String): AuthResult<User> {
        return try {
            val response = api.login(LoginRequest(username, password))
            if (response.isSuccessful && response.body() != null) {
                val authResponse = response.body()!!
                tokenManager.saveTokens(authResponse.access, authResponse.refresh)

                // Fetch user data
                val userResponse = api.getCurrentUser()
                if (userResponse.isSuccessful && userResponse.body() != null) {
                    val userDto = userResponse.body()!!
                    AuthResult.Success(
                        User(
                            id = userDto.id,
                            username = userDto.username,
                            email = userDto.email,
                            firstName = userDto.firstName,
                            lastName = userDto.lastName,
                            isStaff = userDto.isStaff,
                            isSuperuser = userDto.isSuperuser
                        )
                    )
                } else {
                    AuthResult.Error("Failed to fetch user data")
                }
            } else {
                AuthResult.Error(response.message() ?: "Login failed")
            }
        } catch (e: Exception) {
            AuthResult.Error(e.message ?: "Network error")
        }
    }

    /**
     * Clears stored tokens to log out the user.
     */
    override suspend fun logout() {
        tokenManager.clearTokens()
    }

    /**
     * Attempts to refresh the access token.
     *
     * Uses the stored refresh token to obtain a new access token.
     */
    override suspend fun refreshToken(): Boolean {
        val refreshToken = tokenManager.getRefreshToken() ?: return false
        return try {
            val response = api.refreshToken(
                com.edupath.data.api.dto.RefreshTokenRequest(refreshToken)
            )
            if (response.isSuccessful && response.body() != null) {
                tokenManager.saveTokens(response.body()!!.access, refreshToken)
                true
            } else {
                false
            }
        } catch (e: Exception) {
            false
        }
    }

    /**
     * Delegates to TokenManager to check login status.
     */
    override suspend fun isLoggedIn(): Boolean = tokenManager.isLoggedIn()

    /**
     * Fetches current user from API.
     *
     * @return User if authenticated and API call succeeds, null otherwise
     */
    override suspend fun getCurrentUser(): User? {
        return try {
            val response = api.getCurrentUser()
            if (response.isSuccessful && response.body() != null) {
                val dto = response.body()!!
                User(
                    id = dto.id,
                    username = dto.username,
                    email = dto.email,
                    firstName = dto.firstName,
                    lastName = dto.lastName,
                    isStaff = dto.isStaff,
                    isSuperuser = dto.isSuperuser
                )
            } else null
        } catch (e: Exception) {
            null
        }
    }
}
