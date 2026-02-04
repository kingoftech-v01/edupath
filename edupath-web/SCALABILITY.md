# Edupath Scalability Guidelines

**Version**: 1.0
**Last Updated**: 2026-01-28
**Status**: RECOMMENDED - Follow these patterns for scalable architecture

---

## Table of Contents

1. [Scalability Principles](#1-scalability-principles)
2. [Database Optimization](#2-database-optimization)
3. [Caching Strategies](#3-caching-strategies)
4. [Background Tasks](#4-background-tasks)
5. [API Performance](#5-api-performance)
6. [Static & Media Files](#6-static--media-files)
7. [Horizontal Scaling](#7-horizontal-scaling)
8. [Monitoring & Profiling](#8-monitoring--profiling)

---

## 1. Scalability Principles

### 1.1 Design for Scale

```
┌────────────────────────────────────────────────────────────────┐
│                        Load Balancer                            │
│                     (nginx / AWS ALB)                          │
└────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        ┌──────────┐    ┌──────────┐    ┌──────────┐
        │  App 1   │    │  App 2   │    │  App 3   │   Stateless
        │ (Django) │    │ (Django) │    │ (Django) │   App Servers
        └──────────┘    └──────────┘    └──────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  ┌──────────┐          ┌──────────┐          ┌──────────┐
  │  Redis   │          │ PostgreSQL│          │   S3     │
  │ (Cache)  │          │   (DB)   │          │ (Files)  │
  └──────────┘          └──────────┘          └──────────┘
```

### 1.2 Key Principles

1. **Stateless Application** - No session data on server
2. **External Session Store** - Use Redis for sessions
3. **Horizontal Scaling** - Add more servers, not bigger ones
4. **Cache Everything** - Reduce database load
5. **Async Processing** - Don't block HTTP requests

---

## 2. Database Optimization

### 2.1 Indexing Strategy

```python
# models.py

class Course(models.Model):
    # Single column indexes for filtered fields
    title = models.CharField(max_length=200, db_index=True)
    status = models.CharField(max_length=20, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)

    # ForeignKey automatically creates index
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    class Meta:
        # Composite indexes for common query patterns
        indexes = [
            # For: Course.objects.filter(status='published', category=cat)
            models.Index(fields=['status', 'category']),

            # For: Course.objects.filter(is_published=True).order_by('-created_at')
            models.Index(fields=['is_published', '-created_at']),

            # For text search (PostgreSQL)
            models.Index(
                fields=['title'],
                name='course_title_trgm_idx',
                opclasses=['gin_trgm_ops'],
            ),
        ]
```

### 2.2 Query Optimization

```python
# PROBLEM: N+1 Queries
# Each iteration makes a separate query for instructor
courses = Course.objects.all()
for course in courses:
    print(course.instructor.name)  # N additional queries!

# SOLUTION 1: select_related (ForeignKey, OneToOne)
courses = Course.objects.select_related('instructor', 'category').all()
for course in courses:
    print(course.instructor.name)  # No additional queries

# SOLUTION 2: prefetch_related (ManyToMany, reverse ForeignKey)
courses = Course.objects.prefetch_related('reviews', 'tags').all()
for course in courses:
    print(course.reviews.count())  # Prefetched

# SOLUTION 3: Prefetch with custom queryset
from django.db.models import Prefetch

courses = Course.objects.prefetch_related(
    Prefetch(
        'reviews',
        queryset=Review.objects.filter(rating__gte=4).order_by('-created_at')[:5]
    )
).all()
```

### 2.3 Efficient Querying

```python
# Use values() for read-only data (avoids model instantiation)
titles = Course.objects.filter(is_published=True).values_list('title', flat=True)

# Use exists() instead of count() for boolean checks
if Course.objects.filter(status='published').exists():
    pass  # More efficient than count() > 0

# Use only() to limit fields loaded
courses = Course.objects.only('id', 'title', 'slug').all()

# Use defer() to exclude heavy fields
courses = Course.objects.defer('description', 'full_content').all()

# Bulk operations
Course.objects.filter(status='draft').update(status='archived')
Course.objects.bulk_create([Course(...), Course(...), Course(...)])
Course.objects.bulk_update(courses, ['status', 'updated_at'])

# Chunked iteration for large datasets
from django.core.paginator import Paginator

def process_all_courses():
    paginator = Paginator(Course.objects.all(), 100)
    for page_num in paginator.page_range:
        page = paginator.page(page_num)
        for course in page.object_list:
            process_course(course)
```

### 2.4 Database Connection Pooling

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling (10 minutes)
        'CONN_HEALTH_CHECKS': True,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}

# For high-traffic: Use pgbouncer
# DATABASES['default']['HOST'] = 'pgbouncer'
# DATABASES['default']['PORT'] = '6432'
```

### 2.5 Read Replicas

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edupath',
        # ... primary database config
    },
    'replica': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'edupath',
        # ... replica database config
    },
}

# Database router
class PrimaryReplicaRouter:
    def db_for_read(self, model, **hints):
        return 'replica'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == 'default'

DATABASE_ROUTERS = ['path.to.PrimaryReplicaRouter']
```

---

## 3. Caching Strategies

### 3.1 Cache Configuration

```python
# settings.py

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/0'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
        'KEY_PREFIX': 'edupath',
    },
    'sessions': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'session',
    },
}

# Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'
```

### 3.2 View-Level Caching

```python
# views.py

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Cache entire view response
@cache_page(60 * 15)  # 15 minutes
def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, 'courses/list.html', {'courses': courses})


# Cache per user
@cache_page(60 * 15)
@vary_on_cookie
def dashboard(request):
    # Different cache for each user
    return render(request, 'dashboard.html')


# Conditional caching based on user
def course_list(request):
    if request.user.is_authenticated:
        # Don't cache for authenticated users (personalized content)
        courses = get_courses_for_user(request.user)
    else:
        # Cache for anonymous users
        cache_key = 'course_list_anonymous'
        courses = cache.get(cache_key)
        if courses is None:
            courses = list(Course.objects.filter(is_published=True)[:20])
            cache.set(cache_key, courses, timeout=300)

    return render(request, 'courses/list.html', {'courses': courses})
```

### 3.3 Object-Level Caching

```python
# models.py

from django.core.cache import cache


class Course(models.Model):
    # ...

    @classmethod
    def get_cached(cls, course_id):
        """Get course from cache or database."""
        cache_key = f'course:{course_id}'
        course = cache.get(cache_key)

        if course is None:
            try:
                course = cls.objects.select_related(
                    'instructor', 'category'
                ).get(pk=course_id)
                cache.set(cache_key, course, timeout=3600)  # 1 hour
            except cls.DoesNotExist:
                return None

        return course

    def save(self, *args, **kwargs):
        """Invalidate cache on save."""
        super().save(*args, **kwargs)
        cache.delete(f'course:{self.pk}')

    def delete(self, *args, **kwargs):
        """Invalidate cache on delete."""
        cache.delete(f'course:{self.pk}')
        super().delete(*args, **kwargs)
```

### 3.4 Query Caching

```python
# utils.py

from django.core.cache import cache
from django.db.models import Count, Avg


def get_course_stats():
    """Get cached course statistics."""
    cache_key = 'course_stats'
    stats = cache.get(cache_key)

    if stats is None:
        stats = {
            'total_courses': Course.objects.count(),
            'published_courses': Course.objects.filter(is_published=True).count(),
            'total_students': Enrollment.objects.values('user').distinct().count(),
            'avg_rating': Review.objects.aggregate(avg=Avg('rating'))['avg'],
        }
        cache.set(cache_key, stats, timeout=3600)  # 1 hour

    return stats


def invalidate_course_stats():
    """Call when courses/enrollments change."""
    cache.delete('course_stats')
```

### 3.5 Template Fragment Caching

```html
{% load cache %}

<!-- Cache expensive template fragments -->
{% cache 3600 course_sidebar course.id %}
    <div class="sidebar">
        <h3>{{ course.title }}</h3>
        <p>{{ course.description|truncatewords:50 }}</p>
        <ul>
            {% for lesson in course.lessons.all %}
                <li>{{ lesson.title }}</li>
            {% endfor %}
        </ul>
    </div>
{% endcache %}

<!-- Cache with user-specific key -->
{% cache 600 user_dashboard user.id %}
    <!-- User-specific content -->
{% endcache %}
```

---

## 4. Background Tasks

### 4.1 Celery Configuration

```python
# celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Edupath.settings')

app = Celery('edupath')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


# settings.py

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/2')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/3')

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'UTC'

CELERY_TASK_ROUTES = {
    'courses.tasks.send_email': {'queue': 'email'},
    'courses.tasks.process_video': {'queue': 'video'},
    'courses.tasks.generate_report': {'queue': 'reports'},
}

CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
```

### 4.2 Task Definitions

```python
# tasks.py

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={'max_retries': 3},
)
def send_welcome_email(self, user_id):
    """
    Send welcome email to new user.

    Runs asynchronously with automatic retry on failure.
    """
    from django.contrib.auth import get_user_model
    from django.core.mail import send_mail

    User = get_user_model()
    user = User.objects.get(id=user_id)

    logger.info(f"Sending welcome email to {user.email}")

    send_mail(
        subject='Welcome to Edupath!',
        message=f'Hello {user.first_name}, welcome to our platform.',
        from_email='noreply@edupath.com',
        recipient_list=[user.email],
    )

    return f'Email sent to {user.email}'


@shared_task(bind=True)
def process_video_upload(self, video_id):
    """
    Process uploaded video (transcoding, thumbnails).

    Long-running task that should not block HTTP requests.
    """
    from courses.models import Video

    video = Video.objects.get(id=video_id)

    # Update status
    video.status = 'processing'
    video.save(update_fields=['status'])

    try:
        # Process video (transcoding, etc.)
        process_video(video.file.path)

        video.status = 'ready'
        video.save(update_fields=['status'])

        return f'Video {video_id} processed successfully'

    except Exception as e:
        video.status = 'failed'
        video.save(update_fields=['status'])
        raise


@shared_task
def cleanup_expired_sessions():
    """
    Periodic task to clean up expired sessions.

    Schedule: daily at 3 AM
    """
    from django.contrib.sessions.models import Session
    from django.utils import timezone

    expired = Session.objects.filter(expire_date__lt=timezone.now())
    count = expired.count()
    expired.delete()

    return f'Deleted {count} expired sessions'
```

### 4.3 Task Scheduling

```python
# settings.py

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'cleanup-sessions': {
        'task': 'core.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),  # Daily at 3 AM
    },
    'update-course-stats': {
        'task': 'courses.tasks.update_course_statistics',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'send-daily-digest': {
        'task': 'accounts.tasks.send_daily_digest',
        'schedule': crontab(hour=8, minute=0),  # Daily at 8 AM
    },
}
```

### 4.4 Using Tasks in Views

```python
# views.py

from .tasks import send_welcome_email, process_video_upload


def register(request):
    """User registration view."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Send email asynchronously (non-blocking)
            send_welcome_email.delay(user.id)

            return redirect('registration_complete')

    return render(request, 'register.html', {'form': form})


def upload_video(request, course_id):
    """Video upload view."""
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course_id = course_id
            video.status = 'pending'
            video.save()

            # Process video asynchronously
            process_video_upload.delay(video.id)

            return JsonResponse({
                'status': 'uploaded',
                'video_id': video.id,
                'message': 'Video is being processed'
            })

    return render(request, 'upload.html', {'form': form})
```

---

## 5. API Performance

### 5.1 Pagination

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# Custom pagination
from rest_framework.pagination import PageNumberPagination, CursorPagination


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CursorPagination(CursorPagination):
    """
    Cursor pagination for large datasets.
    More efficient than offset pagination for millions of records.
    """
    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'


# views.py
class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination
```

### 5.2 Field Selection

```python
# serializers.py

class DynamicFieldsMixin:
    """
    Allow clients to specify which fields to return.
    Usage: GET /api/courses/?fields=id,title,price
    """

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields.split(','))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CourseSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'instructor', 'category']


# views.py
class CourseViewSet(viewsets.ModelViewSet):
    def get_serializer(self, *args, **kwargs):
        fields = self.request.query_params.get('fields')
        if fields:
            kwargs['fields'] = fields
        return super().get_serializer(*args, **kwargs)
```

### 5.3 Response Compression

```python
# settings.py

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',  # Enable gzip compression
    # ... other middleware
]

# Or use WhiteNoise for static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### 5.4 API Caching

```python
# views.py

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CourseViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 5))  # 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 15))  # 15 minutes
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
```

---

## 6. Static & Media Files

### 6.1 Static Files Configuration

```python
# settings.py

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Or for S3
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

### 6.2 Media Files with S3

```python
# settings.py

if not DEBUG:
    # AWS S3 configuration
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION', default='us-east-1')

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'private'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',  # 1 day
    }

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

### 6.3 CDN Integration

```python
# settings.py

# CloudFront CDN
CDN_DOMAIN = config('CDN_DOMAIN', default='')

if CDN_DOMAIN:
    STATIC_URL = f'https://{CDN_DOMAIN}/static/'
    MEDIA_URL = f'https://{CDN_DOMAIN}/media/'
```

---

## 7. Horizontal Scaling

### 7.1 Stateless Application

```python
# Ensure no server-side session state

# Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'sessions'

# Use Redis for cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
    },
}

# Don't store files locally
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### 7.2 Load Balancer Health Check

```python
# urls.py

urlpatterns = [
    path('health/', include('health_check.urls')),
]

# settings.py

INSTALLED_APPS += [
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.celery',
    'health_check.contrib.redis',
]
```

### 7.3 Docker Configuration

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "Edupath.wsgi:application"]
```

```yaml
# docker-compose.yml

version: '3.8'

services:
  web:
    build: .
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/edupath
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    deploy:
      replicas: 3

  celery:
    build: .
    command: celery -A edupath worker -l info
    depends_on:
      - redis

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

---

## 8. Monitoring & Profiling

### 8.1 Query Monitoring

```python
# settings.py (development)

if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['console'],
    }

# Use django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

### 8.2 Performance Monitoring

```python
# settings.py

# Sentry for error tracking and performance
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN', default=''),
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,  # 10% of transactions
    profiles_sample_rate=0.1,
)
```

### 8.3 Custom Metrics

```python
# middleware.py

import time
import logging

logger = logging.getLogger('performance')


class RequestTimingMiddleware:
    """Log request timing for performance monitoring."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        if duration > 1.0:  # Log slow requests (>1 second)
            logger.warning(
                f"Slow request: {request.method} {request.path} "
                f"took {duration:.2f}s"
            )

        response['X-Request-Time'] = f'{duration:.3f}s'
        return response
```

---

## Quick Reference

### Performance Checklist

- [ ] Database indexes on filtered/sorted fields
- [ ] select_related/prefetch_related for related objects
- [ ] Pagination on all list endpoints
- [ ] Caching for expensive queries
- [ ] Background tasks for long operations
- [ ] Static files served via CDN
- [ ] Gzip compression enabled
- [ ] Connection pooling configured

### Scaling Checklist

- [ ] Stateless application (no server-side state)
- [ ] Redis for sessions and cache
- [ ] S3 or similar for file storage
- [ ] Celery for background tasks
- [ ] Health check endpoint
- [ ] Docker containerization
- [ ] Load balancer configuration

---

**Follow these guidelines for scalable Edupath architecture.**

*Last updated: 2026-01-28*
