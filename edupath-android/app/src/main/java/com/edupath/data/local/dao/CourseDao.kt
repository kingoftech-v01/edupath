package com.edupath.data.local.dao

import androidx.room.*
import com.edupath.data.local.entities.CourseEntity
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object for course-related database operations.
 *
 * Provides methods for querying, inserting, updating, and deleting
 * courses in the local SQLite database. Uses Kotlin Flow for
 * reactive data streams.
 */
@Dao
interface CourseDao {

    /**
     * Gets all active courses ordered by ID descending (newest first).
     *
     * @return Flow emitting list of courses that updates on database changes
     */
    @Query("SELECT * FROM courses WHERE isActive = 1 ORDER BY id DESC")
    fun getAllCourses(): Flow<List<CourseEntity>>

    /**
     * Gets featured courses for homepage display.
     *
     * @return Flow emitting up to 6 featured, active courses
     */
    @Query("SELECT * FROM courses WHERE isFeatured = 1 AND isActive = 1 LIMIT 6")
    fun getFeaturedCourses(): Flow<List<CourseEntity>>

    /**
     * Gets all free courses.
     *
     * @return Flow emitting list of free, active courses
     */
    @Query("SELECT * FROM courses WHERE isFree = 1 AND isActive = 1")
    fun getFreeCourses(): Flow<List<CourseEntity>>

    /**
     * Gets a specific course by its URL slug.
     *
     * @param slug Unique course identifier
     * @return The course entity or null if not found
     */
    @Query("SELECT * FROM courses WHERE slug = :slug LIMIT 1")
    suspend fun getCourseBySlug(slug: String): CourseEntity?

    /**
     * Gets all courses in a specific category.
     *
     * @param categoryId Category ID to filter by
     * @return Flow emitting courses in the specified category
     */
    @Query("SELECT * FROM courses WHERE categoryId = :categoryId AND isActive = 1")
    fun getCoursesByCategory(categoryId: Int): Flow<List<CourseEntity>>

    /**
     * Searches courses by title or description.
     *
     * @param query Search query string
     * @return Flow emitting matching courses
     */
    @Query("SELECT * FROM courses WHERE title LIKE '%' || :query || '%' OR desc LIKE '%' || :query || '%'")
    fun searchCourses(query: String): Flow<List<CourseEntity>>

    /**
     * Inserts or replaces multiple courses.
     *
     * @param courses List of courses to insert/replace
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(courses: List<CourseEntity>)

    /**
     * Inserts or replaces a single course.
     *
     * @param course Course to insert/replace
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(course: CourseEntity)

    /**
     * Deletes a specific course.
     *
     * @param course Course to delete
     */
    @Delete
    suspend fun delete(course: CourseEntity)

    /**
     * Deletes all courses from the database.
     */
    @Query("DELETE FROM courses")
    suspend fun deleteAll()

    /**
     * Deletes courses cached before a specific timestamp.
     *
     * Used for cache invalidation and cleanup.
     *
     * @param timestamp Cutoff timestamp in milliseconds
     */
    @Query("DELETE FROM courses WHERE cachedAt < :timestamp")
    suspend fun deleteOlderThan(timestamp: Long)
}
