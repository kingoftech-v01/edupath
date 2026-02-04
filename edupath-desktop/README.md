# EduPath Desktop

A PyQt6-based desktop client for the EduPath educational platform.

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Framework | PyQt6 | Native desktop interface |
| HTTP Client | httpx | Async API communication |
| Models | Pydantic | Data validation and serialization |
| Local Storage | SQLAlchemy + SQLite | Offline data caching |
| Auth Storage | keyring | Secure credential storage |
| Testing | pytest + pytest-qt | Unit and UI testing |

## Requirements

### System Requirements

- Windows 10/11, macOS 10.14+, or Linux
- Python 3.10+
- 4GB RAM minimum
- 100MB disk space
- Internet connection (for sync)

### Development Dependencies

```
PyQt6>=6.5.0
httpx>=0.25.0
pydantic>=2.0.0
SQLAlchemy>=2.0.0
keyring>=24.0.0
pytest>=7.0.0
pytest-qt>=4.2.0
pytest-asyncio>=0.21.0
```

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
API_BASE_URL=https://api.edupath.com
API_VERSION=v1
CACHE_EXPIRY_HOURS=24
```

### 4. Run the Application

```bash
python src/main.py
```

## Project Structure

```
edupath-desktop/
├── src/
│   ├── main.py                    # Application entry point
│   ├── config.py                  # Configuration settings
│   │
│   ├── api/                       # API communication layer
│   │   ├── __init__.py
│   │   ├── client.py              # Async HTTP client (httpx)
│   │   └── auth.py                # JWT token management
│   │
│   ├── models/                    # Pydantic data models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   └── course.py              # Course, Category, Instructor models
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication service
│   │   ├── course_service.py      # Course data service
│   │   ├── cache_service.py       # SQLite caching service
│   │   └── sync_service.py        # Offline synchronization
│   │
│   ├── ui/                        # User interface layer
│   │   ├── __init__.py
│   │   ├── main_window.py         # Main application window
│   │   │
│   │   ├── views/                 # Screen views
│   │   │   ├── __init__.py
│   │   │   ├── login_view.py      # Login screen
│   │   │   ├── dashboard_view.py  # Dashboard screen
│   │   │   ├── courses_view.py    # Course list screen
│   │   │   ├── course_detail_view.py  # Course detail screen
│   │   │   └── admin/             # Admin views
│   │   │       ├── __init__.py
│   │   │       ├── users_view.py
│   │   │       └── courses_admin_view.py
│   │   │
│   │   ├── widgets/               # Reusable UI components
│   │   │   ├── __init__.py
│   │   │   ├── course_card.py     # Course card widget
│   │   │   ├── video_player.py    # Video player widget
│   │   │   └── progress_bar.py    # Progress indicator
│   │   │
│   │   └── styles/
│   │       └── theme.qss          # Application stylesheet
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── validators.py          # Input validation
│       └── helpers.py             # Helper functions
│
├── tests/                         # Test suite
│   ├── conftest.py                # Pytest fixtures
│   ├── test_api/                  # API client tests
│   ├── test_services/             # Service layer tests
│   └── test_ui/                   # UI component tests
│
├── resources/                     # Static resources
│   └── icons/                     # Application icons
│
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
├── setup.py                       # Package setup
└── README.md                      # This file
```

## Features

### Core Features

- **User Authentication**: Login, logout, session management with secure token storage
- **Course Browsing**: Browse and search courses with filtering by category
- **Course Details**: View course information, instructor, and syllabus
- **Video Playback**: Integrated video player for course content
- **Offline Mode**: Cache courses and content for offline access
- **Progress Tracking**: Track course progress locally and sync when online

### Technical Features

- **Secure Token Storage**: Uses system keyring for JWT tokens
- **Async API Calls**: Non-blocking HTTP requests with httpx
- **Local SQLite Cache**: Offline data persistence
- **Background Sync**: Automatic synchronization when online
- **Dark Theme**: Modern dark UI theme with QSS styling

## Architecture

### Service Layer

```python
# Authentication flow
auth_service = AuthService(api_client)
user = await auth_service.login(username, password)

# Course data
course_service = CourseService(api_client, cache_service)
courses = await course_service.get_courses()

# Offline caching
cache_service = CacheService(db_path)
cache_service.cache_courses(courses)
```

### UI Navigation

The application uses a stacked widget pattern for navigation:

```python
# MainWindow manages view navigation
main_window.show_view("login")      # Show login screen
main_window.show_view("dashboard")  # Show dashboard
main_window.show_view("courses")    # Show course list
```

## API Integration

The desktop app communicates with the EduPath Django API.

### Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `POST /accounts/api/v1/auth/login/` | User authentication |
| `POST /accounts/api/v1/auth/token/refresh/` | Token refresh |
| `GET /courses/api/v1/courses/` | Course listing |
| `GET /courses/api/v1/courses/{slug}/` | Course details |
| `GET /courses/api/v1/categories/` | Category listing |
| `GET /accounts/api/v1/profiles/me/` | User profile |

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_services/test_auth_service.py

# Run UI tests
pytest tests/test_ui/ -v
```

### Code Style

```bash
# Format code
black src/ tests/

# Check types
mypy src/

# Lint
flake8 src/ tests/
```

### Building

```bash
# Install build dependencies
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed src/main.py
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_BASE_URL` | Backend API URL | `http://localhost:8000` |
| `API_VERSION` | API version | `v1` |
| `CACHE_EXPIRY_HOURS` | Cache validity period | `24` |
| `DEBUG` | Enable debug mode | `false` |

### Application Settings

Edit `src/config.py` for application-level settings:

```python
class Config:
    APP_NAME = "EduPath Desktop"
    APP_VERSION = "1.0.0"
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
```

## Troubleshooting

### Common Issues

**"Failed to connect to API"**
- Check internet connection
- Verify `API_BASE_URL` in configuration
- Ensure backend server is running

**"Authentication failed"**
- Clear stored credentials: `keyring.delete_password("edupath", "access_token")`
- Re-login to the application

**"PyQt6 import error"**
- Ensure PyQt6 is installed: `pip install PyQt6`
- Check Python version (3.10+ required)

**"Database locked"**
- Close other instances of the application
- Delete cache: `rm ~/.edupath/cache.db`

## Related Projects

| Project | Description |
|---------|-------------|
| [edupath-web](../edupath-web) | Django web application |
| [edupath-android](../edupath-android) | Android mobile application |

## License

Proprietary - All rights reserved.
