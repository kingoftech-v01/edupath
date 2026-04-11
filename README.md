# Edupath

Multi-platform educational platform for online learning.

## Projects

| Project | Description | Technologies | Status |
|---------|-------------|--------------|--------|
| [edupath-web](./edupath-web) | Web application | Django + DRF, Tailwind | Active |
| [edupath-desktop](./edupath-desktop) | Cross-platform desktop client | **Python + PyQt6**, SQLAlchemy, httpx, Pydantic | Active |
| [edupath-android](./edupath-android) | Android mobile client | Kotlin, Gradle KTS | In progress |
| [edupath-ios](./edupath-ios) | iOS mobile client | Swift + SwiftUI (planned) | Placeholder |

## Structure

```
edupath/
├── API_SPECIFICATION.md        # Shared API documentation for all clients
│
├── edupath-web/                # Web application (Django)
│   ├── Edupath/                # Django project settings
│   ├── App/                    # Main app
│   ├── accounts/               # User authentication
│   ├── courses/                # Course management
│   ├── blog/                   # Blog posts
│   ├── core/                   # Site configuration
│   ├── data/                   # Fixtures / seed data
│   ├── static/, templates/, theme/
│   └── tests/
│
├── edupath-desktop/            # Desktop client (Python + PyQt6)
│   ├── src/                    # Application source
│   ├── tests/                  # Test suite
│   ├── requirements.txt        # PyQt6, SQLAlchemy, httpx, Pydantic, aiosqlite
│   ├── CONVENTIONS.md
│   ├── SECURITY.md
│   └── TECHNOLOGY_DECISION.md
│
├── edupath-android/            # Android client (Kotlin, Gradle KTS)
│   ├── app/                    # Application module
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   └── gradle/
│
└── edupath-ios/                # iOS client (placeholder)
    └── README.md               # Planned stack: Swift 5.9+, SwiftUI, MVVM + Clean Architecture
```

## Documentation

### Cross-Platform

| Document | Description |
|----------|-------------|
| [API_SPECIFICATION.md](./API_SPECIFICATION.md) | Shared API specification for all platforms |

### Web (Django)

| Document | Description |
|----------|-------------|
| [CONVENTIONS.md](./edupath-web/CONVENTIONS.md) | Coding standards and best practices |
| [SECURITY.md](./edupath-web/SECURITY.md) | Security guidelines |
| [SCALABILITY.md](./edupath-web/SCALABILITY.md) | Performance and scaling patterns |
| [README.md](./edupath-web/README.md) | Setup and development guide |

### Desktop (Python + PyQt6)

| Document | Description |
|----------|-------------|
| [CONVENTIONS.md](./edupath-desktop/CONVENTIONS.md) | Development standards |
| [SECURITY.md](./edupath-desktop/SECURITY.md) | Desktop security guidelines |
| [TECHNOLOGY_DECISION.md](./edupath-desktop/TECHNOLOGY_DECISION.md) | Why PyQt6 was chosen |
| [README.md](./edupath-desktop/README.md) | Setup and development guide |

### Android (Kotlin)

| Document | Description |
|----------|-------------|
| [README.md](./edupath-android/README.md) | Setup and build guide |

### iOS (planned, placeholder)

| Document | Description |
|----------|-------------|
| [README.md](./edupath-ios/README.md) | Planned stack and roadmap |

## Quick Start

### Web Application

```bash
cd edupath-web
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure environment variables
python manage.py migrate
python manage.py runserver
```

Access at http://localhost:8000

### Desktop Application (PyQt6)

```bash
cd edupath-desktop
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m src                   # or: python src/main.py
```

### Android Application (Kotlin)

```bash
cd edupath-android
./gradlew assembleDebug
# APK at: app/build/outputs/apk/debug/app-debug.apk
```

### iOS Application

