package com.edupath.di

import android.content.Context
import androidx.room.Room
import com.edupath.data.local.EduPathDatabase
import com.edupath.data.local.dao.CourseDao
import com.edupath.data.local.dao.CategoryDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

/**
 * Hilt module that provides database-related dependencies.
 *
 * This module configures and provides singleton instances of:
 * - Room database for local data persistence
 * - Data Access Objects (DAOs) for database operations
 *
 * The database uses destructive migration, meaning data will be lost
 * on schema changes. For production, implement proper migrations.
 */
@Module
@InstallIn(SingletonComponent::class)
object DatabaseModule {

    /**
     * Provides the Room database instance.
     *
     * Creates the EduPath database with destructive migration enabled.
     * The database is used for offline caching of courses and categories.
     *
     * @param context The application context for database creation
     * @return Singleton EduPathDatabase instance
     */
    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): EduPathDatabase =
        Room.databaseBuilder(
            context,
            EduPathDatabase::class.java,
            "edupath_database"
        )
            .fallbackToDestructiveMigration()
            .build()

    /**
     * Provides the Course DAO for course-related database operations.
     *
     * @param database The Room database instance
     * @return CourseDao for CRUD operations on courses
     */
    @Provides
    @Singleton
    fun provideCourseDao(database: EduPathDatabase): CourseDao = database.courseDao()

    /**
     * Provides the Category DAO for category-related database operations.
     *
     * @param database The Room database instance
     * @return CategoryDao for CRUD operations on categories
     */
    @Provides
    @Singleton
    fun provideCategoryDao(database: EduPathDatabase): CategoryDao = database.categoryDao()
}
