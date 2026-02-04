package com.edupath.domain.model

/**
 * Domain model representing a course.
 *
 * @property id Unique course identifier
 * @property title Course display title
 * @property slug URL-friendly unique identifier
 * @property name Course short name
 * @property desc Course description
 * @property price Course price as string
 * @property isFree Whether the course is free
 * @property img URL to course thumbnail image
 * @property videoUrl URL to course intro video
 * @property lessons Number of lessons
 * @property students Number of enrolled students
 * @property durationHours Total duration in hours
 * @property categoryId Associated category ID
 * @property categoryName Category display name
 * @property instructorId Associated instructor ID
 * @property instructorName Instructor display name
 * @property isFeatured Whether course is featured
 */
data class Course(
    val id: Int,
    val title: String,
    val slug: String,
    val name: String = "",
    val desc: String,
    val price: String = "0.00",
    val isFree: Boolean = false,
    val img: String? = null,
    val videoUrl: String = "",
    val lessons: Int = 0,
    val students: Int = 0,
    val durationHours: Int = 0,
    val categoryId: Int? = null,
    val categoryName: String? = null,
    val instructorId: Int? = null,
    val instructorName: String? = null,
    val isFeatured: Boolean = false
) {
    /**
     * Returns formatted price string with currency symbol.
     * Shows "$0" for free courses.
     */
    val formattedPrice: String
        get() = if (isFree || price == "0.00") "$0" else "$$price"

    /**
     * Returns instructor name, falling back to course name if not set.
     */
    val instructorDisplayName: String
        get() = instructorName ?: name
}

/**
 * Domain model representing a course category.
 *
 * @property id Unique category identifier
 * @property name Category display name
 * @property slug URL-friendly unique identifier
 * @property icon Icon identifier
 * @property description Category description
 * @property courseCount Number of courses in this category
 */
data class Category(
    val id: Int,
    val name: String,
    val slug: String,
    val icon: String = "",
    val description: String = "",
    val courseCount: Int = 0
)

/**
 * Domain model representing a course instructor.
 *
 * @property id Unique instructor identifier
 * @property name Instructor's full name
 * @property slug URL-friendly unique identifier
 * @property title Professional title
 * @property bio Instructor biography
 * @property img URL to profile image
 * @property facebookUrl Facebook profile URL
 * @property instagramUrl Instagram profile URL
 * @property linkedinUrl LinkedIn profile URL
 * @property twitterUrl Twitter profile URL
 */
data class Instructor(
    val id: Int,
    val name: String,
    val slug: String,
    val title: String = "",
    val bio: String = "",
    val img: String? = null,
    val facebookUrl: String = "",
    val instagramUrl: String = "",
    val linkedinUrl: String = "",
    val twitterUrl: String = ""
)

/**
 * Domain model representing a course review.
 *
 * @property id Unique review identifier
 * @property name Reviewer's display name
 * @property title Reviewer's title
 * @property desc Review text content
 * @property rating Rating value (typically 1-5)
 * @property img URL to reviewer's avatar
 * @property courseId Associated course ID
 * @property userId Associated user ID
 */
data class Review(
    val id: Int,
    val name: String,
    val title: String = "Student",
    val desc: String,
    val rating: Int,
    val img: String? = null,
    val courseId: Int? = null,
    val userId: Int? = null
)
