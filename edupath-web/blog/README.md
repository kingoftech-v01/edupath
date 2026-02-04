# Blog App

Blog and articles module for Edupath platform.

## Purpose

Handles blog functionality:
- Blog post creation and management
- Author attribution
- Content publishing
- Blog categories (optional)

## Models

| Model | Description |
|-------|-------------|
| `Blog` | Blog post entity |

### Blog Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Post title |
| `slug` | SlugField | URL-friendly identifier |
| `content` | TextField | Post content (HTML) |
| `excerpt` | TextField | Short summary |
| `author` | ForeignKey | Post author (Instructor) |
| `image` | ImageField | Featured image |
| `published_date` | DateField | Publication date |
| `read_time` | PositiveIntegerField | Estimated read time (minutes) |
| `is_published` | BooleanField | Publication status |
| `created_at` | DateTimeField | Creation timestamp |
| `updated_at` | DateTimeField | Last update |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/blog/` | List all posts |
| POST | `/api/v1/blog/` | Create post |
| GET | `/api/v1/blog/{id}/` | Get post detail |
| PUT | `/api/v1/blog/{id}/` | Update post |
| DELETE | `/api/v1/blog/{id}/` | Delete post |

## Frontend Views

| URL | View | Description |
|-----|------|-------------|
| `/blog/` | `blog_list` | All blog posts |
| `/blog/{slug}/` | `blog_detail` | Single post |
| `/blog/author/{username}/` | `author_posts` | Posts by author |

## Query Examples

```python
# Get published posts
posts = Blog.objects.filter(
    is_published=True
).select_related(
    'author'
).order_by('-published_date')

# Get recent posts
recent = Blog.objects.filter(
    is_published=True
).order_by('-published_date')[:5]

# Get posts by author
author_posts = Blog.objects.filter(
    author__slug='john-doe',
    is_published=True
)
```

## Features

- Auto-generate slug from title
- Calculate read time from content length
- Featured image with responsive sizes
- SEO-friendly URLs

## Dependencies

- courses app (for Instructor model as author)
- Pillow (image processing)
