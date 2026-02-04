package com.edupath.domain.usecase

import com.edupath.data.repository.CourseRepository
import com.edupath.domain.model.Course
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

/**
 * Use case for getting all courses.
 *
 * Returns a reactive Flow of courses from the repository.
 *
 * @property repository Course data repository
 */
class GetCoursesUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Gets all courses as a Flow.
     *
     * @return Flow emitting course list updates
     */
    operator fun invoke(): Flow<List<Course>> = repository.getCourses()
}

/**
 * Use case for getting featured courses.
 *
 * Returns courses marked as featured for homepage display.
 *
 * @property repository Course data repository
 */
class GetFeaturedCoursesUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Gets featured courses as a Flow.
     *
     * @return Flow emitting featured courses
     */
    operator fun invoke(): Flow<List<Course>> = repository.getFeaturedCourses()
}

/**
 * Use case for getting free courses.
 *
 * @property repository Course data repository
 */
class GetFreeCoursesUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Gets free courses as a Flow.
     *
     * @return Flow emitting free courses
     */
    operator fun invoke(): Flow<List<Course>> = repository.getFreeCourses()
}

/**
 * Use case for getting a single course by its slug.
 *
 * @property repository Course data repository
 */
class GetCourseBySlugUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Gets a course by its URL slug.
     *
     * @param slug Unique course identifier
     * @return Course if found, null otherwise
     */
    suspend operator fun invoke(slug: String): Course? = repository.getCourseBySlug(slug)
}

/**
 * Use case for searching courses.
 *
 * @property repository Course data repository
 */
class SearchCoursesUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Searches courses by query string.
     *
     * @param query Search query
     * @return List of matching courses
     */
    suspend operator fun invoke(query: String): List<Course> = repository.searchCourses(query)
}

/**
 * Use case for refreshing course data from the API.
 *
 * @property repository Course data repository
 */
class RefreshCoursesUseCase @Inject constructor(
    private val repository: CourseRepository
) {
    /**
     * Refreshes courses from the backend API.
     */
    suspend operator fun invoke() = repository.refreshCourses()
}
