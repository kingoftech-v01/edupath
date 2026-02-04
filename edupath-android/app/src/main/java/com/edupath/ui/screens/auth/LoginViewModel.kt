package com.edupath.ui.screens.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.data.repository.AuthResult
import com.edupath.domain.usecase.LoginUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the login screen.
 *
 * @property username Current username input
 * @property password Current password input
 * @property isLoading Whether login is in progress
 * @property error Error message if login failed
 * @property isLoggedIn Whether login was successful
 */
data class LoginUiState(
    val username: String = "",
    val password: String = "",
    val isLoading: Boolean = false,
    val error: String? = null,
    val isLoggedIn: Boolean = false
)

/**
 * ViewModel for the login screen.
 *
 * Manages login form state and handles authentication logic
 * by delegating to [LoginUseCase].
 *
 * @property loginUseCase Use case for performing login
 */
@HiltViewModel
class LoginViewModel @Inject constructor(
    private val loginUseCase: LoginUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(LoginUiState())

    /** Observable login UI state. */
    val uiState: StateFlow<LoginUiState> = _uiState.asStateFlow()

    /**
     * Updates the username field and clears any error.
     *
     * @param username New username value
     */
    fun onUsernameChange(username: String) {
        _uiState.update { it.copy(username = username, error = null) }
    }

    /**
     * Updates the password field and clears any error.
     *
     * @param password New password value
     */
    fun onPasswordChange(password: String) {
        _uiState.update { it.copy(password = password, error = null) }
    }

    /**
     * Attempts to log in with current credentials.
     *
     * Sets isLoading during the operation and updates
     * isLoggedIn or error based on the result.
     */
    fun login() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            when (val result = loginUseCase(_uiState.value.username, _uiState.value.password)) {
                is AuthResult.Success -> {
                    _uiState.update { it.copy(isLoading = false, isLoggedIn = true) }
                }
                is AuthResult.Error -> {
                    _uiState.update { it.copy(isLoading = false, error = result.message) }
                }
                AuthResult.Loading -> {
                    // Already handled
                }
            }
        }
    }
}
