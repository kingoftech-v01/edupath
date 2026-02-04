package com.edupath

import app.cash.turbine.test
import com.edupath.data.repository.CourseRepository
import com.edupath.domain.model.Category
import com.edupath.domain.model.Course
import com.edupath.domain.usecase.*
import com.edupath.ui.screens.home.HomeViewModel
import io.mockk.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*

@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModelTest {

    private val testDispatcher = StandardTestDispatcher()
    private lateinit var getFeaturedCoursesUseCase: GetFeaturedCoursesUseCase
    private lateinit var getCoursesUseCase: GetCoursesUseCase
    private lateinit var refreshCoursesUseCase: RefreshCoursesUseCase
    private lateinit var logoutUseCase: LogoutUseCase
    private lateinit var courseRepository: CourseRepository

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        getFeaturedCoursesUseCase = mockk()
        getCoursesUseCase = mockk()
        refreshCoursesUseCase = mockk()
        logoutUseCase = mockk()
        courseRepository = mockk()
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `initial state is loading`() = runTest {
        val courses = listOf(
            Course(id = 1, title = "Course 1", slug = "course-1", desc = "Desc 1", isFeatured = true),
            Course(id = 2, title = "Course 2", slug = "course-2", desc = "Desc 2", isFeatured = true)
        )
        val categories = listOf(
            Category(id = 1, name = "Development", slug = "development")
        )

        every { getFeaturedCoursesUseCase() } returns flowOf(courses)
        every { getCoursesUseCase() } returns flowOf(courses)
        every { courseRepository.getCategories() } returns flowOf(categories)
        coEvery { refreshCoursesUseCase() } just Runs
        coEvery { courseRepository.refreshCategories() } just Runs

        val viewModel = HomeViewModel(
            getFeaturedCoursesUseCase,
            getCoursesUseCase,
            refreshCoursesUseCase,
            logoutUseCase,
            courseRepository
        )

        assertTrue(viewModel.uiState.value.isLoading)
    }

    @Test
    fun `logout sets loggedOut to true`() = runTest {
        val courses = emptyList<Course>()
        val categories = emptyList<Category>()

        every { getFeaturedCoursesUseCase() } returns flowOf(courses)
        every { getCoursesUseCase() } returns flowOf(courses)
        every { courseRepository.getCategories() } returns flowOf(categories)
        coEvery { refreshCoursesUseCase() } just Runs
        coEvery { courseRepository.refreshCategories() } just Runs
        coEvery { logoutUseCase() } just Runs

        val viewModel = HomeViewModel(
            getFeaturedCoursesUseCase,
            getCoursesUseCase,
            refreshCoursesUseCase,
            logoutUseCase,
            courseRepository
        )

        viewModel.logout()
        advanceUntilIdle()

        assertTrue(viewModel.uiState.value.loggedOut)
        coVerify { logoutUseCase() }
    }
}
