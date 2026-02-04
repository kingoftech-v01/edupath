# Edupath Security Guidelines

**Version**: 1.0
**Last Updated**: 2026-01-28
**Status**: MANDATORY - All code MUST comply with these security standards

---

## Table of Contents

1. [Security Principles](#1-security-principles)
2. [Environment & Secrets](#2-environment--secrets)
3. [Authentication](#3-authentication)
4. [Authorization](#4-authorization)
5. [Input Validation](#5-input-validation)
6. [Output Encoding](#6-output-encoding)
7. [CORS & CSRF](#7-cors--csrf)
8. [Security Headers](#8-security-headers)
9. [Database Security](#9-database-security)
10. [File Upload Security](#10-file-upload-security)
11. [API Security](#11-api-security)
12. [Logging & Monitoring](#12-logging--monitoring)
13. [Dependency Security](#13-dependency-security)
14. [Security Checklist](#14-security-checklist)

---

## 1. Security Principles

### 1.1 Defense in Depth

Apply multiple layers of security controls:

```
┌─────────────────────────────────────────────────────┐
│                    WAF / CDN                         │  Layer 1: Network
├─────────────────────────────────────────────────────┤
│              Rate Limiting / Firewall                │  Layer 2: Application
├─────────────────────────────────────────────────────┤
│           Authentication / Authorization             │  Layer 3: Identity
├─────────────────────────────────────────────────────┤
│            Input Validation / Sanitization           │  Layer 4: Data
├─────────────────────────────────────────────────────┤
│              Database Access Controls                │  Layer 5: Storage
└─────────────────────────────────────────────────────┘
```

### 1.2 Principle of Least Privilege

- Users get minimum permissions needed
- Services use restricted database accounts
- API tokens have scoped permissions

### 1.3 Fail Secure

When errors occur, fail to a secure state:

```python
# CORRECT - Deny by default
def has_permission(user, resource):
    try:
        return check_permission(user, resource)
    except Exception:
        return False  # Fail secure: deny access

# WRONG - Fail open
def has_permission(user, resource):
    try:
        return check_permission(user, resource)
    except Exception:
        return True  # DANGEROUS: grants access on error
```

---

## 2. Environment & Secrets

### 2.1 Never Hardcode Secrets

**CRITICAL**: Never commit secrets to version control.

```python
# settings.py

from decouple import config, Csv

# CORRECT - Load from environment
SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL')
API_KEY = config('STRIPE_API_KEY')

# WRONG - Hardcoded secrets (SECURITY VIOLATION!)
SECRET_KEY = 'django-insecure-abc123'  # NEVER DO THIS
DATABASE_PASSWORD = 'password123'       # NEVER DO THIS
```

### 2.2 Environment File Security

```bash
# .gitignore - MUST include these
.env
.env.local
.env.production
*.pem
*.key
secrets/
```

### 2.3 Secret Key Generation

```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Or use secrets module
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 2.4 Production Secrets Management

For production, use:
- AWS Secrets Manager
- HashiCorp Vault
- Azure Key Vault
- Google Secret Manager

```python
# Example: AWS Secrets Manager
import boto3
import json

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

---

## 3. Authentication

### 3.1 Password Security

```python
# settings.py

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12},  # Minimum 12 characters
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom validator for complexity
class ComplexityValidator:
    def validate(self, password, user=None):
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            raise ValidationError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain digit")
        if not any(c in '!@#$%^&*()' for c in password):
            raise ValidationError("Password must contain special character")
```

### 3.2 Session Security

```python
# settings.py

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

SESSION_COOKIE_SECURE = True          # HTTPS only
SESSION_COOKIE_HTTPONLY = True        # No JavaScript access
SESSION_COOKIE_SAMESITE = 'Lax'       # CSRF protection
SESSION_COOKIE_AGE = 86400            # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True     # Extend on activity

# Regenerate session on login (prevent session fixation)
# This is done automatically by Django's login()
```

### 3.3 Login Security

```python
# views.py

from django.contrib.auth import login, authenticate
from django.contrib.auth.signals import user_logged_in, user_login_failed
import logging

logger = logging.getLogger('security')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Rate limit login attempts
        cache_key = f'login_attempts_{get_client_ip(request)}'
        attempts = cache.get(cache_key, 0)

        if attempts >= 5:
            logger.warning(f"Login blocked for IP: {get_client_ip(request)}")
            return HttpResponse("Too many attempts. Try again later.", status=429)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request)
            cache.delete(cache_key)  # Reset attempts on success
            logger.info(f"Successful login: {username}")
            return redirect('dashboard')
        else:
            cache.set(cache_key, attempts + 1, timeout=300)  # 5 minute lockout
            logger.warning(f"Failed login attempt for: {username}")
            return render(request, 'login.html', {'error': 'Invalid credentials'})
```

### 3.4 Two-Factor Authentication

```python
# Recommended: django-two-factor-auth

INSTALLED_APPS += [
    'django_otp',
    'django_otp.plugins.otp_totp',
    'two_factor',
]

# Enforce 2FA for admin users
TWO_FACTOR_FORCE_OTP_ADMIN = True
```

---

## 4. Authorization

### 4.1 Permission Classes

```python
# permissions.py

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners to edit.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for owner
        return obj.owner == request.user


class IsInstructorOrAdmin(permissions.BasePermission):
    """
    Permission for instructors and admin users only.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_staff or hasattr(request.user, 'instructor_profile'))
        )


class IsEnrolledInCourse(permissions.BasePermission):
    """
    Permission for users enrolled in the course.
    """
    def has_object_permission(self, request, view, obj):
        return Enrollment.objects.filter(
            user=request.user,
            course=obj
        ).exists()
```

### 4.2 View-Level Authorization

```python
# views_api.py

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """Return different permissions based on action."""
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsInstructorOrAdmin()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwner()]
        return super().get_permissions()


# views_frontend.py
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('courses.add_course', raise_exception=True)
def create_course(request):
    """Only users with add_course permission can access."""
    pass
```

### 4.3 Template Authorization

```html
<!-- Check permissions in templates -->
{% if perms.courses.add_course %}
    <a href="{% url 'courses:create' %}">Create Course</a>
{% endif %}

{% if user == course.owner or user.is_staff %}
    <a href="{% url 'courses:edit' course.pk %}">Edit</a>
{% endif %}
```

---

## 5. Input Validation

### 5.1 Form Validation

```python
# forms.py

from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
import bleach


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price']

    def clean_title(self):
        """Sanitize and validate title."""
        title = self.cleaned_data['title']

        # Remove HTML tags
        title = bleach.clean(title, tags=[], strip=True)

        # Check length
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters")
        if len(title) > 200:
            raise forms.ValidationError("Title cannot exceed 200 characters")

        return title

    def clean_price(self):
        """Validate price is positive and reasonable."""
        price = self.cleaned_data['price']

        if price < 0:
            raise forms.ValidationError("Price cannot be negative")
        if price > 9999.99:
            raise forms.ValidationError("Price cannot exceed $9,999.99")

        return price

    def clean_description(self):
        """Sanitize HTML in description."""
        description = self.cleaned_data['description']

        # Allow only safe HTML tags
        allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'a']
        allowed_attrs = {'a': ['href', 'title']}

        return bleach.clean(
            description,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
```

### 5.2 Serializer Validation

```python
# serializers.py

from rest_framework import serializers
import re


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'slug']
        read_only_fields = ['id', 'slug']

    def validate_title(self, value):
        """Validate title format and content."""
        # Check for suspicious patterns
        if re.search(r'<script|javascript:|on\w+=', value, re.IGNORECASE):
            raise serializers.ValidationError("Invalid characters in title")

        # Check length
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title too short")

        return value.strip()

    def validate_price(self, value):
        """Ensure price is valid."""
        if value < 0:
            raise serializers.ValidationError("Price must be positive")
        return value

    def validate(self, data):
        """Cross-field validation."""
        # Example: Free courses must have [FREE] in title
        if data.get('price', 0) == 0:
            if '[FREE]' not in data.get('title', ''):
                raise serializers.ValidationError(
                    "Free courses must include [FREE] in title"
                )
        return data
```

### 5.3 URL Parameter Validation

```python
# views.py

from django.http import Http404
import uuid


def course_detail(request, course_id):
    """Validate course_id parameter."""
    # Validate UUID format
    try:
        uuid.UUID(str(course_id))
    except ValueError:
        raise Http404("Invalid course ID")

    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course_detail.html', {'course': course})
```

---

## 6. Output Encoding

### 6.1 Template Auto-Escaping

Django automatically escapes HTML in templates. **NEVER disable this without good reason.**

```html
<!-- SAFE - Auto-escaped -->
{{ user_input }}

<!-- DANGEROUS - Unescaped (only for trusted content) -->
{{ trusted_html|safe }}

<!-- If you must render HTML, sanitize first -->
{{ sanitized_html|safe }}
```

### 6.2 JSON Response Escaping

```python
# Django REST Framework handles this automatically
# But for manual JSON responses:

from django.http import JsonResponse

def api_view(request):
    # JsonResponse escapes content automatically
    return JsonResponse({
        'message': user_input,  # Escaped
        'html': sanitized_html,  # Must be sanitized before storing
    })
```

### 6.3 JavaScript Context

```html
<!-- WRONG - XSS vulnerability -->
<script>
var data = "{{ user_input }}";  // Can break out of string
</script>

<!-- CORRECT - Use json_script filter -->
{{ user_data|json_script:"user-data" }}
<script>
const data = JSON.parse(document.getElementById('user-data').textContent);
</script>
```

---

## 7. CORS & CSRF

### 7.1 CORS Configuration

```python
# settings.py

INSTALLED_APPS += ['corsheaders']

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Development only
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Production - ALWAYS whitelist
else:
    CORS_ALLOWED_ORIGINS = [
        "https://edupath.com",
        "https://www.edupath.com",
        "https://app.edupath.com",
    ]

    CORS_ALLOWED_ORIGIN_REGEXES = [
        r"^https://\w+\.edupath\.com$",
    ]

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOW_METHODS = [
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
    ]

    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'origin',
        'x-csrftoken',
        'x-requested-with',
    ]
```

### 7.2 CSRF Protection

```python
# settings.py

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://edupath.com',
    'https://www.edupath.com',
]

# For API views that don't use sessions
# Use token-based authentication instead of CSRF
```

```html
<!-- Always include CSRF token in forms -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>

<!-- For AJAX requests -->
<script>
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(data),
});
</script>
```

---

## 8. Security Headers

### 8.1 Required Headers

```python
# settings.py

# Built-in Django security
SECURE_BROWSER_XSS_FILTER = True        # X-XSS-Protection
SECURE_CONTENT_TYPE_NOSNIFF = True      # X-Content-Type-Options
X_FRAME_OPTIONS = 'DENY'                 # Clickjacking protection

# HTTPS enforcement (production only)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000       # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 8.2 Content Security Policy

```python
# Using django-csp

INSTALLED_APPS += ['csp']

MIDDLEWARE += ['csp.middleware.CSPMiddleware']

# CSP Configuration
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.example.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'", "https://api.edupath.com")
CSP_FRAME_ANCESTORS = ("'none'",)
CSP_FORM_ACTION = ("'self'",)
```

### 8.3 Custom Security Middleware

```python
# middleware.py

class SecurityHeadersMiddleware:
    """Add additional security headers."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'

        # Enable XSS filter
        response['X-XSS-Protection'] = '1; mode=block'

        # Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'

        # Referrer policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions policy
        response['Permissions-Policy'] = (
            'accelerometer=(), camera=(), geolocation=(), '
            'gyroscope=(), magnetometer=(), microphone=(), '
            'payment=(), usb=()'
        )

        return response
```

---

## 9. Database Security

### 9.1 SQL Injection Prevention

```python
# CORRECT - Using ORM (parameterized queries)
Course.objects.filter(title__icontains=user_input)
Course.objects.filter(price__lte=max_price)

# CORRECT - Parameterized raw query (if absolutely necessary)
Course.objects.raw(
    "SELECT * FROM courses_course WHERE title LIKE %s",
    [f'%{user_input}%']
)

# CORRECT - Using cursor with parameters
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM courses_course WHERE id = %s",
        [course_id]
    )

# WRONG - String interpolation (SQL INJECTION!)
Course.objects.raw(f"SELECT * FROM courses WHERE title = '{user_input}'")

# WRONG - Format string
cursor.execute("SELECT * FROM courses WHERE id = %s" % course_id)
```

### 9.2 Database User Permissions

```sql
-- Create restricted user for application
CREATE USER edupath_app WITH PASSWORD 'secure_password';

-- Grant only necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO edupath_app;

-- Revoke dangerous permissions
REVOKE CREATE ON SCHEMA public FROM edupath_app;
REVOKE DROP ON ALL TABLES IN SCHEMA public FROM edupath_app;
```

### 9.3 Sensitive Data Encryption

```python
# models.py

from django.db import models
from django_cryptography.fields import encrypt


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Encrypt sensitive data at rest
    ssn = encrypt(models.CharField(max_length=11, blank=True))
    phone = encrypt(models.CharField(max_length=20, blank=True))

    # Regular field (no encryption needed)
    bio = models.TextField(blank=True)
```

---

## 10. File Upload Security

### 10.1 File Validation

```python
# validators.py

import magic
import os
from django.core.exceptions import ValidationError
from django.conf import settings


ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf'}
ALLOWED_MIMETYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'application/pdf'
}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file_upload(file):
    """Comprehensive file upload validation."""

    # 1. Check file size
    if file.size > MAX_FILE_SIZE:
        raise ValidationError(
            f"File too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
        )

    # 2. Check extension
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"File type {ext} is not allowed")

    # 3. Verify actual file content (not just extension)
    file_content = file.read(1024)
    file.seek(0)  # Reset file pointer

    mime_type = magic.from_buffer(file_content, mime=True)
    if mime_type not in ALLOWED_MIMETYPES:
        raise ValidationError(
            f"File content ({mime_type}) doesn't match allowed types"
        )

    # 4. Check for dangerous content
    if ext in {'.pdf'}:
        # Check PDF for JavaScript
        content = file.read()
        file.seek(0)
        if b'/JavaScript' in content or b'/JS' in content:
            raise ValidationError("PDF contains JavaScript (not allowed)")

    return True
```

### 10.2 Secure File Storage

```python
# models.py

import uuid
import os


def secure_upload_path(instance, filename):
    """Generate secure, unpredictable file path."""
    ext = os.path.splitext(filename)[1].lower()
    new_filename = f"{uuid.uuid4()}{ext}"
    return f"uploads/{instance.__class__.__name__.lower()}/{new_filename}"


class Course(models.Model):
    thumbnail = models.ImageField(
        upload_to=secure_upload_path,
        validators=[validate_file_upload]
    )


# settings.py

# Serve media files through X-Sendfile (nginx) in production
# Never serve user uploads directly through Django
```

### 10.3 Image Processing Security

```python
# utils.py

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def process_uploaded_image(image_file, max_size=(1920, 1080)):
    """
    Process and sanitize uploaded image.

    - Removes EXIF metadata (privacy)
    - Resizes if too large
    - Converts to safe format
    """
    img = Image.open(image_file)

    # Remove EXIF data
    data = list(img.getdata())
    img_no_exif = Image.new(img.mode, img.size)
    img_no_exif.putdata(data)

    # Resize if needed
    if img_no_exif.size[0] > max_size[0] or img_no_exif.size[1] > max_size[1]:
        img_no_exif.thumbnail(max_size, Image.LANCZOS)

    # Save to buffer
    buffer = BytesIO()
    img_no_exif.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)

    return InMemoryUploadedFile(
        buffer, 'ImageField', 'image.jpg',
        'image/jpeg', buffer.getbuffer().nbytes, None
    )
```

---

## 11. API Security

### 11.1 Rate Limiting

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
    },
}

# Custom throttle for sensitive endpoints
class LoginThrottle(throttling.AnonRateThrottle):
    rate = '5/minute'

class PasswordResetThrottle(throttling.AnonRateThrottle):
    rate = '3/hour'
```

### 11.2 API Authentication

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # Or JWT
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
```

### 11.3 API Input Sanitization

```python
# middleware.py

import json
import bleach


class APIInputSanitizationMiddleware:
    """Sanitize API request bodies."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.content_type == 'application/json':
            try:
                body = json.loads(request.body)
                sanitized = self.sanitize_dict(body)
                request._body = json.dumps(sanitized).encode()
            except json.JSONDecodeError:
                pass

        return self.get_response(request)

    def sanitize_dict(self, data):
        """Recursively sanitize dictionary values."""
        if isinstance(data, dict):
            return {k: self.sanitize_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_dict(item) for item in data]
        elif isinstance(data, str):
            return bleach.clean(data, tags=[], strip=True)
        return data
```

---

## 12. Logging & Monitoring

### 12.1 Security Logging

```python
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '{asctime} {levelname} {name} {message} '
                     '[user:{user_id}] [ip:{ip}] [path:{path}]',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'security',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}
```

### 12.2 Security Event Logging

```python
# signals.py

from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed
)
from django.dispatch import receiver
import logging

security_logger = logging.getLogger('security')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    security_logger.info(
        f"User logged in",
        extra={
            'user_id': user.id,
            'ip': get_client_ip(request),
            'path': request.path,
        }
    )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    security_logger.warning(
        f"Failed login attempt for: {credentials.get('username', 'unknown')}",
        extra={
            'user_id': None,
            'ip': get_client_ip(request),
            'path': request.path,
        }
    )


def get_client_ip(request):
    """Get client IP from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
```

### 12.3 Audit Trail

```python
# models.py

class AuditLog(models.Model):
    """Track all security-relevant actions."""

    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('PERMISSION_CHANGE', 'Permission Change'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    details = models.JSONField(default=dict)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
        ]
```

---

## 13. Dependency Security

### 13.1 Dependency Scanning

```bash
# Install safety for vulnerability scanning
pip install safety

# Scan dependencies
safety check -r requirements.txt

# Add to CI/CD pipeline
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: pip install safety
      - name: Security scan
        run: safety check -r requirements.txt
```

### 13.2 Keeping Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Use pip-tools for pinned requirements
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

### 13.3 requirements.txt Best Practices

```
# Pin exact versions for reproducibility
Django==5.1.6
djangorestframework==3.14.0
django-allauth==0.61.1

# Include hash verification for production
Django==5.1.6 \
    --hash=sha256:abc123...
```

---

## 14. Security Checklist

### Pre-Deployment Checklist

- [ ] SECRET_KEY is from environment variable
- [ ] DEBUG is False in production
- [ ] ALLOWED_HOSTS is configured
- [ ] HTTPS is enforced (SECURE_SSL_REDIRECT)
- [ ] HSTS is enabled
- [ ] Session cookies are secure
- [ ] CSRF protection is enabled
- [ ] CORS is properly configured
- [ ] Database uses strong password
- [ ] File uploads are validated
- [ ] Rate limiting is configured
- [ ] Logging is configured
- [ ] Error pages don't leak information

### Code Review Security Checklist

- [ ] No hardcoded secrets
- [ ] All user input is validated
- [ ] SQL queries use ORM or parameterized queries
- [ ] File uploads are validated
- [ ] Permissions are checked
- [ ] Sensitive data is encrypted
- [ ] Error messages don't leak information
- [ ] Logging doesn't include sensitive data

### Periodic Security Tasks

- [ ] Weekly: Run dependency security scan
- [ ] Monthly: Review access logs for anomalies
- [ ] Monthly: Review and rotate API keys
- [ ] Quarterly: Security audit
- [ ] Quarterly: Penetration testing (if applicable)

---

## Quick Reference

### Security Headers

| Header | Value | Purpose |
|--------|-------|---------|
| X-Frame-Options | DENY | Prevent clickjacking |
| X-Content-Type-Options | nosniff | Prevent MIME sniffing |
| X-XSS-Protection | 1; mode=block | XSS filter |
| Strict-Transport-Security | max-age=31536000 | Enforce HTTPS |
| Content-Security-Policy | default-src 'self' | Restrict content sources |

### HTTP Status Codes for Security

| Code | Usage |
|------|-------|
| 401 | Not authenticated |
| 403 | Not authorized (authenticated but no permission) |
| 429 | Rate limit exceeded |

---

**This security guide is MANDATORY for all Edupath development.**

*Last updated: 2026-01-28*
