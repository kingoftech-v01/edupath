package com.edupath.data.repository

import com.edupath.data.api.EduPathApi
import com.edupath.data.api.dto.LoginRequest
import com.edupath.domain.model.User
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject
import javax.inject.Singleton

/** Auth operation result: Success, Error, or Loading. */
sealed class AuthResult<out T> {
    data class Success<T>(val data: T) : AuthResult<T>()
    data class Error(val message: String) : AuthResult<Nothing>()
    object Loading : AuthResult<Nothing>()
}

/** Authentication operations interface. */
interface AuthRepository {
    suspend fun login(username: String, password: String): AuthResult<User>
    suspend fun logout()
    suspend fun refreshToken(): Boolean
    suspend fun isLoggedIn(): Boolean
    suspend fun getCurrentUser(): User?
}

/** Auth implementation with JWT token management. */
@Singleton
class AuthRepositoryImpl @Inject constructor(
    private val api: EduPathApi,
    private val tokenManager: TokenManager
) : AuthRepository {

    override suspend fun login(username: String, password: String): AuthResult<User> {
        return try {
            val response = api.login(LoginRequest(username, password))
            if (response.isSuccessful && response.body() != null) {
                val authResponse = response.body()!!
                tokenManager.saveTokens(authResponse.access, authResponse.refresh)

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

    override suspend fun logout() {
        tokenManager.clearTokens()
    }

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

    override suspend fun isLoggedIn(): Boolean = tokenManager.isLoggedIn()

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
