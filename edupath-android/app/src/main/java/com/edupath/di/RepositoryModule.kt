package com.edupath.di

import com.edupath.data.repository.AuthRepository
import com.edupath.data.repository.AuthRepositoryImpl
import com.edupath.data.repository.CourseRepository
import com.edupath.data.repository.CourseRepositoryImpl
import com.edupath.data.repository.UserRepository
import com.edupath.data.repository.UserRepositoryImpl
import dagger.Binds
import dagger.Module
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

/**
 * Hilt module that binds repository implementations to their interfaces.
 *
 * This module uses @Binds annotations to tell Hilt which concrete
 * implementation to use when a repository interface is requested.
 *
 * Repositories provided:
 * - AuthRepository for authentication operations
 * - CourseRepository for course data operations
 * - UserRepository for user data operations
 */
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    /**
     * Binds the AuthRepository implementation.
     *
     * @param impl The concrete AuthRepositoryImpl instance
     * @return AuthRepository interface backed by the implementation
     */
    @Binds
    @Singleton
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository

    /**
     * Binds the CourseRepository implementation.
     *
     * @param impl The concrete CourseRepositoryImpl instance
     * @return CourseRepository interface backed by the implementation
     */
    @Binds
    @Singleton
    abstract fun bindCourseRepository(impl: CourseRepositoryImpl): CourseRepository

    /**
     * Binds the UserRepository implementation.
     *
     * @param impl The concrete UserRepositoryImpl instance
     * @return UserRepository interface backed by the implementation
     */
    @Binds
    @Singleton
    abstract fun bindUserRepository(impl: UserRepositoryImpl): UserRepository
}
