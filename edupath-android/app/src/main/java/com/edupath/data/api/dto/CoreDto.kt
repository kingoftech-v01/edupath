package com.edupath.data.api.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

/**
 * Data transfer object for blog post information.
 *
 * @property id Unique blog post identifier
 * @property title Blog post title
 * @property slug URL-friendly unique identifier
 * @property name Short name for the post
 * @property content Full HTML content of the blog post
 * @property excerpt Short preview/summary text
 * @property img URL to featured image
 * @property readTimeMinutes Estimated reading time in minutes
 * @property publishDate ISO date string of publication
 * @property author The blog post author (uses InstructorDto)
 * @property isActive Whether post is publicly visible
 */
@JsonClass(generateAdapter = true)
data class BlogDto(
    val id: Int,
    val title: String,
    val slug: String,
    val name: String = "",
    val content: String = "",
    val excerpt: String = "",
    val img: String? = null,
    @Json(name = "read_time_minutes") val readTimeMinutes: Int = 5,
    @Json(name = "publish_date") val publishDate: String? = null,
    val author: InstructorDto? = null,
    @Json(name = "is_active") val isActive: Boolean = true
)

/**
 * Aggregated data for the homepage.
 *
 * Contains all the data needed to render the homepage in a single API call.
 *
 * @property features List of platform feature highlights
 * @property businessPartners List of business partner logos
 * @property categories Course categories for navigation
 * @property featuredCourses Highlighted courses to display
 * @property instructors Featured instructors
 * @property reviews Customer testimonials
 * @property statistics Platform statistics (students, courses, etc.)
 * @property recentBlogs Most recent blog posts
 */
@JsonClass(generateAdapter = true)
data class HomepageDataDto(
    val features: List<FeatureDto> = emptyList(),
    @Json(name = "business_partners") val businessPartners: List<BusinessPartnerDto> = emptyList(),
    val categories: List<CategoryDto> = emptyList(),
    @Json(name = "featured_courses") val featuredCourses: List<CourseDto> = emptyList(),
    val instructors: List<InstructorDto> = emptyList(),
    val reviews: List<ReviewDto> = emptyList(),
    val statistics: List<StatisticDto> = emptyList(),
    @Json(name = "recent_blogs") val recentBlogs: List<BlogDto> = emptyList()
)

/**
 * Data transfer object for platform feature highlights.
 *
 * @property id Unique feature identifier
 * @property icon Icon identifier for the feature
 * @property title Feature title
 * @property desc Feature description
 * @property linkUrl Optional URL for "Learn more" link
 */
@JsonClass(generateAdapter = true)
data class FeatureDto(
    val id: Int,
    val icon: String,
    val title: String,
    val desc: String,
    @Json(name = "link_url") val linkUrl: String = ""
)

/**
 * Data transfer object for business partner/sponsor information.
 *
 * @property id Unique partner identifier
 * @property name Partner company name
 * @property img URL to partner logo image
 * @property websiteUrl Partner's website URL
 */
@JsonClass(generateAdapter = true)
data class BusinessPartnerDto(
    val id: Int,
    val name: String,
    val img: String,
    @Json(name = "website_url") val websiteUrl: String = ""
)

/**
 * Data transfer object for platform statistics.
 *
 * Used for animated counter displays on the homepage.
 *
 * @property id Unique statistic identifier
 * @property title Statistic label (e.g., "Students Enrolled")
 * @property number Current value to display
 * @property target Target/goal value for progress indicators
 * @property symbol Symbol to append (e.g., "+", "%", "K")
 */
@JsonClass(generateAdapter = true)
data class StatisticDto(
    val id: Int,
    val title: String,
    val number: Int = 0,
    val target: Int = 0,
    val symbol: String = "+"
)

/**
 * Data transfer object for site-wide configuration.
 *
 * Contains branding, contact information, and social media links.
 *
 * @property siteName Platform name
 * @property tagline Platform tagline/slogan
 * @property email Contact email address
 * @property phone Contact phone number
 * @property address Physical address
 * @property facebookUrl Facebook page URL
 * @property twitterUrl Twitter profile URL
 * @property instagramUrl Instagram profile URL
 * @property linkedinUrl LinkedIn page URL
 * @property youtubeUrl YouTube channel URL
 */
@JsonClass(generateAdapter = true)
data class SiteConfigDto(
    @Json(name = "site_name") val siteName: String = "EduPath",
    val tagline: String = "",
    val email: String = "",
    val phone: String = "",
    val address: String = "",
    @Json(name = "facebook_url") val facebookUrl: String = "",
    @Json(name = "twitter_url") val twitterUrl: String = "",
    @Json(name = "instagram_url") val instagramUrl: String = "",
    @Json(name = "linkedin_url") val linkedinUrl: String = "",
    @Json(name = "youtube_url") val youtubeUrl: String = ""
)

/**
 * Request body for contact form submission.
 *
 * @property name Sender's full name
 * @property email Sender's email address
 * @property subject Message subject line
 * @property message Message body content
 */
@JsonClass(generateAdapter = true)
data class ContactDto(
    val name: String,
    val email: String,
    val subject: String,
    val message: String
)
