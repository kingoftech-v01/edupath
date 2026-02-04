package com.edupath.data.api.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

/**
 * Data transfer object for user information from the API.
 *
 * Contains basic user account data including authentication info
 * and permission flags.
 *
 * @property id Unique user identifier
 * @property username User's login name
 * @property email User's email address
 * @property firstName User's first name
 * @property lastName User's last name
 * @property isStaff Whether user has staff privileges
 * @property isSuperuser Whether user has superuser/admin privileges
 */
@JsonClass(generateAdapter = true)
data class UserDto(
    val id: Int,
    val username: String,
    val email: String,
    @Json(name = "first_name") val firstName: String = "",
    @Json(name = "last_name") val lastName: String = "",
    @Json(name = "is_staff") val isStaff: Boolean = false,
    @Json(name = "is_superuser") val isSuperuser: Boolean = false
)

/**
 * Data transfer object for user profile information.
 *
 * Contains extended profile data including bio, social links,
 * and notification preferences.
 *
 * @property id Profile ID
 * @property user Associated user ID
 * @property avatar URL to user's avatar image
 * @property bio User's biography text
 * @property phone User's phone number
 * @property website User's personal website URL
 * @property linkedinUrl LinkedIn profile URL
 * @property twitterUrl Twitter profile URL
 * @property githubUrl GitHub profile URL
 * @property emailNotifications Whether email notifications are enabled
 */
@JsonClass(generateAdapter = true)
data class UserProfileDto(
    val id: Int? = null,
    val user: Int? = null,
    val avatar: String? = null,
    val bio: String = "",
    val phone: String = "",
    val website: String = "",
    @Json(name = "linkedin_url") val linkedinUrl: String = "",
    @Json(name = "twitter_url") val twitterUrl: String = "",
    @Json(name = "github_url") val githubUrl: String = "",
    @Json(name = "email_notifications") val emailNotifications: Boolean = true
)
