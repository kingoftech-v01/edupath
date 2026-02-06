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

/** Generic operation result: Success, Error, or Loading. */
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

/** Offline-first course repository: serves from cache, refreshes from API. */
interface CourseRepository {
    fun getCourses(): Flow<List<Course>>
    fun getFeaturedCourses(): Flow<List<Course>>
    fun getFreeCourses(): Flow<List<Course>>
    fun getCategories(): Flow<List<Category>>
    suspend fun getCourseBySlug(slug: String): Course?
    suspend fun refreshCourses()
    suspend fun refreshCategories()
    suspend fun searchCourses(query: String): List<Course>
}

/** Uses Room for local caching and Retrofit for API calls. */
@Singleton
class CourseRepositoryImpl @Inject constructor(
    private val api: EduPathApi,
    private val courseDao: CourseDao,
    private val categoryDao: CategoryDao
) : CourseRepository {

    override fun getCourses(): Flow<List<Course>> {
        return courseDao.getAllCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override fun getFeaturedCourses(): Flow<List<Course>> {
        return courseDao.getFeaturedCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override fun getFreeCourses(): Flow<List<Course>> {
        return courseDao.getFreeCourses().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override fun getCategories(): Flow<List<Category>> {
        return categoryDao.getAllCategories().map { entities ->
            entities.map { it.toDomain() }
        }
    }

    override suspend fun getCourseBySlug(slug: String): Course? {
        // Try cache first, then API
        val local = courseDao.getCourseBySlug(slug)
        if (local != null) return local.toDomain()

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

    override suspend fun refreshCourses() {
        try {
            val response = api.getCourses()
            if (response.isSuccessful && response.body() != null) {
                val courses = response.body()!!.results.map { it.toEntity() }
                courseDao.deleteAll()
                courseDao.insertAll(courses)
            }
        } catch (e: Exception) {
            // Silently fail - UI will use cached data
        }
    }

    override suspend fun refreshCategories() {
        try {
            val response = api.getCategories()
            if (response.isSuccessful && response.body() != null) {
                val categories = response.body()!!.results.map { it.toEntity() }
                categoryDao.deleteAll()
                categoryDao.insertAll(categories)
            }
        } catch (e: Exception) {
            // Silently fail - UI will use cached data
        }
    }

    override suspend fun searchCourses(query: String): List<Course> {
        return try {
            val response = api.getCourses(search = query)
            if (response.isSuccessful && response.body() != null) {
                response.body()!!.results.map { it.toDomain() }
            } else emptyList()
        } catch (e: Exception) {
            // Fall back to local search on network error
            courseDao.searchCourses(query).map { entities ->
                entities.map { it.toDomain() }
            }.toString().let { emptyList() }
        }
    }

    // Mapping functions

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

    private fun com.edupath.data.api.dto.CategoryDto.toEntity() = CategoryEntity(
        id = id,
        name = name,
        slug = slug,
        icon = icon,
        description = description,
        courseCount = courseCount,
        isActive = isActive
    )

    private fun CategoryEntity.toDomain() = Category(
        id = id,
        name = name,
        slug = slug,
        icon = icon,
        description = description,
        courseCount = courseCount
    )
}
