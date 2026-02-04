package com.edupath

import com.edupath.data.api.EduPathApi
import com.edupath.data.api.dto.CategoryDto
import com.edupath.data.api.dto.CourseDto
import com.edupath.data.api.dto.PaginatedResponse
import com.edupath.data.local.dao.CategoryDao
import com.edupath.data.local.dao.CourseDao
import com.edupath.data.repository.CourseRepositoryImpl
import io.mockk.*
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.runTest
import okhttp3.ResponseBody.Companion.toResponseBody
import org.junit.Before
import org.junit.Test
import org.junit.Assert.*
import retrofit2.Response

class CourseRepositoryTest {

    private lateinit var api: EduPathApi
    private lateinit var courseDao: CourseDao
    private lateinit var categoryDao: CategoryDao
    private lateinit var repository: CourseRepositoryImpl

    @Before
    fun setup() {
        api = mockk()
        courseDao = mockk(relaxed = true)
        categoryDao = mockk(relaxed = true)
        repository = CourseRepositoryImpl(api, courseDao, categoryDao)
    }

    @Test
    fun `getCourses returns flow from dao`() = runTest {
        every { courseDao.getAllCourses() } returns flowOf(emptyList())

        repository.getCourses().collect { courses ->
            assertTrue(courses.isEmpty())
        }
    }

    @Test
    fun `getFeaturedCourses returns flow from dao`() = runTest {
        every { courseDao.getFeaturedCourses() } returns flowOf(emptyList())

        repository.getFeaturedCourses().collect { courses ->
            assertTrue(courses.isEmpty())
        }
    }

    @Test
    fun `refreshCourses fetches from API and saves to dao`() = runTest {
        val courseDto = CourseDto(
            id = 1,
            title = "Test Course",
            slug = "test-course",
            desc = "Description"
        )
        val response = PaginatedResponse(
            count = 1,
            next = null,
            previous = null,
            results = listOf(courseDto)
        )
        coEvery { api.getCourses() } returns Response.success(response)
        coEvery { courseDao.deleteAll() } just Runs
        coEvery { courseDao.insertAll(any()) } just Runs

        repository.refreshCourses()

        coVerify { courseDao.deleteAll() }
        coVerify { courseDao.insertAll(any()) }
    }

    @Test
    fun `refreshCategories fetches from API and saves to dao`() = runTest {
        val categoryDto = CategoryDto(
            id = 1,
            name = "Development",
            slug = "development"
        )
        val response = PaginatedResponse(
            count = 1,
            next = null,
            previous = null,
            results = listOf(categoryDto)
        )
        coEvery { api.getCategories() } returns Response.success(response)
        coEvery { categoryDao.deleteAll() } just Runs
        coEvery { categoryDao.insertAll(any()) } just Runs

        repository.refreshCategories()

        coVerify { categoryDao.deleteAll() }
        coVerify { categoryDao.insertAll(any()) }
    }

    @Test
    fun `getCourseBySlug returns from local first`() = runTest {
        val entity = com.edupath.data.local.entities.CourseEntity(
            id = 1,
            title = "Test Course",
            slug = "test-course",
            name = "Instructor",
            desc = "Description",
            price = "49.99",
            isFree = false,
            img = null,
            videoUrl = "",
            lessons = 10,
            students = 100,
            durationHours = 5,
            categoryId = 1,
            categoryName = "Development",
            instructorId = 1,
            instructorName = "John Doe",
            isFeatured = true,
            isActive = true
        )
        coEvery { courseDao.getCourseBySlug("test-course") } returns entity

        val result = repository.getCourseBySlug("test-course")

        assertNotNull(result)
        assertEquals("Test Course", result?.title)
        coVerify(exactly = 0) { api.getCourse(any()) }
    }
}
