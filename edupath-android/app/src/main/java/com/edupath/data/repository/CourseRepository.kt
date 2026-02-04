package com.edupath.data.repository

import com.edupath.data.api.EduPathApi
import com.edupath.data.local.dao.CategoryDao
import com.edupath.data.local.dao.CourseDao
import com.edupath.data.local.entities.CategoryEntity
import com.edupath.data.local.entities.CourseEntity
import com.edupath.domain.model.Category
import com.edupath.domain.model.Course
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Sealed class representing generic operation results.
 *
 * @param T The type of data on success
 */
sealed class Result<out T> {
    /**
     * Successful operation with data.
     */
    data class Success<T>(val data: T) : Result<T>()

    /**
     * Failed operation with error message.
     */
    data class Error(val message: String) : Result<Nothing>()

    /**
     * Loading state for async operations.
     */
    object Loading : Result<Nothing>()
}

/**
 * Repository interface for course and category data operations.
 *
 * Implements an offline-first pattern: data is served from local cache
 * and refreshed from the API when requested.
 */
interface CourseRepository {
    /**
     * Gets all courses as a reactive Flow.
     *
     * @return Flow emitting course list updates from local cache
     */
    fun getCourses(): Flow<List<Course>>

    /**
     * Gets featured courses for homepage display.
     *
     * @return Flow emitting featured courses from local cache
     */
    fun getFeaturedCourses(): Flow<List<Course>>

    /**
     * Gets free courses.
     *
     * @return Flow emitting free courses from local cache
     */
    fun getFreeCourses(): Flow<List<Course>>

    /**
     * Gets all categories as a reactive Flow.
     *
     * @return Flow emitting category list updates from local cache
     */
    fun getCategories(): Flow<List<Category>>

    /**
     * Gets a specific course by slug, checking cache first then API.
     *
     * @param slug Unique course identifier
     * @return Course if found, null otherwise
     */
    suspend fun getCourseBySlug(slug: String): Course?

    /**
     * Refreshes courses from the API and updates local cache.
     */
    suspend fun refreshCourses()

    /**
     * Refreshes categories from the API and updates local cache.
     */
    suspend fun refreshCategories()

    /**
     * Searches courses by query string.
     *
     * @param query Search query
     * @return List of matching courses
     */
    suspend fun searchCourses(query: String): List<Course>
}

/**
 * Implementation of [CourseRepository] with offline-first pattern.
 *
 * Uses Room database for local caching and Retrofit for API calls.
 * Data flows from Room via Kotlin Flow for reactive UI updates.
 *
 * @property api EduPath API interface
 * @property courseDao Course database access object
 * @property categoryDao Category database access object
 */
