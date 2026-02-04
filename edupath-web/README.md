# Edupath Web

Web application for the Edupath educational platform, built with Django and Django REST Framework.

## Features

- Course management with categories and instructors
- User authentication (local + social via django-allauth)
- REST API with DRF
- Blog system
- Contact form
- Responsive design with Tailwind CSS

## Requirements

- Python 3.11+
- Node.js 18+ (for Tailwind CSS)
- PostgreSQL (production) or SQLite (development)
- Redis (optional, for caching)

## Quick Start

### 1. Clone and Setup

```bash
cd edupath-web
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

Required environment variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `DATABASE_URL` - Database connection string

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Access at http://localhost:8000

Admin panel at http://localhost:8000/admin/

## Project Structure

```
edupath-web/
├── Edupath/                # Django project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # URL routing
│   └── wsgi.py             # WSGI entry point
│
├── accounts/               # User authentication & profiles
├── courses/                # Course management
├── blog/                   # Blog posts
├── core/                   # Site configuration
├── App/                    # Legacy app (deprecated)
│
├── static/                 # Static files
├── templates/              # HTML templates
├── media/                  # User uploads
│
├── CONVENTIONS.md          # Development conventions (MANDATORY)
├── SECURITY.md             # Security guidelines
├── SCALABILITY.md          # Scaling patterns
├── .env.example            # Environment template
└── requirements.txt        # Python dependencies
```

## Documentation

| Document | Description |
|----------|-------------|
| [CONVENTIONS.md](./CONVENTIONS.md) | Coding standards and conventions |
| [SECURITY.md](./SECURITY.md) | Security best practices |
| [SCALABILITY.md](./SCALABILITY.md) | Performance and scaling |
| [.env.example](./.env.example) | Environment configuration |

Each app also has its own README:
- [accounts/README.md](./accounts/README.md)
- [courses/README.md](./courses/README.md)
- [blog/README.md](./blog/README.md)
- [core/README.md](./core/README.md)

## API Endpoints

Base URL: `/api/v1/`

| Endpoint | Description |
|----------|-------------|
| `/api/v1/courses/` | Course management |
| `/api/v1/courses/categories/` | Course categories |
| `/api/v1/blog/` | Blog posts |
| `/api/v1/accounts/` | User accounts |
| `/api/v1/core/config/` | Site configuration |

See each app's README for detailed API documentation.

## Development

### Running Tests

```bash
python manage.py test
```

### Tailwind CSS

```bash
python manage.py tailwind start
```

### Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser

```bash
python manage.py createsuperuser
```

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Configure `SECRET_KEY` with a secure value
3. Set `ALLOWED_HOSTS` to your domain
4. Use PostgreSQL for database
5. Configure HTTPS and security headers
6. Set up Redis for caching
7. Configure email settings

See [SECURITY.md](./SECURITY.md) for complete security checklist.

## Contributing

1. Read [CONVENTIONS.md](./CONVENTIONS.md) first
2. Follow the dual-layer architecture (frontend + API)
3. Add tests for new features
4. Update documentation
5. Submit pull request

## License

Proprietary - All rights reserved.
