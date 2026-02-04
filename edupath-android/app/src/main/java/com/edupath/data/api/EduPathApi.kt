package com.edupath.data.api

import com.edupath.data.api.dto.*
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit API interface for EduPath backend.
 *
 * This interface defines all the REST API endpoints used by the EduPath Android app
 * to communicate with the Django backend. All methods are suspend functions for
 * coroutine-based async execution.
 *
 * Endpoints are organized by feature:
 * - Authentication: Login, token refresh
 * - User: Profile management
 * - Courses: Course listing, details, filtering
 * - Categories: Course categories
 * - Instructors: Course instructors
 * - Reviews: Course reviews
 * - Blog: Blog posts
 * - Core: Homepage data, site configuration, contact
 */
interface EduPathApi {

    // ==================== Authentication ====================

    /**
     * Authenticates a user with username and password.
     *
     * @param credentials Login credentials containing username and password
     * @return Response containing access and refresh JWT tokens
     */
    @POST("accounts/api/v1/auth/login/")
    suspend fun login(@Body credentials: LoginRequest): Response<AuthResponse>

    /**
     * Refreshes an expired access token using the refresh token.
     *
     * @param request Request containing the refresh token
     * @return Response containing new access token
     */
    @POST("accounts/api/v1/auth/token/refresh/")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<AuthResponse>

    // ==================== User ====================

    /**
     * Gets the currently authenticated user's basic information.
     *
     * @return Response containing user data
     */
    @GET("accounts/api/v1/me/")
    suspend fun getCurrentUser(): Response<UserDto>

    /**
     * Gets the current user's profile details.
     *
     * @return Response containing profile data including bio, social links, etc.
     */
    @GET("accounts/api/v1/profiles/me/")
    suspend fun getUserProfile(): Response<UserProfileDto>

    /**
     * Updates the current user's profile.
     *
     * @param profile Updated profile data
     * @return Response containing the updated profile
     */
    @PATCH("accounts/api/v1/profiles/me/")
    suspend fun updateProfile(@Body profile: UserProfileDto): Response<UserProfileDto>

    // ==================== Courses ====================

    /**
     * Gets a paginated list of courses with optional filtering.
     *
     * @param category Filter by category slug
     * @param search Search query for course title/description
     * @param isFree Filter for free courses only
     * @param page Page number for pagination
     * @return Paginated response containing course list
     */
    @GET("courses/api/v1/courses/")
    suspend fun getCourses(
        @Query("category__slug") category: String? = null,
        @Query("search") search: String? = null,
        @Query("is_free") isFree: Boolean? = null,
        @Query("page") page: Int = 1
    ): Response<PaginatedResponse<CourseDto>>

    /**
     * Gets detailed information for a specific course.
     *
     * @param slug Unique course identifier
     * @return Response containing course details
     */
    @GET("courses/api/v1/courses/{slug}/")
    suspend fun getCourse(@Path("slug") slug: String): Response<CourseDto>

    /**
     * Gets the list of featured courses for homepage display.
     *
     * @return List of featured courses
     */
    @GET("courses/api/v1/courses/featured/")
    suspend fun getFeaturedCourses(): Response<List<CourseDto>>

    /**
     * Gets the list of free courses.
     *
     * @return List of free courses
     */
    @GET("courses/api/v1/courses/free/")
    suspend fun getFreeCourses(): Response<List<CourseDto>>

    /**
     * Gets courses related to a specific course.
     *
     * @param slug Course slug to find related courses for
     * @return List of related courses
     */
    @GET("courses/api/v1/courses/{slug}/related/")
    suspend fun getRelatedCourses(@Path("slug") slug: String): Response<List<CourseDto>>

    // ==================== Categories ====================

    /**
     * Gets a paginated list of course categories.
     *
     * @return Paginated response containing category list
     */
    @GET("courses/api/v1/categories/")
    suspend fun getCategories(): Response<PaginatedResponse<CategoryDto>>

    /**
     * Gets details for a specific category.
     *
     * @param slug Unique category identifier
     * @return Response containing category details
     */
    @GET("courses/api/v1/categories/{slug}/")
    suspend fun getCategory(@Path("slug") slug: String): Response<CategoryDto>

    // ==================== Instructors ====================

    /**
     * Gets a paginated list of instructors.
     *
     * @return Paginated response containing instructor list
     */
    @GET("courses/api/v1/instructors/")
    suspend fun getInstructors(): Response<PaginatedResponse<InstructorDto>>

    /**
     * Gets details for a specific instructor.
     *
     * @param slug Unique instructor identifier
     * @return Response containing instructor details
     */
    @GET("courses/api/v1/instructors/{slug}/")
    suspend fun getInstructor(@Path("slug") slug: String): Response<InstructorDto>

    // ==================== Reviews ====================

    /**
     * Gets reviews for a specific course.
     *
     * @param courseId ID of the course to get reviews for
     * @return Paginated response containing review list
     */
    @GET("courses/api/v1/reviews/")
    suspend fun getReviews(@Query("course") courseId: Int): Response<PaginatedResponse<ReviewDto>>

    /**
     * Submits a new review for a course.
     *
     * @param review Review data including rating and description
     * @return Response containing the created review
     */
    @POST("courses/api/v1/reviews/")
    suspend fun submitReview(@Body review: ReviewCreateDto): Response<ReviewDto>

    // ==================== Blog ====================

    /**
     * Gets a paginated list of blog posts.
     *
     * @return Paginated response containing blog post list
     */
    @GET("blog/api/v1/posts/")
    suspend fun getBlogPosts(): Response<PaginatedResponse<BlogDto>>

    /**
     * Gets a specific blog post by slug.
     *
     * @param slug Unique blog post identifier
     * @return Response containing blog post details
     */
    @GET("blog/api/v1/posts/{slug}/")
    suspend fun getBlogPost(@Path("slug") slug: String): Response<BlogDto>

    /**
     * Gets the most recent blog posts.
     *
     * @return List of recent blog posts
     */
    @GET("blog/api/v1/posts/recent/")
    suspend fun getRecentBlogPosts(): Response<List<BlogDto>>

    // ==================== Core ====================

    /**
     * Gets aggregated data for the homepage.
     *
     * Includes features, partners, categories, featured courses,
     * instructors, reviews, statistics, and recent blogs.
     *
     * @return Response containing all homepage data
     */
    @GET("core/api/v1/homepage/")
    suspend fun getHomepageData(): Response<HomepageDataDto>

    /**
     * Gets site configuration (name, contact info, social links).
     *
     * @return Response containing site configuration
     */
    @GET("core/api/v1/site-config/")
    suspend fun getSiteConfig(): Response<SiteConfigDto>

    /**
     * Submits a contact form message.
     *
     * @param contact Contact form data
     * @return Response containing success message
     */
    @POST("core/api/v1/contact/")
    suspend fun submitContact(@Body contact: ContactDto): Response<MessageResponse>
}
