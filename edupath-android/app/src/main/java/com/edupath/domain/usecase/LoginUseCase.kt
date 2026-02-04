package com.edupath.domain.usecase

import com.edupath.data.repository.AuthRepository
import com.edupath.data.repository.AuthResult
import com.edupath.domain.model.User
import javax.inject.Inject

/**
 * Use case for user login with validation.
 *
 * Validates input before delegating to the repository.
 * Returns validation errors for empty username/password.
 *
 * @property repository Authentication repository
 */
class LoginUseCase @Inject constructor(
    private val repository: AuthRepository
) {
    /**
     * Attempts to log in with the provided credentials.
     *
     * @param username User's username or email
     * @param password User's password
     * @return AuthResult.Success with User on success,
     *         AuthResult.Error with validation or auth error message
     */
    suspend operator fun invoke(username: String, password: String): AuthResult<User> {
        if (username.isBlank()) {
            return AuthResult.Error("Username is required")
        }
        if (password.isBlank()) {
            return AuthResult.Error("Password is required")
        }
        return repository.login(username, password)
    }
}

/**
 * Use case for user logout.
 *
 * Clears stored authentication tokens.
 *
 * @property repository Authentication repository
 */
class LogoutUseCase @Inject constructor(
    private val repository: AuthRepository
) {
    /**
     * Logs out the current user.
     */
    suspend operator fun invoke() = repository.logout()
}

/**
 * Use case for checking authentication status.
 *
 * @property repository Authentication repository
 */
class CheckAuthUseCase @Inject constructor(
    private val repository: AuthRepository
) {
    /**
     * Checks if a user is currently logged in.
     *
     * @return true if logged in, false otherwise
     */
    suspend operator fun invoke(): Boolean = repository.isLoggedIn()
}

/**
 * Use case for getting the current user.
 *
 * @property repository Authentication repository
 */
class GetCurrentUserUseCase @Inject constructor(
    private val repository: AuthRepository
) {
    /**
     * Gets the currently authenticated user.
     *
     * @return User if authenticated, null otherwise
     */
    suspend operator fun invoke(): User? = repository.getCurrentUser()
}