The `edupath-ios/` directory is currently a placeholder. See its [README](./edupath-ios/README.md) for the planned Swift / SwiftUI stack.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                            CLIENTS                                   │
├──────────────┬──────────────────┬──────────────────┬────────────────┤
│  Web (Django)│ Desktop (PyQt6)  │  Android (Kotlin)│  iOS (planned) │
│  - SSR Views │ - Python 3.10+   │  - Gradle KTS    │  - SwiftUI     │
│  - REST API  │ - SQLAlchemy     │  - MVVM          │  - MVVM + Clean│
│  - Tailwind  │ - httpx + Pydantic│  - (Compose)    │  - Swift 5.9+  │
└──────┬───────┴────────┬─────────┴─────────┬────────┴───────┬────────┘
       │                │                    │                │
       └────────────────┴────────────────────┴────────────────┘
                                │
                                ▼
         ┌─────────────────────────────────────┐
         │            REST API                  │
         │     (Django REST Framework)          │
         │                                      │
         │  /api/v1/courses/                    │
         │  /api/v1/accounts/                   │
         │  /api/v1/blog/                       │
         └─────────────────┬───────────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────┐
         │           DATABASE                   │
         │     PostgreSQL (Production)          │
         │     SQLite (Development)             │
         └─────────────────────────────────────┘
```

## Security Standards

All platforms follow these security principles:

1. **No hardcoded secrets** - Use environment variables
2. **Secure credential storage** - OS-native secure storage
3. **HTTPS only** - TLS 1.2+ for all communications
4. **Input validation** - Validate all user input
5. **Authentication** - Token-based authentication
6. **Rate limiting** - Protect against abuse

See platform-specific SECURITY.md for detailed guidelines.

## Development Workflow

### Branch Strategy

```
main        ─────────────────────────────────────────────►
                    │                    │
develop     ────────┼────────────────────┼────────────────►
                    │                    │
feature/*   ────────┴────────────────────┘
```

### Commit Convention

```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
Scope: web, mobile, desktop, api, docs
```

Examples:
- `feat(web): add course enrollment`
- `fix(mobile): resolve login crash`
- `docs(api): update endpoint documentation`

## GitHub Repositories

Each project has its own repository for independent development:

| Repository | Description | CI/CD |
|------------|-------------|-------|
| `edupath-web` | Django web platform | GitHub Actions |
| `edupath-desktop` | Windows native application | GitHub Actions |
| `edupath-mobile` | Android Kotlin application | GitHub Actions |

## Contributing

1. **Read documentation first**
   - Platform-specific CONVENTIONS.md
   - SECURITY.md guidelines
   - API_SPECIFICATION.md for API work

2. **Create feature branch** from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature
   ```

3. **Follow coding standards**
   - Run linters before committing
   - Write tests for new features
   - Update documentation

4. **Submit pull request**
   - Clear description of changes
   - Link to related issues
   - Request review from maintainers

## Environment Setup

### Required Tools

| Tool | Version | Platform |
|------|---------|----------|
| Python | 3.11+ | Web |
| Node.js | 18+ | Web, Desktop |
| Rust | 1.70+ | Desktop |
| Android Studio | Latest | Mobile |
| JDK | 17+ | Mobile |

### IDE Recommendations

| Platform | Recommended IDE |
|----------|----------------|
| Web | VS Code + Python extension |
| Desktop | VS Code + rust-analyzer |
| Mobile | Android Studio |

## Testing

### Web
```bash
cd edupath-web
python manage.py test
```

### Desktop
```bash
cd edupath-desktop
npm run test
cargo test --manifest-path src-tauri/Cargo.toml
```

### Mobile
```bash
cd edupath-mobile
./gradlew test
./gradlew connectedAndroidTest
```

## Deployment

| Platform | Deployment Target |
|----------|-------------------|
| Web | Docker + Kubernetes |
| Desktop | Windows Store / Direct Download |
| Mobile | Google Play Store |

## Support

- **Bug Reports**: Create an issue in the respective repository
- **Feature Requests**: Create an issue with `[Feature]` prefix
- **Security Issues**: Email security@edupath.com (do not create public issues)

## License

Proprietary - All rights reserved.
