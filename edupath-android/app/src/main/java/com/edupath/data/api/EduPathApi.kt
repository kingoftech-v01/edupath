package com.edupath.data.api

import com.edupath.data.api.dto.*
import retrofit2.Response
import retrofit2.http.*

/** Retrofit API interface for EduPath Django backend. */
interface EduPathApi {

    // Auth
    @POST("accounts/api/v1/auth/login/")
    suspend fun login(@Body credentials: LoginRequest): Response<AuthResponse>

    @POST("accounts/api/v1/auth/token/refresh/")
    suspend fun refreshToken(@Body request: RefreshTokenRequest): Response<AuthResponse>

    // User
    @GET("accounts/api/v1/me/")
    suspend fun getCurrentUser(): Response<UserDto>

    @GET("accounts/api/v1/profiles/me/")
    suspend fun getUserProfile(): Response<UserProfileDto>

    @PATCH("accounts/api/v1/profiles/me/")
    suspend fun updateProfile(@Body profile: UserProfileDto): Response<UserProfileDto>

    // Courses
    @GET("courses/api/v1/courses/")
    suspend fun getCourses(
        @Query("category__slug") category: String? = null,
        @Query("search") search: String? = null,
        @Query("is_free") isFree: Boolean? = null,
        @Query("page") page: Int = 1
    ): Response<PaginatedResponse<CourseDto>>

    @GET("courses/api/v1/courses/{slug}/")
    suspend fun getCourse(@Path("slug") slug: String): Response<CourseDto>

    @GET("courses/api/v1/courses/featured/")
    suspend fun getFeaturedCourses(): Response<List<CourseDto>>

    @GET("courses/api/v1/courses/free/")
    suspend fun getFreeCourses(): Response<List<CourseDto>>

    @GET("courses/api/v1/courses/{slug}/related/")
    suspend fun getRelatedCourses(@Path("slug") slug: String): Response<List<CourseDto>>

    // Categories
    @GET("courses/api/v1/categories/")
    suspend fun getCategories(): Response<PaginatedResponse<CategoryDto>>

    @GET("courses/api/v1/categories/{slug}/")
    suspend fun getCategory(@Path("slug") slug: String): Response<CategoryDto>

    // Instructors
    @GET("courses/api/v1/instructors/")
    suspend fun getInstructors(): Response<PaginatedResponse<InstructorDto>>

    @GET("courses/api/v1/instructors/{slug}/")
    suspend fun getInstructor(@Path("slug") slug: String): Response<InstructorDto>

    // Reviews
    @GET("courses/api/v1/reviews/")
    suspend fun getReviews(@Query("course") courseId: Int): Response<PaginatedResponse<ReviewDto>>

    @POST("courses/api/v1/reviews/")
    suspend fun submitReview(@Body review: ReviewCreateDto): Response<ReviewDto>

    // Blog
    @GET("blog/api/v1/posts/")
    suspend fun getBlogPosts(): Response<PaginatedResponse<BlogDto>>

    @GET("blog/api/v1/posts/{slug}/")
    suspend fun getBlogPost(@Path("slug") slug: String): Response<BlogDto>

    @GET("blog/api/v1/posts/recent/")
    suspend fun getRecentBlogPosts(): Response<List<BlogDto>>

    // Core
    /** Aggregated homepage data: features, partners, courses, instructors, etc. */
    @GET("core/api/v1/homepage/")
    suspend fun getHomepageData(): Response<HomepageDataDto>

    @GET("core/api/v1/site-config/")
    suspend fun getSiteConfig(): Response<SiteConfigDto>

    @POST("core/api/v1/contact/")
    suspend fun submitContact(@Body contact: ContactDto): Response<MessageResponse>
}
