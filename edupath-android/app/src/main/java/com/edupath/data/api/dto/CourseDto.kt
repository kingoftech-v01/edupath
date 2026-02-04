package com.edupath.data.api.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

/**
 * Data transfer object for course information from the API.
 *
 * @property id Unique course identifier
 * @property title Course display title
 * @property slug URL-friendly unique identifier
 * @property name Course short name
 * @property desc Course description
 * @property price Course price as string (e.g., "29.99")
 * @property isFree Whether the course is free
 * @property img URL to course thumbnail image
 * @property videoUrl URL to course intro/preview video
 * @property lessons Number of lessons in the course
 * @property students Number of enrolled students
 * @property durationHours Total course duration in hours
 * @property category The course category
 * @property instructor The course instructor
 * @property isFeatured Whether course is featured on homepage
 * @property isActive Whether course is publicly visible
 */
@JsonClass(generateAdapter = true)
data class CourseDto(
    val id: Int,
    val title: String,
    val slug: String,
    val name: String = "",
    val desc: String,
    val price: String = "0.00",
    @Json(name = "is_free") val isFree: Boolean = false,
    val img: String? = null,
    @Json(name = "video_url") val videoUrl: String = "",
    val lessons: Int = 0,
    val students: Int = 0,
    @Json(name = "duration_hours") val durationHours: Int = 0,
    val category: CategoryDto? = null,
    val instructor: InstructorDto? = null,
    @Json(name = "is_featured") val isFeatured: Boolean = false,
    @Json(name = "is_active") val isActive: Boolean = true
)

/**
 * Data transfer object for course category information.
 *
 * @property id Unique category identifier
 * @property name Category display name
 * @property slug URL-friendly unique identifier
 * @property icon Icon identifier for the category
 * @property description Category description
 * @property courseCount Number of courses in this category
 * @property isActive Whether category is publicly visible
 */
@JsonClass(generateAdapter = true)
data class CategoryDto(
    val id: Int,
    val name: String,
    val slug: String,
    val icon: String = "",
    val description: String = "",
    @Json(name = "course_count") val courseCount: Int = 0,
    @Json(name = "is_active") val isActive: Boolean = true
)

/**
 * Data transfer object for instructor information.
 *
 * @property id Unique instructor identifier
 * @property name Instructor's full name
 * @property slug URL-friendly unique identifier
 * @property title Professional title (e.g., "Senior Developer")
 * @property bio Instructor biography
 * @property img URL to instructor profile image
 * @property facebookUrl Facebook profile URL
 * @property instagramUrl Instagram profile URL
 * @property linkedinUrl LinkedIn profile URL
 * @property twitterUrl Twitter profile URL
 * @property isActive Whether instructor profile is publicly visible
 */
@JsonClass(generateAdapter = true)
data class InstructorDto(
    val id: Int,
    val name: String,
    val slug: String,
    val title: String = "",
    val bio: String = "",
    val img: String? = null,
    @Json(name = "facebook_url") val facebookUrl: String = "",
    @Json(name = "instagram_url") val instagramUrl: String = "",
    @Json(name = "linkedin_url") val linkedinUrl: String = "",
    @Json(name = "twitter_url") val twitterUrl: String = "",
    @Json(name = "is_active") val isActive: Boolean = true
)

/**
 * Data transfer object for course review information.
 *
 * @property id Unique review identifier
 * @property name Reviewer's display name
 * @property title Reviewer's title (default: "Student")
 * @property desc Review text content
 * @property rating Rating value (typically 1-5)
 * @property img URL to reviewer's avatar
 * @property course Associated course ID
 * @property user Associated user ID
 * @property isActive Whether review is publicly visible
 */
@JsonClass(generateAdapter = true)
data class ReviewDto(
    val id: Int,
    val name: String,
    val title: String = "Student",
    val desc: String,
    val rating: Int,
    val img: String? = null,
    val course: Int? = null,
    val user: Int? = null,
    @Json(name = "is_active") val isActive: Boolean = true
)

/**
 * Request body for creating a new course review.
 *
 * @property course ID of the course being reviewed
 * @property rating Rating value (typically 1-5)
 * @property desc Review text content
 * @property name Optional reviewer name override
 */
@JsonClass(generateAdapter = true)
data class ReviewCreateDto(
    val course: Int,
    val rating: Int,
    val desc: String,
    val name: String = ""
)

/**
 * Generic paginated response wrapper for list endpoints.
 *
 * @param T The type of items in the results list
 * @property count Total number of items across all pages
 * @property next URL to the next page, null if on last page
 * @property previous URL to the previous page, null if on first page
 * @property results List of items for the current page
 */
@JsonClass(generateAdapter = true)
data class PaginatedResponse<T>(
    val count: Int,
    val next: String?,
    val previous: String?,
    val results: List<T>
)
