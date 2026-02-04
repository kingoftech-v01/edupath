# Edupath Development Conventions

**Version**: 3.0
**Last Updated**: 2026-01-28
**Status**: MANDATORY - All development MUST follow these conventions

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture & Structure](#2-architecture--structure)
3. [Naming Conventions](#3-naming-conventions)
4. [URL & View Conventions](#4-url--view-conventions)
5. [Security Standards](#5-security-standards)
6. [Scalability Guidelines](#6-scalability-guidelines)
7. [Code Documentation Standards](#7-code-documentation-standards)
8. [Testing Conventions](#8-testing-conventions)
9. [Git Workflow](#9-git-workflow)
10. [Environment Configuration](#10-environment-configuration)
11. [Error Handling](#11-error-handling)
12. [API Design Standards](#12-api-design-standards)
13. [Database Best Practices](#13-database-best-practices)
14. [Performance Optimization](#14-performance-optimization)

---

## 1. Project Overview

### 1.1 Platform Description

Edupath is a **multi-platform educational platform** consisting of:

| Platform | Technology | Repository |
|----------|------------|------------|
| Web | Django 5.x + DRF | `edupath-web` |
| Mobile | Kotlin/Android | `edupath-mobile` |
| Desktop | TBD (C#/.NET or Electron) | `edupath-desktop` |

### 1.2 Core Principles

1. **Security First** - Never compromise security for convenience
2. **Scalability** - Design for growth from day one
3. **Documentation** - Code without documentation is incomplete
4. **Consistency** - Follow conventions across all platforms
5. **Testability** - Write testable code with high coverage

### 1.3 Technology Stack (Web)

```
Backend:
- Python 3.11+
- Django 5.1.x
- Django REST Framework
- django-allauth (authentication)
- django-filter (query filtering)
- Celery (background tasks)

Frontend:
- Django Templates
- Tailwind CSS
- HTMX (dynamic interactions)
- Alpine.js (client-side reactivity)

Database:
- PostgreSQL (production)
- SQLite (development only)

Caching:
- Redis (sessions, cache, Celery broker)
```

---

## 2. Architecture & Structure

### 2.1 Dual-Layer Architecture

Edupath uses a **dual-layer pattern** separating concerns:

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                         │
├─────────────────────────┬───────────────────────────────┤
│   Browser (HTML/HTMX)   │   API Clients (JSON)          │
└─────────────────────────┴───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                      │
├─────────────────────────┬───────────────────────────────┤
│   views_frontend.py     │   views_api.py                │
│   (HTML templates)      │   (REST JSON)                 │
└─────────────────────────┴───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   BUSINESS LAYER                         │
├─────────────────────────────────────────────────────────┤
│   models.py | forms.py | serializers.py | services.py   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
├─────────────────────────────────────────────────────────┤
│   PostgreSQL | Redis | File Storage                      │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Django App Structure (MANDATORY)

Every Django app MUST follow this structure:

```
app_name/
├── __init__.py
├── README.md                # App documentation (REQUIRED)
├── models.py                # Database models
├── forms.py                 # Django forms
├── views_frontend.py        # Frontend HTML views
├── views_api.py             # API views (DRF ViewSets)
├── serializers.py           # DRF serializers
├── urls.py                  # URL configuration (both layers)
├── admin.py                 # Admin interface
├── permissions.py           # Custom permissions (if needed)
├── signals.py               # Signal handlers (if needed)
├── services.py              # Business logic (if complex)
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_api.py
├── templates/
│   └── app_name/
│       ├── list.html
│       ├── detail.html
│       └── form.html
└── migrations/
    └── __init__.py
```

### 2.3 Project Structure

```
edupath-web/
├── manage.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
├── CONVENTIONS.md           # This file
├── SECURITY.md
├── SCALABILITY.md
│
├── Edupath/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py          # Base settings
│   ├── settings_dev.py      # Development overrides
│   ├── settings_prod.py     # Production overrides
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                # User authentication & profiles
├── courses/                 # Courses, categories, reviews
├── blog/                    # Blog posts
├── core/                    # Site configuration, static pages
│
├── static/                  # Static files
├── media/                   # User uploads
├── templates/               # Global templates
│   ├── base.html
│   ├── partials/
│   └── components/
│
└── tests/                   # Project-level tests
    └── test_integration.py
```

---

## 3. Naming Conventions

### 3.1 File Naming

| Type | Convention | Example |
|------|------------|---------|
| Python files | `snake_case.py` | `views_frontend.py` |
| Templates | `snake_case.html` | `course_detail.html` |
| Static files | `kebab-case.*` | `main-styles.css` |
| Migrations | Auto-generated | `0001_initial.py` |

### 3.2 Code Naming

| Type | Convention | Example |
|------|------------|---------|
| Classes | `PascalCase` | `CourseViewSet` |
| Functions | `snake_case` | `get_course_list` |
| Variables | `snake_case` | `course_count` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_UPLOAD_SIZE` |
| Private | `_leading_underscore` | `_calculate_price` |

### 3.3 URL Naming

| Layer | URL Style | View Name Style | Example |
|-------|-----------|-----------------|---------|
| Frontend | `kebab-case` | `snake_case` | `/course-detail/` → `course_detail` |
| API | `kebab-case` | `kebab-case` | `/api/v1/courses/` → `course-list` |

### 3.4 Database Naming

| Type | Convention | Example |
|------|------------|---------|
| Table names | `app_modelname` | `courses_course` |
| Field names | `snake_case` | `created_at` |
| Foreign keys | `model_id` | `category_id` |
| Many-to-many | `model1_model2` | `course_tags` |

---

## 4. URL & View Conventions

### 4.1 URL Structure

```
# Frontend URLs (HTML responses)
/app-name/                           # List view
/app-name/create/                    # Create view
/app-name/<uuid:pk>/                 # Detail view
/app-name/<uuid:pk>/edit/            # Update view
/app-name/<uuid:pk>/delete/          # Delete view
/app-name/<uuid:pk>/action-name/     # Custom action

# API URLs (JSON responses)
/api/v1/app-name/                    # List/Create
/api/v1/app-name/<uuid:pk>/          # Retrieve/Update/Delete
/api/v1/app-name/<uuid:pk>/action/   # Custom action
```

### 4.2 Namespace Convention

All URLs use nested namespaces:

```python
# Format: layer:app:view_name
'frontend:courses:course_list'        # Frontend HTML view
'api:v1:courses:course-list'          # API endpoint

# Usage in templates
{% url 'frontend:courses:course_detail' pk=course.pk %}

# Usage in code
from django.urls import reverse
reverse('api:v1:courses:course-list')
```

### 4.3 urls.py Template (MANDATORY)

```python
"""
App Name URLs - Frontend and API routing.

URL Namespaces:
- Frontend: frontend:app_name:view_name
- API: api:v1:app_name:resource-name
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views_frontend
from . import views_api

# =============================================================================
# API ROUTER
# =============================================================================

api_router = DefaultRouter()
api_router.register(r'resources', views_api.ResourceViewSet, basename='resource')

api_urlpatterns = [
    path('', include(api_router.urls)),
]

# =============================================================================
# FRONTEND URLS
# =============================================================================

frontend_urlpatterns = [
    path('', views_frontend.resource_list, name='resource_list'),
    path('create/', views_frontend.resource_create, name='resource_create'),
    path('<uuid:pk>/', views_frontend.resource_detail, name='resource_detail'),
    path('<uuid:pk>/edit/', views_frontend.resource_update, name='resource_update'),
    path('<uuid:pk>/delete/', views_frontend.resource_delete, name='resource_delete'),
]

# =============================================================================
# APP URL CONFIGURATION
# =============================================================================

app_name = 'app_name'

urlpatterns = [
    path('api/', include((api_urlpatterns, 'api'))),
    path('', include((frontend_urlpatterns, 'frontend'))),
]
```

### 4.4 ViewSet Pattern

```python
"""
App Name API Views - REST API endpoints.

Provides CRUD operations via Django REST Framework ViewSets.
"""

from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Resource
from .serializers import ResourceSerializer, ResourceListSerializer
from .permissions import IsOwnerOrReadOnly


class ResourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Resource CRUD operations.

    Endpoints:
    - GET    /api/v1/app-name/resources/           List all
    - POST   /api/v1/app-name/resources/           Create new
    - GET    /api/v1/app-name/resources/{pk}/      Retrieve one
    - PUT    /api/v1/app-name/resources/{pk}/      Update (full)
    - PATCH  /api/v1/app-name/resources/{pk}/      Update (partial)
    - DELETE /api/v1/app-name/resources/{pk}/      Delete

    Filtering:
    - ?status=active
    - ?search=keyword
    - ?ordering=-created_at
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return queryset with optimized queries."""
        return Resource.objects.select_related('owner', 'category').all()

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return ResourceListSerializer
        return ResourceSerializer

    def perform_create(self, serializer):
        """Set owner to current user on create."""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        """
        Archive a resource.

        POST /api/v1/app-name/resources/{pk}/archive/
        """
        resource = self.get_object()
        resource.status = 'archived'
        resource.save(update_fields=['status'])
        return Response({'status': 'archived'})
```

---

## 5. Security Standards

**CRITICAL: Security is non-negotiable. All code MUST follow these standards.**

### 5.1 Environment Variables

**NEVER hardcode secrets in code.**

```python
# settings.py - CORRECT
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')

# WRONG - Never do this
SECRET_KEY = 'django-insecure-xxx'  # SECURITY VIOLATION
```

Required environment variables:
- `SECRET_KEY` - Django secret key (generate new for production)
- `DEBUG` - False in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DATABASE_URL` - Database connection string
- `CORS_ALLOWED_ORIGINS` - Allowed CORS origins

### 5.2 Authentication Security

```python
# settings.py

# Session security
SESSION_COOKIE_SECURE = True          # HTTPS only
SESSION_COOKIE_HTTPONLY = True        # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'       # CSRF protection
SESSION_COOKIE_AGE = 86400            # 24 hours

# CSRF security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='').split(',')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

### 5.3 Authorization

Every view MUST have explicit permission checks:

```python
# views_api.py
from rest_framework import permissions

class CourseViewSet(viewsets.ModelViewSet):
    # ALWAYS specify permission classes
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """Custom permissions based on action."""
        if self.action in ['create', 'update', 'destroy']:
            return [permissions.IsAuthenticated(), IsInstructorOrAdmin()]
        return super().get_permissions()
```

### 5.4 Input Validation

**ALWAYS validate user input:**

```python
# serializers.py
from rest_framework import serializers

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price']

    def validate_price(self, value):
        """Ensure price is positive."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        if value > 99999:
            raise serializers.ValidationError("Price exceeds maximum")
        return value

    def validate_title(self, value):
        """Sanitize title input."""
        # Remove potentially dangerous characters
        import bleach
        return bleach.clean(value, tags=[], strip=True)
```

### 5.5 CORS Configuration

```python
# settings.py

# Development
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # Only in development!
else:
    # Production - ALWAYS whitelist specific origins
    CORS_ALLOWED_ORIGINS = [
        "https://edupath.com",
        "https://www.edupath.com",
    ]
    CORS_ALLOW_CREDENTIALS = True
```

### 5.6 Security Headers

```python
# settings.py

# Security middleware (must be first)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ... other middleware
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings (production only)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 5.7 Database Security

```python
# CORRECT - Using ORM (parameterized queries)
Course.objects.filter(title__icontains=user_input)

# WRONG - Raw SQL with user input (SQL INJECTION RISK!)
cursor.execute(f"SELECT * FROM courses WHERE title LIKE '%{user_input}%'")

# If raw SQL is necessary, use parameterized queries
cursor.execute("SELECT * FROM courses WHERE title LIKE %s", [f'%{user_input}%'])
```

### 5.8 File Upload Security

```python
# settings.py
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

ALLOWED_UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']

# forms.py
def validate_file(file):
    """Validate uploaded file."""
    import os
    from django.core.exceptions import ValidationError

    # Check file size
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(f"File too large. Max size: {settings.MAX_UPLOAD_SIZE} bytes")

    # Check extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        raise ValidationError(f"File type not allowed: {ext}")

    # Validate file content matches extension
    import magic
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    # ... validate mime type matches extension
```

### 5.9 Rate Limiting

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/minute',  # Custom throttle for login
    },
}
```

See **SECURITY.md** for comprehensive security guidelines.

---

## 6. Scalability Guidelines

### 6.1 Database Optimization

```python
# models.py - Add indexes for filtered fields
class Course(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'status']),
        ]
```

### 6.2 Query Optimization

```python
# WRONG - N+1 query problem
courses = Course.objects.all()
for course in courses:
    print(course.instructor.name)  # Separate query for each course!

# CORRECT - Use select_related for ForeignKey
courses = Course.objects.select_related('instructor', 'category').all()

# CORRECT - Use prefetch_related for ManyToMany/reverse FK
courses = Course.objects.prefetch_related('reviews', 'tags').all()
```

### 6.3 Pagination

**ALWAYS paginate list endpoints:**

```python
# views_api.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Custom pagination
class CoursePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
```

### 6.4 Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# views.py - Cache expensive queries
from django.core.cache import cache

def get_course_stats():
    cache_key = 'course_stats'
    stats = cache.get(cache_key)
    if stats is None:
        stats = Course.objects.aggregate(
            total=Count('id'),
            avg_rating=Avg('reviews__rating'),
        )
        cache.set(cache_key, stats, timeout=3600)  # 1 hour
    return stats
```

### 6.5 Background Tasks

**Never block HTTP requests with long-running tasks:**

```python
# tasks.py
from celery import shared_task

@shared_task
def send_welcome_email(user_id):
    """Send welcome email asynchronously."""
    user = User.objects.get(id=user_id)
    # Send email...

# views.py
def register(request):
    user = User.objects.create(...)
    send_welcome_email.delay(user.id)  # Non-blocking
    return Response({'status': 'registered'})
```

See **SCALABILITY.md** for comprehensive scaling guidelines.

---

## 7. Code Documentation Standards

### 7.1 Module Docstrings (REQUIRED)

Every Python file MUST have a module docstring:

```python
"""
Courses Models - Database models for course management.

This module defines the data models for the courses app including:
- Category: Course categories with hierarchical support
- Instructor: Course instructors with profiles
- Course: Main course entity with all metadata
- Review: User reviews and ratings for courses

All models inherit from TimestampedModel for automatic timestamps.
"""

from django.db import models
```

### 7.2 Class Docstrings (REQUIRED)

```python
class Course(TimestampedModel):
    """
    Course model representing an educational course.

    A course belongs to a category and instructor, and can have
    multiple reviews. Courses can be free or paid.

    Attributes:
        title: Course title (max 200 chars)
        slug: URL-friendly identifier (auto-generated)
        description: Full course description (HTML allowed)
        price: Course price in USD (0 for free courses)
        instructor: ForeignKey to Instructor
        category: ForeignKey to Category
        is_published: Whether course is publicly visible
        video_url: Optional promotional video URL

    Properties:
        is_free: Returns True if price is 0
        review_count: Number of reviews
        average_rating: Average rating from reviews

    Example:
        >>> course = Course.objects.create(
        ...     title="Python Basics",
        ...     price=29.99,
        ...     instructor=instructor,
        ...     category=category
        ... )
        >>> course.is_free
        False
    """
```

### 7.3 Function Docstrings (REQUIRED for public functions)

```python
def calculate_course_progress(user, course):
    """
    Calculate user's progress in a course.

    Calculates the percentage of lessons completed by the user
    in the given course. Returns 0 if user hasn't started.

    Args:
        user: The User instance to check progress for.
        course: The Course instance to check.

    Returns:
        float: Progress percentage between 0.0 and 100.0.
            Returns 0.0 if no progress exists.

    Raises:
        ValueError: If user or course is None.
        Course.DoesNotExist: If course doesn't exist.

    Example:
        >>> progress = calculate_course_progress(user, course)
        >>> print(f"Progress: {progress}%")
        Progress: 75.0%
    """
    if user is None or course is None:
        raise ValueError("User and course are required")

    total_lessons = course.lessons.count()
    if total_lessons == 0:
        return 0.0

    completed = CompletedLesson.objects.filter(
        user=user,
        lesson__course=course
    ).count()

    return (completed / total_lessons) * 100
```

### 7.4 Inline Comments

```python
# GOOD - Explains WHY
# Using select_related to avoid N+1 queries when displaying course list
courses = Course.objects.select_related('instructor').all()

# BAD - Explains WHAT (obvious from code)
# Get all courses
courses = Course.objects.all()

# GOOD - Explains complex logic
# Calculate discount: 20% off for annual subscribers, capped at $50
if user.subscription == 'annual':
    discount = min(price * 0.20, 50.00)

# TODO format
# TODO(username): Add caching for expensive query - Issue #123
```

### 7.5 README Per Folder (REQUIRED)

Every app folder MUST have a README.md:

```markdown
# Courses App

Course management module for the Edupath platform.

## Purpose

Handles all course-related functionality including:
- Course creation and management
- Category organization
- Instructor profiles
- Student reviews and ratings

## Models

| Model | Description |
|-------|-------------|
| Category | Course categories with hierarchy |
| Instructor | Course instructors |
| Course | Main course entity |
| Review | User reviews and ratings |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/courses/ | List all courses |
| POST | /api/v1/courses/ | Create course |
| GET | /api/v1/courses/{id}/ | Get course detail |
| PUT | /api/v1/courses/{id}/ | Update course |
| DELETE | /api/v1/courses/{id}/ | Delete course |

## Frontend Views

| URL | View | Template |
|-----|------|----------|
| /courses/ | course_list | courses/course_list.html |
| /courses/{slug}/ | course_detail | courses/course_detail.html |

## Dependencies

- accounts app (for User model)
- core app (for site configuration)
```

---

## 8. Testing Conventions

### 8.1 Test Structure

```
app_name/
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Model unit tests
│   ├── test_views.py        # View unit tests
│   ├── test_api.py          # API endpoint tests
│   ├── test_forms.py        # Form validation tests
│   ├── test_serializers.py  # Serializer tests
│   └── factories.py         # Test data factories
```

### 8.2 Test Naming

```python
# Format: test_<what>_<scenario>_<expected_result>

def test_create_course_valid_data_returns_201(self):
    """Course creation with valid data should return 201."""
    pass

def test_create_course_negative_price_returns_400(self):
    """Course creation with negative price should return 400."""
    pass

def test_course_str_returns_title(self):
    """Course __str__ should return the title."""
    pass
```

### 8.3 Test Example

```python
"""
Courses API Tests - Test suite for course API endpoints.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Course, Category
from .factories import CourseFactory, UserFactory


class CourseAPITestCase(APITestCase):
    """Test suite for Course API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = UserFactory()
        self.category = Category.objects.create(name='Programming')
        self.course = CourseFactory(category=self.category)

    def test_list_courses_returns_200(self):
        """GET /api/v1/courses/ should return 200 and list of courses."""
        url = reverse('api:v1:courses:course-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_course_unauthenticated_returns_401(self):
        """POST /api/v1/courses/ without auth should return 401."""
        url = reverse('api:v1:courses:course-list')
        data = {'title': 'New Course', 'price': 29.99}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_course_authenticated_returns_201(self):
        """POST /api/v1/courses/ with auth should return 201."""
        self.client.force_authenticate(user=self.user)
        url = reverse('api:v1:courses:course-list')
        data = {
            'title': 'New Course',
            'description': 'Course description',
            'price': 29.99,
            'category': self.category.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
```

### 8.4 Coverage Requirements

- **Minimum**: 80% overall coverage
- **Critical paths**: 100% coverage (authentication, payments, permissions)
- **Models**: 100% coverage for all model methods and properties

```bash
# Run tests with coverage
coverage run --source='.' manage.py test
coverage report --fail-under=80
coverage html
```

---

## 9. Git Workflow

### 9.1 Branch Naming

```
main                    # Production-ready code
develop                 # Integration branch
feature/add-course-reviews    # New feature
bugfix/fix-login-error        # Bug fix
hotfix/security-patch         # Urgent production fix
release/v1.2.0               # Release preparation
```

### 9.2 Commit Messages

Follow Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, semicolons, etc.)
- `refactor`: Code refactor (no feature/fix)
- `test`: Add/update tests
- `chore`: Maintenance tasks

Examples:
```
feat(courses): add course review functionality

- Add Review model with rating and comment
- Add ReviewViewSet with CRUD operations
- Add review submission form to course detail page

Closes #123
```

```
fix(auth): prevent session fixation on login

Regenerate session ID after successful authentication
to prevent session fixation attacks.

Security: CVE-2024-XXXX
```

### 9.3 Pull Request Process

1. Create feature branch from `develop`
2. Make changes with proper commits
3. Push branch and create PR
4. Fill out PR template:
   - Description of changes
   - Link to issue/ticket
   - Testing performed
   - Screenshots (if UI changes)
5. Request code review
6. Address review comments
7. Ensure CI passes
8. Merge after approval

### 9.4 Code Review Checklist

- [ ] Code follows conventions
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] No hardcoded secrets
- [ ] Performance considered
- [ ] Error handling adequate

---

## 10. Environment Configuration

### 10.1 Environment Files

```
.env.example      # Template (committed to git)
.env              # Local development (NOT in git)
.env.test         # Testing environment (NOT in git)
.env.production   # Production (NOT in git, on server only)
```

### 10.2 Required Variables

```bash
# .env.example

# =============================================================================
# DJANGO CORE
# =============================================================================
SECRET_KEY=your-secret-key-here-generate-new-for-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# =============================================================================
# DATABASE
# =============================================================================
DATABASE_URL=postgres://user:password@localhost:5432/edupath
# For SQLite (dev only): DATABASE_URL=sqlite:///db.sqlite3

# =============================================================================
# SECURITY
# =============================================================================
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# =============================================================================
# EMAIL
# =============================================================================
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# =============================================================================
# REDIS / CACHING
# =============================================================================
REDIS_URL=redis://localhost:6379/0
CACHE_URL=redis://localhost:6379/1

# =============================================================================
# CELERY
# =============================================================================
CELERY_BROKER_URL=redis://localhost:6379/2

# =============================================================================
# STORAGE
# =============================================================================
# For local: leave empty
# For S3: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

# =============================================================================
# THIRD PARTY
# =============================================================================
SENTRY_DSN=
GOOGLE_ANALYTICS_ID=
```

### 10.3 Settings Organization

```python
# settings.py - Base settings

from decouple import config, Csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Database
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
    )
}
```

---

## 11. Error Handling

### 11.1 Exception Handling Pattern

```python
# GOOD - Catch specific exceptions, log with context
import logging

logger = logging.getLogger(__name__)

def enroll_in_course(user, course):
    """Enroll user in a course."""
    try:
        enrollment = Enrollment.objects.create(user=user, course=course)
        return enrollment
    except IntegrityError:
        logger.warning(
            "Duplicate enrollment attempt",
            extra={'user_id': user.id, 'course_id': course.id}
        )
        raise AlreadyEnrolledException("User is already enrolled")
    except Course.DoesNotExist:
        logger.error(
            "Course not found during enrollment",
            extra={'course_id': course.id}
        )
        raise

# BAD - Catch all exceptions
try:
    do_something()
except Exception:  # Too broad!
    pass  # Silently ignoring errors
```

### 11.2 API Error Response Format

```python
# Standard error response format
{
    "error": "validation_error",
    "message": "The provided data is invalid",
    "details": {
        "price": ["Price must be a positive number"],
        "title": ["Title is required"]
    },
    "code": "ERR_VALIDATION"
}

# Implementation
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error': exc.__class__.__name__.lower(),
            'message': str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            'details': response.data if isinstance(response.data, dict) else {},
            'code': f'ERR_{response.status_code}',
        }

    return response
```

### 11.3 Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/edupath.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'edupath': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

---

## 12. API Design Standards

### 12.1 RESTful Principles

| HTTP Method | Usage | Example |
|-------------|-------|---------|
| GET | Retrieve resource(s) | `GET /api/v1/courses/` |
| POST | Create resource | `POST /api/v1/courses/` |
| PUT | Full update | `PUT /api/v1/courses/1/` |
| PATCH | Partial update | `PATCH /api/v1/courses/1/` |
| DELETE | Delete resource | `DELETE /api/v1/courses/1/` |

### 12.2 Response Status Codes

| Code | Usage |
|------|-------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation error) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 429 | Too Many Requests (rate limited) |
| 500 | Internal Server Error |

### 12.3 Response Format

```python
# Success response (list)
{
    "success": true,
    "data": [
        {"id": 1, "title": "Python Basics"},
        {"id": 2, "title": "Django Fundamentals"}
    ],
    "meta": {
        "page": 1,
        "page_size": 20,
        "total_count": 100,
        "total_pages": 5
    }
}

# Success response (single)
{
    "success": true,
    "data": {
        "id": 1,
        "title": "Python Basics",
        "description": "Learn Python from scratch"
    }
}

# Error response
{
    "success": false,
    "error": "validation_error",
    "message": "Invalid data provided",
    "details": {
        "price": ["Must be a positive number"]
    }
}
```

### 12.4 API Versioning

```python
# urls.py
urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('api/v2/', include('api.v2.urls')),  # Future version
]

# Deprecation header for old versions
class DeprecationMiddleware:
    def process_response(self, request, response):
        if '/api/v1/' in request.path:
            response['Deprecation'] = 'true'
            response['Sunset'] = 'Sat, 01 Jan 2026 00:00:00 GMT'
        return response
```

---

## 13. Database Best Practices

### 13.1 Model Design

```python
# Abstract base models
class TimestampedModel(models.Model):
    """Abstract model with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Abstract model with soft delete support."""
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """Soft delete instead of hard delete."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])


# Usage
class Course(TimestampedModel, SoftDeleteModel):
    title = models.CharField(max_length=200)
    # ...
```

### 13.2 Index Strategy

```python
class Course(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # Composite indexes for common query patterns
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_published', '-created_at']),
        ]
```

### 13.3 Migration Best Practices

```python
# DO: Review migrations before applying
python manage.py showmigrations
python manage.py sqlmigrate app_name 0001

# DO: Create data migrations for data changes
python manage.py makemigrations --empty app_name

# DON'T: Edit applied migrations (create new ones instead)
# DON'T: Use RunPython for heavy data operations (use management commands)

# Data migration example
def populate_slugs(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    for course in Course.objects.filter(slug=''):
        course.slug = slugify(course.title)
        course.save(update_fields=['slug'])

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
```

### 13.4 Query Optimization

```python
# Use QuerySet methods efficiently
# BAD
for course in Course.objects.all():
    if course.status == 'published':
        print(course.title)

# GOOD
for course in Course.objects.filter(status='published'):
    print(course.title)

# Use values() for read-only data
titles = Course.objects.filter(status='published').values_list('title', flat=True)

# Use exists() instead of count() for boolean checks
if Course.objects.filter(status='published').exists():
    pass

# Use bulk operations
Course.objects.filter(status='draft').update(status='published')
Course.objects.bulk_create([Course(...), Course(...)])
```

---

## 14. Performance Optimization

### 14.1 Query Monitoring

```python
# settings.py (development only)
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
    }

# Use django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### 14.2 Static Files

```python
# settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# For production with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 14.3 Template Optimization

```html
<!-- Cache template fragments -->
{% load cache %}
{% cache 3600 course_sidebar course.id %}
    <!-- Expensive template code -->
{% endcache %}

<!-- Use with for repeated access -->
{% with course.instructor as instructor %}
    {{ instructor.name }} - {{ instructor.bio }}
{% endwith %}
```

### 14.4 API Response Optimization

```python
# Use serializer fields to limit data
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'price']  # Only needed fields

# Use pagination
class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

# Use field selection
# GET /api/v1/courses/?fields=id,title
class DynamicFieldsMixin:
    def get_serializer(self, *args, **kwargs):
        fields = self.request.query_params.get('fields')
        if fields:
            kwargs['fields'] = fields.split(',')
        return super().get_serializer(*args, **kwargs)
```

---

## Summary

### Key Principles

1. **Security First** - Never compromise security
2. **Document Everything** - Code without docs is incomplete
3. **Test Thoroughly** - Minimum 80% coverage
4. **Optimize Queries** - Avoid N+1, use indexes
5. **Follow Conventions** - Consistency is key
6. **Review Code** - All changes require review

### Quick Reference

| Item | Convention |
|------|------------|
| Files | `snake_case.py` |
| Classes | `PascalCase` |
| Functions | `snake_case` |
| URLs | `kebab-case` |
| Constants | `UPPER_SNAKE_CASE` |
| Commits | `type(scope): description` |
| Branches | `type/description` |

### Required Files Per App

- [ ] `README.md`
- [ ] `models.py`
- [ ] `views_frontend.py`
- [ ] `views_api.py`
- [ ] `serializers.py`
- [ ] `urls.py`
- [ ] `admin.py`
- [ ] `tests/`

---

**This convention is MANDATORY for all Edupath development.**

*Last updated: 2026-01-28*
