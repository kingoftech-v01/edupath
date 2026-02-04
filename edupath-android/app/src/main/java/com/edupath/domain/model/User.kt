package com.edupath.domain.model

/**
 * Domain model representing a user account.
 *
 * @property id Unique user identifier
 * @property username User's login name
 * @property email User's email address
 * @property firstName User's first name
 * @property lastName User's last name
 * @property isStaff Whether user has staff privileges
 * @property isSuperuser Whether user has admin privileges
 */
data class User(
    val id: Int,
    val username: String,
    val email: String,
    val firstName: String = "",
    val lastName: String = "",
    val isStaff: Boolean = false,
    val isSuperuser: Boolean = false
) {
    /**
     * Returns the user's full name, or username if no name is set.
     */
    val fullName: String
        get() = "$firstName $lastName".trim().ifEmpty { username }
}

/**
 * Domain model representing a user's extended profile.
 *
 * @property id Profile identifier
 * @property bio User biography
 * @property phone Phone number
 * @property website Personal website URL
 * @property linkedinUrl LinkedIn profile URL
 * @property twitterUrl Twitter profile URL
 * @property githubUrl GitHub profile URL
 * @property emailNotifications Whether email notifications are enabled
 */
data class UserProfile(
    val id: Int = 0,
    val bio: String = "",
    val phone: String = "",
    val website: String = "",
    val linkedinUrl: String = "",
    val twitterUrl: String = "",
    val githubUrl: String = "",
    val emailNotifications: Boolean = true
)