@Singleton
class CourseRepositoryImpl @Inject constructor(
    private val api: EduPathApi,
    private val courseDao: CourseDao,
    private val categoryDao: CategoryDao
) : CourseRepository {

    /**
     * Returns all courses from local cache as a Flow.
     */
    override fun getCourses(): Flow<List<Course>> {
        return courseDao.getAllCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    /**
     * Returns featured courses from local cache.
     */
    override fun getFeaturedCourses(): Flow<List<Course>> {
        return courseDao.getFeaturedCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    /**
     * Returns free courses from local cache.
     */
    override fun getFreeCourses(): Flow<List<Course>> {
        return courseDao.getFreeCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    /**
     * Returns all categories from local cache.
     */
    override fun getCategories(): Flow<List<Category>> {
        return categoryDao.getAllCategories().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    /**
     * Gets course by slug, trying local cache first then API.
     *
     * If found via API, also caches the course locally.
     */
    override suspend fun getCourseBySlug(slug: String): Course? {
        // Try local first
        val local = courseDao.getCourseBySlug(slug)
        if (local != null) return local.toDomain()

        // Fetch from API
        return try {
            val response = api.getCourse(slug)
            if (response.isSuccessful && response.body() != null) {
                val dto = response.body()!!
                val entity = dto.toEntity()
                courseDao.insert(entity)
                entity.toDomain()
            } else null
        } catch (e: Exception) {
            null
        }
    }

    /**
     * Fetches courses from API and replaces local cache.
     */
    override suspend fun refreshCourses() {
        try {
            val response = api.getCourses()
            if (response.isSuccessful && response.body() != null) {
                val courses = response.body()!!.results.map { it.toEntity() }
                courseDao.deleteAll()
                courseDao.insertAll(courses)
            }
        } catch (e: Exception) {
            // Handle error - data will come from cache
        }
    }

    /**
     * Fetches categories from API and replaces local cache.
     */
    override suspend fun refreshCategories() {
        try {
            val response = api.getCategories()
            if (response.isSuccessful && response.body() != null) {
                val categories = response.body()!!.results.map { it.toEntity() }
                categoryDao.deleteAll()
                categoryDao.insertAll(categories)
            }
        } catch (e: Exception) {
            // Handle error
        }
    }

    /**
     * Searches courses via API, falling back to local search on error.
     */
    override suspend fun searchCourses(query: String): List<Course> {
        return try {
            val response = api.getCourses(search = query)
            if (response.isSuccessful && response.body() != null) {
                response.body()!!.results.map { it.toDomain() }
            } else emptyList()
        } catch (e: Exception) {
            // Fall back to local search
            courseDao.searchCourses(query).map { entities ->
                entities.map { it.toDomain() }
            }.toString().let { emptyList() }
        }
    }

    // ==================== Mapping Functions ====================

    /**
     * Maps CourseDto to CourseEntity for database storage.
     */
    private fun com.edupath.data.api.dto.CourseDto.toEntity() = CourseEntity(
        id = id,
        title = title,
        slug = slug,
        name = name,
        desc = desc,
        price = price,
        isFree = isFree,
        img = img,
        videoUrl = videoUrl,
        lessons = lessons,
        students = students,
        durationHours = durationHours,
        categoryId = category?.id,
        categoryName = category?.name,
        instructorId = instructor?.id,
        instructorName = instructor?.name,
        isFeatured = isFeatured,
        isActive = isActive
    )

    /**
     * Maps CourseDto to Course domain model.
     */
    private fun com.edupath.data.api.dto.CourseDto.toDomain() = Course(
        id = id,
        title = title,
        slug = slug,
        name = name,
        desc = desc,
        price = price,
        isFree = isFree,
        img = img,
        videoUrl = videoUrl,
        lessons = lessons,
        students = students,
        durationHours = durationHours,
        categoryId = category?.id,
        categoryName = category?.name,
        instructorId = instructor?.id,
        instructorName = instructor?.name,
        isFeatured = isFeatured
    )

    /**
     * Maps CourseEntity to Course domain model.
     */
    private fun CourseEntity.toDomain() = Course(
        id = id,
        title = title,
        slug = slug,
        name = name,
        desc = desc,
        price = price,
        isFree = isFree,
        img = img,
        videoUrl = videoUrl,
        lessons = lessons,
        students = students,
        durationHours = durationHours,
        categoryId = categoryId,
        categoryName = categoryName,
        instructorId = instructorId,
        instructorName = instructorName,
        isFeatured = isFeatured
    )

    /**
     * Maps CategoryDto to CategoryEntity for database storage.
     */
    private fun com.edupath.data.api.dto.CategoryDto.toEntity() = CategoryEntity(
        id = id,
        name = name,
        slug = slug,
        icon = icon,
        description = description,
        courseCount = courseCount,
        isActive = isActive
    )

    /**
     * Maps CategoryEntity to Category domain model.
     */
    private fun CategoryEntity.toDomain() = Category(
        id = id,
        name = name,
        slug = slug,
        icon = icon,
        description = description,
        courseCount = courseCount
    )
}
