package com.edupath.data.local.entities

import androidx.room.Entity
import androidx.room.PrimaryKey

/**
 * Room entity representing a cached category in the local database.
 *
 * This entity stores category data locally for offline access
 * and efficient filtering of courses.
 *
 * @property id Unique category identifier (primary key)
 * @property name Category display name
 * @property slug URL-friendly unique identifier
 * @property icon Icon identifier for the category
 * @property description Category description
 * @property courseCount Number of courses in this category
 * @property isActive Whether category is publicly visible
 * @property cachedAt Timestamp when cached (for cache invalidation)
 */
@Entity(tableName = "categories")
data class CategoryEntity(
    @PrimaryKey val id: Int,
    val name: String,
    val slug: String,
    val icon: String,
    val description: String,
    val courseCount: Int,
    val isActive: Boolean,
    val cachedAt: Long = System.currentTimeMillis()
)
