package com.edupath.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Room entity representing a cached course in the local database.
 *
 * This entity stores course data locally for offline access.
 * The data is synced from the API and includes denormalized
 * category and instructor information for efficient querying.
 *
 * @property id Unique course identifier (primary key)
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
 * @property categoryName Denormalized category name for display
 * @property instructorId Associated instructor ID
 * @property instructorName Denormalized instructor name for display
 * @property isFeatured Whether course is featured
 * @property isActive Whether course is publicly visible
 * @property cachedAt Timestamp when cached (for cache invalidation)
 */
@Entity(tableName = "courses")
data class CourseEntity(
    @PrimaryKey val id: Int,
    val title: String,
    val slug: String,
    val name: String,
    val desc: String,
    val price: String,
    val isFree: Boolean,
    val img: String?,
    val videoUrl: String,
    val lessons: Int,
    val students: Int,
    val durationHours: Int,
    val categoryId: Int?,
    val categoryName: String?,
    val instructorId: Int?,
    val instructorName: String?,
    val isFeatured: Boolean,
    val isActive: Boolean,
    val cachedAt: Long = System.currentTimeMillis()
)
