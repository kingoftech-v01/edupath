package com.edupath

import com.edupath.data.repository.AuthResult
import com.edupath.domain.model.User
import com.edupath.domain.usecase.LoginUseCase
import com.edupath.ui.screens.auth.LoginViewModel
import io.mockk.coEvery
import io.mockk.mockk
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*

@OptIn(ExperimentalCoroutinesApi::class)
class LoginViewModelTest {

    private val testDispatcher = StandardTestDispatcher()
    private lateinit var loginUseCase: LoginUseCase
    private lateinit var viewModel: LoginViewModel

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        loginUseCase = mockk()
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `initial state is empty`() {
        viewModel = LoginViewModel(loginUseCase)

        val state = viewModel.uiState.value
        assertEquals("", state.username)
        assertEquals("", state.password)
        assertFalse(state.isLoading)
        assertNull(state.error)
        assertFalse(state.isLoggedIn)
    }

    @Test
    fun `onUsernameChange updates username`() {
        viewModel = LoginViewModel(loginUseCase)

        viewModel.onUsernameChange("testuser")

        assertEquals("testuser", viewModel.uiState.value.username)
    }

    @Test
    fun `onPasswordChange updates password`() {
        viewModel = LoginViewModel(loginUseCase)

        viewModel.onPasswordChange("password123")

        assertEquals("password123", viewModel.uiState.value.password)
    }

    @Test
    fun `login success sets isLoggedIn to true`() = runTest {
        val mockUser = User(
            id = 1,
            username = "testuser",
            email = "test@example.com"
        )
        coEvery { loginUseCase(any(), any()) } returns AuthResult.Success(mockUser)

        viewModel = LoginViewModel(loginUseCase)
        viewModel.onUsernameChange("testuser")
        viewModel.onPasswordChange("password123")
        viewModel.login()

        advanceUntilIdle()

        assertTrue(viewModel.uiState.value.isLoggedIn)
        assertFalse(viewModel.uiState.value.isLoading)
    }

    @Test
    fun `login failure sets error`() = runTest {
        coEvery { loginUseCase(any(), any()) } returns AuthResult.Error("Invalid credentials")

        viewModel = LoginViewModel(loginUseCase)
        viewModel.onUsernameChange("testuser")
        viewModel.onPasswordChange("wrongpass")
        viewModel.login()

        advanceUntilIdle()

        assertFalse(viewModel.uiState.value.isLoggedIn)
        assertEquals("Invalid credentials", viewModel.uiState.value.error)
    }
}
