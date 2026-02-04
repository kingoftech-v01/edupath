# Edupath API Specification

**Version**: 1.0
**Last Updated**: 2026-01-28
**Base URL**: `https://api.edupath.com/api/v1/`

---

## Table of Contents

1. [Overview](#1-overview)
2. [Authentication](#2-authentication)
3. [Common Patterns](#3-common-patterns)
4. [Endpoints](#4-endpoints)
5. [Error Handling](#5-error-handling)
6. [Rate Limiting](#6-rate-limiting)
7. [Versioning](#7-versioning)

---

## 1. Overview

### 1.1 API Design Principles

- **RESTful**: Standard HTTP methods (GET, POST, PUT, PATCH, DELETE)
- **JSON**: All requests and responses use JSON format
- **Pagination**: List endpoints use cursor-based pagination
- **Filtering**: Support for query parameters
- **Versioning**: URL-based versioning (`/api/v1/`)

### 1.2 Supported Platforms

| Platform | Implementation |
|----------|----------------|
| Web | Django REST Framework |
| Mobile | Retrofit (Android) |
| Desktop | Tauri HTTP Client |

### 1.3 Base URLs

| Environment | URL |
|-------------|-----|
| Production | `https://api.edupath.com/api/v1/` |
| Staging | `https://staging-api.edupath.com/api/v1/` |
| Development | `http://localhost:8000/api/v1/` |

---

## 2. Authentication

### 2.1 Authentication Methods

| Method | Use Case | Header |
|--------|----------|--------|
| Token | Mobile/Desktop | `Authorization: Token <token>` |
| Session | Web Browser | Cookie-based |
| JWT | API-only clients | `Authorization: Bearer <token>` |

### 2.2 Login

**Endpoint**: `POST /auth/login/`

**Request**:
```json
{
  "username": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**Error** (401 Unauthorized):
```json
{
  "error": "invalid_credentials",
  "message": "Unable to log in with provided credentials."
}
```

### 2.3 Logout

**Endpoint**: `POST /auth/logout/`

**Headers**:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response** (200 OK):
```json
{
  "message": "Successfully logged out."
}
```

### 2.4 Token Refresh

**Endpoint**: `POST /auth/token/refresh/`

**Request**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response** (200 OK):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2.5 Registration

**Endpoint**: `POST /auth/register/`

**Request**:
```json
{
  "username": "johndoe",
  "email": "user@example.com",
  "password1": "securepassword123",
  "password2": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "user@example.com",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

---

## 3. Common Patterns

### 3.1 Request Headers

All authenticated requests must include:

```http
Authorization: Token <token>
Content-Type: application/json
Accept: application/json
X-Platform: web|mobile|desktop
X-App-Version: 1.0.0
```

### 3.2 Pagination

**Request**:
```
GET /courses/?page=2&page_size=20
```

**Response**:
```json
{
  "count": 150,
  "next": "https://api.edupath.com/api/v1/courses/?page=3",
  "previous": "https://api.edupath.com/api/v1/courses/?page=1",
  "results": [
    { "id": 21, "title": "Course 21" },
    { "id": 22, "title": "Course 22" }
  ]
}
```

### 3.3 Filtering

**Query Parameters**:
```
GET /courses/?category=programming&level=beginner&ordering=-created_at
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category slug |
| `level` | string | Filter by level (beginner, intermediate, advanced) |
| `instructor` | integer | Filter by instructor ID |
| `search` | string | Full-text search |
| `ordering` | string | Sort field (prefix `-` for descending) |

### 3.4 Response Format

**Success Response**:
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "description": "Learn Python basics",
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-20T14:45:00Z"
}
```

**List Response**:
```json
{
  "count": 100,
  "next": "https://api.edupath.com/api/v1/courses/?page=2",
  "previous": null,
  "results": [...]
}
```

**Error Response**:
```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": {
    "email": ["Enter a valid email address."],
    "password": ["Password must be at least 10 characters."]
  }
}
```

---

## 4. Endpoints

### 4.1 Courses

#### List Courses

**Endpoint**: `GET /courses/`

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number |
| `page_size` | integer | 12 | Items per page (max 100) |
| `category` | string | - | Category slug |
| `level` | string | - | Difficulty level |
| `search` | string | - | Search query |
| `ordering` | string | `-created_at` | Sort order |

**Response** (200 OK):
```json
{
  "count": 50,
  "next": "https://api.edupath.com/api/v1/courses/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "slug": "introduction-to-python",
      "description": "Learn Python programming from scratch",
      "short_description": "Python basics for beginners",
      "thumbnail": "https://cdn.edupath.com/courses/python-intro.jpg",
      "category": {
        "id": 1,
        "name": "Programming",
        "slug": "programming"
      },
      "instructor": {
        "id": 1,
        "name": "Jane Smith",
        "avatar": "https://cdn.edupath.com/instructors/jane.jpg"
      },
      "level": "beginner",
      "duration_hours": 10,
      "lessons_count": 25,
      "students_count": 1500,
      "rating": 4.8,
      "reviews_count": 120,
      "price": "49.99",
      "is_free": false,
      "is_featured": true,
      "created_at": "2026-01-10T08:00:00Z"
    }
  ]
}
```

#### Get Course Details

**Endpoint**: `GET /courses/{id}/`

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "slug": "introduction-to-python",
  "description": "Full course description with HTML formatting...",
  "short_description": "Python basics for beginners",
  "thumbnail": "https://cdn.edupath.com/courses/python-intro.jpg",
  "preview_video": "https://cdn.edupath.com/videos/python-preview.mp4",
  "category": {
    "id": 1,
    "name": "Programming",
    "slug": "programming"
  },
  "instructor": {
    "id": 1,
    "name": "Jane Smith",
    "bio": "Senior Python developer with 10 years experience",
    "avatar": "https://cdn.edupath.com/instructors/jane.jpg"
  },
  "level": "beginner",
  "duration_hours": 10,
  "lessons_count": 25,
  "students_count": 1500,
  "rating": 4.8,
  "reviews_count": 120,
  "price": "49.99",
  "is_free": false,
  "is_enrolled": false,
  "requirements": [
    "Basic computer knowledge",
    "No programming experience required"
  ],
  "what_you_learn": [
    "Python syntax and fundamentals",
    "Object-oriented programming",
    "Working with files and databases"
  ],
  "sections": [
    {
      "id": 1,
      "title": "Getting Started",
      "order": 1,
      "lessons": [
        {
          "id": 1,
          "title": "Installing Python",
          "type": "video",
          "duration_minutes": 15,
          "is_preview": true,
          "is_completed": false
        },
        {
          "id": 2,
          "title": "Your First Program",
          "type": "video",
          "duration_minutes": 20,
          "is_preview": false,
          "is_completed": false
        }
      ]
    }
  ],
  "created_at": "2026-01-10T08:00:00Z",
  "updated_at": "2026-01-25T16:30:00Z"
}
```

#### Get Course Progress

**Endpoint**: `GET /courses/{id}/progress/`

**Headers**: `Authorization: Token <token>` (required)

**Response** (200 OK):
```json
{
  "course_id": 1,
  "user_id": 42,
  "progress_percentage": 45,
  "completed_lessons": 11,
  "total_lessons": 25,
  "last_accessed_lesson": {
    "id": 12,
    "title": "Working with Lists",
    "section_id": 2
  },
  "completed_lesson_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  "started_at": "2026-01-15T10:00:00Z",
  "last_activity_at": "2026-01-28T14:30:00Z"
}
```

#### Update Lesson Progress

**Endpoint**: `POST /courses/{id}/lessons/{lesson_id}/complete/`

**Headers**: `Authorization: Token <token>` (required)

**Request**:
```json
{
  "completed": true,
  "progress_seconds": 900
}
```

**Response** (200 OK):
```json
{
  "lesson_id": 12,
  "completed": true,
  "progress_seconds": 900,
  "course_progress_percentage": 48
}
```

### 4.2 Categories

#### List Categories

**Endpoint**: `GET /courses/categories/`

**Response** (200 OK):
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "name": "Programming",
      "slug": "programming",
      "description": "Learn programming languages",
      "icon": "code",
      "courses_count": 25,
      "order": 1
    },
    {
      "id": 2,
      "name": "Design",
      "slug": "design",
      "description": "UI/UX and graphic design",
      "icon": "palette",
      "courses_count": 15,
      "order": 2
    }
  ]
}
```

### 4.3 User Account

#### Get Profile

**Endpoint**: `GET /accounts/profile/`

**Headers**: `Authorization: Token <token>` (required)

**Response** (200 OK):
```json
{
  "id": 42,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "avatar": "https://cdn.edupath.com/avatars/john.jpg",
  "bio": "Passionate learner",
  "date_joined": "2025-06-15T08:00:00Z",
  "enrolled_courses_count": 5,
  "completed_courses_count": 2,
  "total_learning_hours": 45,
  "preferences": {
    "email_notifications": true,
    "push_notifications": true,
    "dark_mode": false,
    "language": "en"
  }
}
```

#### Update Profile

**Endpoint**: `PATCH /accounts/profile/`

**Headers**: `Authorization: Token <token>` (required)

**Request**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Passionate learner and developer"
}
```

**Response** (200 OK):
```json
{
  "id": 42,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Passionate learner and developer"
}
```

#### Get Enrolled Courses

**Endpoint**: `GET /accounts/enrolled-courses/`

**Headers**: `Authorization: Token <token>` (required)

**Response** (200 OK):
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "course": {
        "id": 1,
        "title": "Introduction to Python",
        "thumbnail": "https://cdn.edupath.com/courses/python-intro.jpg"
      },
      "progress_percentage": 45,
      "enrolled_at": "2026-01-15T10:00:00Z",
      "last_activity_at": "2026-01-28T14:30:00Z"
    }
  ]
}
```

### 4.4 Blog

#### List Posts

**Endpoint**: `GET /blog/`

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Category slug |
| `tag` | string | Tag slug |
| `search` | string | Search query |

**Response** (200 OK):
```json
{
  "count": 30,
  "next": "https://api.edupath.com/api/v1/blog/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "10 Tips for Learning Programming",
      "slug": "10-tips-learning-programming",
      "excerpt": "Start your programming journey with these tips...",
      "featured_image": "https://cdn.edupath.com/blog/tips.jpg",
      "author": {
        "id": 1,
        "name": "Jane Smith"
      },
      "category": {
        "id": 1,
        "name": "Tips",
        "slug": "tips"
      },
      "tags": [
        {"id": 1, "name": "Programming", "slug": "programming"},
        {"id": 2, "name": "Beginners", "slug": "beginners"}
      ],
      "published_at": "2026-01-20T10:00:00Z",
      "reading_time_minutes": 5
    }
  ]
}
```

#### Get Post Details

**Endpoint**: `GET /blog/{slug}/`

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "10 Tips for Learning Programming",
  "slug": "10-tips-learning-programming",
  "content": "<p>Full HTML content...</p>",
  "excerpt": "Start your programming journey with these tips...",
  "featured_image": "https://cdn.edupath.com/blog/tips.jpg",
  "author": {
    "id": 1,
    "name": "Jane Smith",
    "avatar": "https://cdn.edupath.com/authors/jane.jpg",
    "bio": "Senior developer and educator"
  },
  "category": {
    "id": 1,
    "name": "Tips",
    "slug": "tips"
  },
  "tags": [
    {"id": 1, "name": "Programming", "slug": "programming"}
  ],
  "published_at": "2026-01-20T10:00:00Z",
  "updated_at": "2026-01-22T14:00:00Z",
  "reading_time_minutes": 5,
  "views_count": 1500,
  "related_posts": [
    {
      "id": 2,
      "title": "Best Programming Languages in 2026",
      "slug": "best-programming-languages-2026",
      "featured_image": "https://cdn.edupath.com/blog/languages.jpg"
    }
  ]
}
```

### 4.5 Core Configuration

#### Get Site Configuration

**Endpoint**: `GET /core/config/`

**Response** (200 OK):
```json
{
  "site_name": "Edupath",
  "tagline": "Learn. Grow. Succeed.",
  "logo_url": "https://cdn.edupath.com/logo.png",
  "support_email": "support@edupath.com",
  "social_links": {
    "facebook": "https://facebook.com/edupath",
    "twitter": "https://twitter.com/edupath",
    "linkedin": "https://linkedin.com/company/edupath"
  },
  "features": {
    "registration_enabled": true,
    "social_login_enabled": true,
    "offline_mode_enabled": true
  },
  "app_versions": {
    "android_min": "1.0.0",
    "android_latest": "1.2.0",
    "desktop_min": "1.0.0",
    "desktop_latest": "1.1.0"
  }
}
```

---

## 5. Error Handling

### 5.1 Error Response Format

All errors follow this format:

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {}
}
```

### 5.2 Error Codes

| HTTP Status | Error Code | Description |
|-------------|------------|-------------|
| 400 | `validation_error` | Invalid input data |
| 400 | `bad_request` | Malformed request |
| 401 | `authentication_required` | No authentication provided |
| 401 | `invalid_token` | Token is invalid or expired |
| 401 | `invalid_credentials` | Wrong username/password |
| 403 | `permission_denied` | Not allowed to perform action |
| 404 | `not_found` | Resource not found |
| 405 | `method_not_allowed` | HTTP method not allowed |
| 409 | `conflict` | Resource conflict (duplicate) |
| 422 | `unprocessable_entity` | Semantic errors |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Server error |
| 503 | `service_unavailable` | Service temporarily down |

### 5.3 Validation Error Example

```json
{
  "error": "validation_error",
  "message": "Invalid input data",
  "details": {
    "email": [
      "Enter a valid email address."
    ],
    "password": [
      "Password must be at least 10 characters.",
      "Password cannot be entirely numeric."
    ]
  }
}
```

### 5.4 Platform-Specific Error Handling

#### Web (JavaScript/TypeScript)

```typescript
try {
  const response = await api.post('/auth/login/', credentials);
  return response.data;
} catch (error) {
  if (error.response?.status === 401) {
    // Handle authentication error
    showError(error.response.data.message);
  } else if (error.response?.status === 422) {
    // Handle validation errors
    setFieldErrors(error.response.data.details);
  } else {
    // Handle other errors
    showError('An unexpected error occurred');
  }
}
```

#### Android (Kotlin)

```kotlin
sealed class ApiResult<out T> {
    data class Success<T>(val data: T) : ApiResult<T>()
    data class Error(val code: String, val message: String) : ApiResult<Nothing>()
}

suspend fun <T> safeApiCall(call: suspend () -> Response<T>): ApiResult<T> {
    return try {
        val response = call()
        if (response.isSuccessful) {
            ApiResult.Success(response.body()!!)
        } else {
            val error = parseError(response.errorBody())
            ApiResult.Error(error.code, error.message)
        }
    } catch (e: Exception) {
        ApiResult.Error("network_error", e.message ?: "Network error")
    }
}
```

#### Desktop (Rust/Tauri)

```rust
#[derive(Debug, Deserialize)]
pub struct ApiError {
    pub error: String,
    pub message: String,
    pub details: Option<HashMap<String, Vec<String>>>,
}

pub async fn handle_response<T: DeserializeOwned>(
    response: Response
) -> Result<T, ApiError> {
    if response.status().is_success() {
        response.json::<T>().await.map_err(|e| ApiError {
            error: "parse_error".to_string(),
            message: e.to_string(),
            details: None,
        })
    } else {
        let error = response.json::<ApiError>().await?;
        Err(error)
    }
}
```

---

## 6. Rate Limiting

### 6.1 Rate Limits

| User Type | Limit | Window |
|-----------|-------|--------|
| Anonymous | 100 requests | 1 hour |
| Authenticated | 1000 requests | 1 hour |
| Premium | 5000 requests | 1 hour |

### 6.2 Rate Limit Headers

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 950
X-RateLimit-Reset: 1706500000
```

### 6.3 Rate Limit Exceeded Response

**Status**: 429 Too Many Requests

```json
{
  "error": "rate_limit_exceeded",
  "message": "Request was throttled. Expected available in 3600 seconds.",
  "retry_after": 3600
}
```

---

## 7. Versioning

### 7.1 API Versioning Strategy

- URL-based versioning: `/api/v1/`, `/api/v2/`
- Major versions for breaking changes
- Minor versions handled within endpoints

### 7.2 Deprecation Policy

1. Deprecated endpoints return `X-API-Deprecated: true` header
2. Deprecation notice sent 6 months before removal
3. Migration guide provided in documentation

### 7.3 Version Headers

```http
X-API-Version: 1.0
X-API-Deprecated: false
X-API-Min-Client-Version: 1.0.0
```

---

## Appendix A: Data Types

### Common Fields

| Field | Type | Format | Example |
|-------|------|--------|---------|
| `id` | integer | - | `42` |
| `created_at` | string | ISO 8601 | `2026-01-28T10:30:00Z` |
| `updated_at` | string | ISO 8601 | `2026-01-28T14:45:00Z` |
| `slug` | string | lowercase, hyphens | `introduction-to-python` |
| `email` | string | email format | `user@example.com` |
| `url` | string | URL format | `https://example.com/image.jpg` |
| `price` | string | decimal | `"49.99"` |
| `duration_minutes` | integer | - | `15` |
| `percentage` | integer | 0-100 | `75` |

### Enumerations

**Course Level**:
- `beginner`
- `intermediate`
- `advanced`

**Lesson Type**:
- `video`
- `text`
- `quiz`
- `assignment`

**Notification Type**:
- `course_update`
- `new_lesson`
- `promotion`
- `system`

---

## Appendix B: SDK Examples

### Web (TypeScript/Axios)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://api.edupath.com/api/v1/',
  headers: {
    'Content-Type': 'application/json',
    'X-Platform': 'web',
  },
});

// Add auth interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Usage
const courses = await api.get('/courses/');
```

### Android (Kotlin/Retrofit)

```kotlin
interface EdupathApi {
    @GET("courses/")
    suspend fun getCourses(
        @Query("page") page: Int = 1,
        @Query("category") category: String? = null
    ): Response<PaginatedResponse<Course>>

    @GET("courses/{id}/")
    suspend fun getCourse(@Path("id") id: Int): Response<CourseDetail>

    @POST("auth/login/")
    suspend fun login(@Body credentials: LoginRequest): Response<LoginResponse>
}
```

### Desktop (Rust)

```rust
use reqwest::Client;
use serde::{Deserialize, Serialize};

pub struct EdupathClient {
    client: Client,
    base_url: String,
    token: Option<String>,
}

impl EdupathClient {
    pub async fn get_courses(&self, page: u32) -> Result<PaginatedResponse<Course>, Error> {
        let url = format!("{}/courses/?page={}", self.base_url, page);
        let response = self.client
            .get(&url)
            .header("Authorization", format!("Token {}", self.token.as_ref().unwrap()))
            .send()
            .await?;
        response.json().await
    }
}
```

---

**This API specification is shared across all Edupath platforms.**

*Last updated: 2026-01-28*
