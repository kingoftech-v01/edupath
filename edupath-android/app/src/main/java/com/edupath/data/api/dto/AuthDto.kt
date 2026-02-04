package com.edupath.data.api.dto

import com.squareup.moshi.Json
import com.squareup.moshi.JsonClass

/**
 * Request body for user login.
 *
 * @property username The user's username or email
 * @property password The user's password
 */
@JsonClass(generateAdapter = true)
data class LoginRequest(
    val username: String,
    val password: String
)

/**
 * Response containing JWT tokens after successful authentication.
 *
 * @property access The access token for API requests (short-lived)
 * @property refresh The refresh token for obtaining new access tokens (long-lived)
 */
@JsonClass(generateAdapter = true)
data class AuthResponse(
    val access: String,
    val refresh: String? = null
)

/**
 * Request body for refreshing an expired access token.
 *
 * @property refresh The refresh token to exchange for a new access token
 */
@JsonClass(generateAdapter = true)
data class RefreshTokenRequest(
    val refresh: String
)

/**
 * Generic response containing a message.
 *
 * Used for success/error responses from various endpoints.
 *
 * @property message The response message
 */
@JsonClass(generateAdapter = true)
data class MessageResponse(
    val message: String
)
