# Courses App

Course management module for Edupath educational platform.

## Purpose

Handles all course-related functionality:
- Course creation and management
- Category organization
- Instructor profiles
- Student reviews and ratings
- Course enrollment

## Models

| Model | Description |
|-------|-------------|
| `Category` | Course categories with ordering |
| `Instructor` | Course instructors with profiles |
| `Course` | Main course entity |
| `Review` | Student reviews and ratings |

### Category Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Category name |
| `slug` | SlugField | URL-friendly identifier |
| `icon` | CharField | Icon class (e.g., MDI icon) |
| `order` | PositiveIntegerField | Display order |
| `is_active` | BooleanField | Visibility flag |

### Instructor Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField | Link to User account |
| `name` | CharField | Display name |
| `title` | CharField | Professional title |
| `bio` | TextField | Biography |
| `avatar` | ImageField | Profile picture |
| `facebook/twitter/linkedin/youtube/instagram` | URLField | Social links |

### Course Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Course title |
| `slug` | SlugField | URL-friendly identifier |
| `description` | TextField | Full description |
| `price` | DecimalField | Course price (0 = free) |
| `category` | ForeignKey | Course category |
| `instructor` | ForeignKey | Course instructor |
| `img` | ImageField | Thumbnail image |
| `video_url` | URLField | Promotional video |
| `lessons` | PositiveIntegerField | Number of lessons |
| `duration_hours` | DecimalField | Total duration |
| `students` | PositiveIntegerField | Enrolled students count |
| `is_published` | BooleanField | Publication status |

### Review Fields

| Field | Type | Description |
|-------|------|-------------|
| `course` | ForeignKey | Reviewed course |
| `user` | ForeignKey | Reviewer |
| `rating` | PositiveIntegerField | Rating (1-5 stars) |
| `comment` | TextField | Review text |
| `created_at` | DateTimeField | Review date |

## API Endpoints

### Courses

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses/` | List all courses |
| POST | `/api/v1/courses/` | Create course |
| GET | `/api/v1/courses/{id}/` | Get course detail |
| PUT | `/api/v1/courses/{id}/` | Update course |
| DELETE | `/api/v1/courses/{id}/` | Delete course |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses/categories/` | List categories |
| GET | `/api/v1/courses/categories/{id}/` | Get category |

### Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses/{id}/reviews/` | List course reviews |
| POST | `/api/v1/courses/{id}/reviews/` | Add review |

## Frontend Views

| URL | View | Description |
|-----|------|-------------|
| `/courses/` | `course_list` | Browse all courses |
| `/courses/grid/` | `course_grid` | Grid view |
| `/courses/{slug}/` | `course_detail` | Course details |
| `/courses/category/{slug}/` | `category_courses` | Courses by category |
| `/instructors/` | `instructor_list` | All instructors |
| `/instructors/{slug}/` | `instructor_detail` | Instructor profile |

## Query Examples

```python
# Get published courses with related data
courses = Course.objects.filter(
    is_published=True
).select_related(
    'instructor', 'category'
).prefetch_related(
    'reviews'
).order_by('-created_at')

# Get course with average rating
from django.db.models import Avg
course = Course.objects.annotate(
    avg_rating=Avg('reviews__rating')
).get(slug='python-basics')

# Get instructor's courses
instructor_courses = Course.objects.filter(
    instructor__slug='john-doe',
    is_published=True
)
```

## Filters & Search

API supports:
- `?category=programming` - Filter by category
- `?search=python` - Search title/description
- `?ordering=-created_at` - Sort by field
- `?price_min=0&price_max=50` - Price range

## Dependencies

- accounts app (for User model)
- Pillow (image processing)
