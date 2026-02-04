package com.edupath

import com.edupath.data.repository.AuthRepository
import com.edupath.data.repository.AuthResult
import com.edupath.domain.model.User
import com.edupath.domain.usecase.LoginUseCase
import io.mockk.coEvery
import io.mockk.coVerify
import io.mockk.mockk
import kotlinx.coroutines.test.runTest
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*

class UseCaseTest {

    private lateinit var authRepository: AuthRepository

    @Before
    fun setup() {
        authRepository = mockk()
    }

    @Test
    fun `LoginUseCase returns error when username is blank`() = runTest {
        val useCase = LoginUseCase(authRepository)

        val result = useCase("", "password123")

        assertTrue(result is AuthResult.Error)
        assertEquals("Username is required", (result as AuthResult.Error).message)
    }

    @Test
    fun `LoginUseCase returns error when password is blank`() = runTest {
        val useCase = LoginUseCase(authRepository)

        val result = useCase("username", "")

        assertTrue(result is AuthResult.Error)
        assertEquals("Password is required", (result as AuthResult.Error).message)
    }

    @Test
    fun `LoginUseCase calls repository when credentials are valid`() = runTest {
        val mockUser = User(
            id = 1,
            username = "testuser",
            email = "test@example.com"
        )
        coEvery { authRepository.login(any(), any()) } returns AuthResult.Success(mockUser)

        val useCase = LoginUseCase(authRepository)
        val result = useCase("testuser", "password123")

        assertTrue(result is AuthResult.Success)
        coVerify { authRepository.login("testuser", "password123") }
    }

    @Test
    fun `LoginUseCase returns repository error`() = runTest {
        coEvery { authRepository.login(any(), any()) } returns AuthResult.Error("Invalid credentials")

        val useCase = LoginUseCase(authRepository)
        val result = useCase("testuser", "wrongpass")

        assertTrue(result is AuthResult.Error)
        assertEquals("Invalid credentials", (result as AuthResult.Error).message)
    }
}
