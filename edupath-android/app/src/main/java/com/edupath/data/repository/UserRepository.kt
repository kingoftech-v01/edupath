package com.edupath.data.repository

import com.edupath.data.api.EduPathApi
import com.edupath.data.api.dto.UserProfileDto
import com.edupath.domain.model.User
import com.edupath.domain.model.UserProfile
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository interface for user data operations.
 *
 * Provides methods to fetch and update user information
 * and profile data.
 */
interface UserRepository {
    /**
     * Gets the currently authenticated user's basic information.
     *
     * @return Result containing User on success, error message on failure
     */
    suspend fun getCurrentUser(): Result<User>

    /**
     * Gets the current user's extended profile.
     *
     * @return Result containing UserProfile on success, error message on failure
     */
    suspend fun getUserProfile(): Result<UserProfile>

    /**
     * Updates the current user's profile.
     *
     * @param profile The updated profile data
     * @return Result containing updated UserProfile on success, error on failure
     */
    suspend fun updateProfile(profile: UserProfile): Result<UserProfile>
}

/**
 * Implementation of [UserRepository] using Retrofit.
 *
 * Handles user data operations via the EduPath API.
 *
 * @property api EduPath API interface
 */
@Singleton
class UserRepositoryImpl @Inject constructor(
    private val api: EduPathApi
) : UserRepository {

    /**
     * Fetches current user from API.
     *
     * @return Result.Success with User or Result.Error with message
     */
    override suspend fun getCurrentUser(): Result<User> {
        return try {
            val response = api.getCurrentUser()
            if (response.isSuccessful && response.body() != null) {
                val dto = response.body()!!
                Result.Success(
                    User(
                        id = dto.id,
                        username = dto.username,
                        email = dto.email,
                        firstName = dto.firstName,
                        lastName = dto.lastName,
                        isStaff = dto.isStaff,
                        isSuperuser = dto.isSuperuser
                    )
                )
            } else {
                Result.Error(response.message() ?: "Failed to get user")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }

    /**
     * Fetches user profile from API.
     *
     * @return Result.Success with UserProfile or Result.Error with message
     */
    override suspend fun getUserProfile(): Result<UserProfile> {
        return try {
            val response = api.getUserProfile()
            if (response.isSuccessful && response.body() != null) {
                val dto = response.body()!!
                Result.Success(
                    UserProfile(
                        id = dto.id ?: 0,
                        bio = dto.bio,
                        phone = dto.phone,
                        website = dto.website,
                        linkedinUrl = dto.linkedinUrl,
                        twitterUrl = dto.twitterUrl,
                        githubUrl = dto.githubUrl,
                        emailNotifications = dto.emailNotifications
                    )
                )
            } else {
                Result.Error(response.message() ?: "Failed to get profile")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }

    /**
     * Updates user profile via API.
     *
     * @param profile The profile data to update
     * @return Result.Success with updated profile or Result.Error
     */
    override suspend fun updateProfile(profile: UserProfile): Result<UserProfile> {
        return try {
            val dto = UserProfileDto(
                bio = profile.bio,
                phone = profile.phone,
                website = profile.website,
                linkedinUrl = profile.linkedinUrl,
                twitterUrl = profile.twitterUrl,
                githubUrl = profile.githubUrl,
                emailNotifications = profile.emailNotifications
            )
            val response = api.updateProfile(dto)
            if (response.isSuccessful && response.body() != null) {
                val updated = response.body()!!
                Result.Success(
                    UserProfile(
                        id = updated.id ?: 0,
                        bio = updated.bio,
                        phone = updated.phone,
                        website = updated.website,
                        linkedinUrl = updated.linkedinUrl,
                        twitterUrl = updated.twitterUrl,
                        githubUrl = updated.githubUrl,
                        emailNotifications = updated.emailNotifications
                    )
                )
            } else {
                Result.Error(response.message() ?: "Failed to update profile")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }
}
