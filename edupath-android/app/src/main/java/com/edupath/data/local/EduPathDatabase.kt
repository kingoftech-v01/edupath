package com.edupath.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.edupath.data.local.dao.CategoryDao
import com.edupath.data.local.dao.CourseDao
import com.edupath.data.local.entities.CategoryEntity
import com.edupath.data.local.entities.CourseEntity

/**
 * Room database for local data persistence and offline caching.
 *
 * This database stores courses and categories locally to enable
 * offline access and improve app performance by reducing network calls.
 *
 * Tables:
 * - courses: Cached course data
 * - categories: Cached category data
 *
 * @see CourseDao for course operations
 * @see CategoryDao for category operations
 */
@Database(
    entities = [
        CourseEntity::class,
        CategoryEntity::class
    ],
    version = 1,
    exportSchema = false
)
abstract class EduPathDatabase : RoomDatabase() {
    /**
     * Provides access to course database operations.
     *
     * @return CourseDao instance for CRUD operations on courses
     */
    abstract fun courseDao(): CourseDao

    /**
     * Provides access to category database operations.
     *
     * @return CategoryDao instance for CRUD operations on categories
     */
    abstract fun categoryDao(): CategoryDao
}
