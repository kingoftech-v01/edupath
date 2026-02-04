package com.edupath.data.local.dao

import androidx.room.*
import com.edupath.data.local.entities.CategoryEntity
import kotlinx.coroutines.flow.Flow

/**
 * Data Access Object for category-related database operations.
 *
 * Provides methods for querying, inserting, updating, and deleting
 * categories in the local SQLite database. Uses Kotlin Flow for
 * reactive data streams.
 */
@Dao
interface CategoryDao {

    /**
     * Gets all active categories ordered alphabetically by name.
     *
     * @return Flow emitting list of categories that updates on database changes
     */
    @Query("SELECT * FROM categories WHERE isActive = 1 ORDER BY name ASC")
    fun getAllCategories(): Flow<List<CategoryEntity>>

    /**
     * Gets a specific category by its URL slug.
     *
     * @param slug Unique category identifier
     * @return The category entity or null if not found
     */
    @Query("SELECT * FROM categories WHERE slug = :slug LIMIT 1")
    suspend fun getCategoryBySlug(slug: String): CategoryEntity?

    /**
     * Inserts or replaces multiple categories.
     *
     * @param categories List of categories to insert/replace
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(categories: List<CategoryEntity>)

    /**
     * Inserts or replaces a single category.
     *
     * @param category Category to insert/replace
     */
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(category: CategoryEntity)

    /**
     * Deletes a specific category.
     *
     * @param category Category to delete
     */
    @Delete
    suspend fun delete(category: CategoryEntity)

    /**
     * Deletes all categories from the database.
     */
    @Query("DELETE FROM categories")
    suspend fun deleteAll()
}
