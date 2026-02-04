# EduPath Android

A native Android application for the EduPath educational platform, built with Kotlin and Jetpack Compose.

## Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Language | Kotlin | Primary development language |
| UI Framework | Jetpack Compose | Modern declarative UI |
| Architecture | MVVM | Model-View-ViewModel pattern |
| DI | Hilt/Dagger | Dependency injection |
| Networking | Retrofit + OkHttp | REST API communication |
| Local Storage | Room | SQLite database abstraction |
| Video Player | ExoPlayer (Media3) | Course video playback |
| Async | Coroutines + Flow | Asynchronous programming |
| Auth Storage | DataStore | Secure token storage |

## Requirements

### Development Environment

- Android Studio Hedgehog (2023.1.1) or later
- JDK 17
- Android SDK 34
- Kotlin 1.9+

### Target Devices

- Android 7.0 (API 24) minimum
- Android 14 (API 34) target
- Phone and tablet support

## Quick Start

### 1. Clone and Open

```bash
git clone https://github.com/your-org/edupath-android.git
```

Open the project in Android Studio.

### 2. Configure API

Create `local.properties` in project root:

```properties
sdk.dir=/path/to/android/sdk
API_BASE_URL=https://api.edupath.com/
```

### 3. Build and Run

```bash
# Debug build
./gradlew assembleDebug

# Install on device
./gradlew installDebug

# Run tests
./gradlew test
```

## Project Structure

```
edupath-android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/edupath/
│   │   │   │   │
│   │   │   │   ├── EduPathApplication.kt     # Application entry point
│   │   │   │   │
│   │   │   │   ├── di/                       # Dependency Injection
│   │   │   │   │   ├── NetworkModule.kt      # Retrofit, OkHttp setup
│   │   │   │   │   ├── DatabaseModule.kt     # Room database setup
│   │   │   │   │   └── RepositoryModule.kt   # Repository bindings
│   │   │   │   │
│   │   │   │   ├── data/                     # Data Layer
│   │   │   │   │   ├── api/                  # Remote data source
│   │   │   │   │   │   ├── EduPathApi.kt     # Retrofit API interface
│   │   │   │   │   │   ├── AuthInterceptor.kt # JWT interceptor
│   │   │   │   │   │   └── dto/              # Data transfer objects
│   │   │   │   │   │       ├── AuthDto.kt
│   │   │   │   │   │       ├── UserDto.kt
│   │   │   │   │   │       ├── CourseDto.kt
│   │   │   │   │   │       └── CoreDto.kt
│   │   │   │   │   │
│   │   │   │   │   ├── local/                # Local data source
│   │   │   │   │   │   ├── EduPathDatabase.kt # Room database
│   │   │   │   │   │   ├── dao/              # Data access objects
│   │   │   │   │   │   │   ├── CourseDao.kt
│   │   │   │   │   │   │   └── CategoryDao.kt
│   │   │   │   │   │   └── entities/         # Database entities
│   │   │   │   │   │       ├── CourseEntity.kt
│   │   │   │   │   │       └── CategoryEntity.kt
│   │   │   │   │   │
│   │   │   │   │   └── repository/           # Repository pattern
│   │   │   │   │       ├── TokenManager.kt   # Auth token management
│   │   │   │   │       ├── AuthRepository.kt # Authentication
│   │   │   │   │       ├── CourseRepository.kt # Course data
│   │   │   │   │       └── UserRepository.kt # User data
│   │   │   │   │
│   │   │   │   ├── domain/                   # Domain Layer
│   │   │   │   │   ├── model/                # Domain models
│   │   │   │   │   │   ├── User.kt
│   │   │   │   │   │   └── Course.kt
│   │   │   │   │   └── usecase/              # Business logic
│   │   │   │   │       ├── GetCoursesUseCase.kt
│   │   │   │   │       └── LoginUseCase.kt
│   │   │   │   │
│   │   │   │   └── ui/                       # Presentation Layer
│   │   │   │       ├── MainActivity.kt       # Single activity
│   │   │   │       │
│   │   │   │       ├── theme/                # Material3 theming
│   │   │   │       │   ├── Color.kt
│   │   │   │       │   ├── Theme.kt
│   │   │   │       │   └── Type.kt
│   │   │   │       │
│   │   │   │       ├── navigation/           # Navigation
│   │   │   │       │   └── NavGraph.kt       # Compose navigation
│   │   │   │       │
│   │   │   │       ├── components/           # Reusable composables
│   │   │   │       │   ├── CourseCard.kt
│   │   │   │       │   ├── VideoPlayer.kt
│   │   │   │       │   └── ProgressIndicator.kt
│   │   │   │       │
│   │   │   │       └── screens/              # Screen composables
│   │   │   │           ├── auth/
│   │   │   │           │   ├── LoginScreen.kt
│   │   │   │           │   └── LoginViewModel.kt
│   │   │   │           ├── home/
│   │   │   │           │   ├── HomeScreen.kt
│   │   │   │           │   └── HomeViewModel.kt
│   │   │   │           ├── courses/
│   │   │   │           │   ├── CoursesScreen.kt
│   │   │   │           │   ├── CourseDetailScreen.kt
│   │   │   │           │   ├── CoursesViewModel.kt
│   │   │   │           │   └── CourseDetailViewModel.kt
│   │   │   │           ├── player/
│   │   │   │           │   ├── VideoPlayerScreen.kt
│   │   │   │           │   └── PlayerViewModel.kt
│   │   │   │           └── admin/
│   │   │   │               ├── AdminDashboardScreen.kt
│   │   │   │               └── AdminViewModel.kt
│   │   │   │
│   │   │   └── res/                          # Android resources
│   │   │       ├── values/
│   │   │       │   ├── strings.xml
│   │   │       │   ├── colors.xml
│   │   │       │   └── themes.xml
│   │   │       └── drawable/
│   │   │
│   │   ├── test/                             # Unit tests
│   │   │   └── java/com/edupath/
│   │   │       ├── UseCaseTest.kt
│   │   │       ├── LoginViewModelTest.kt
│   │   │       ├── HomeViewModelTest.kt
│   │   │       └── CourseRepositoryTest.kt
│   │   │
│   │   └── androidTest/                      # Instrumentation tests
│   │
│   └── build.gradle.kts                      # App module build config
│
├── gradle/
│   └── libs.versions.toml                    # Version catalog
│
├── build.gradle.kts                          # Project build config
├── settings.gradle.kts                       # Project settings
└── README.md                                 # This file
```

## Architecture

### MVVM Pattern

```
┌─────────────────────────────────────────────────────────────┐
│                         UI Layer                             │
│  ┌─────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │   Screen    │◄───│  ViewModel   │◄───│   UiState      │  │
│  │ (Composable)│    │              │    │  (data class)  │  │
│  └─────────────┘    └──────────────┘    └────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Domain Layer                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                      UseCase                          │   │
│  │   - Business logic validation                         │   │
│  │   - Data transformation                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Data Layer                            │
│  ┌────────────────┐              ┌────────────────────────┐ │
│  │   Repository   │◄────────────►│   Data Sources         │ │
│  │                │              │   ┌─────────────────┐  │ │
│  │ - Offline-first│              │   │ Remote (Retrofit)│  │ │
│  │ - Cache logic  │              │   ├─────────────────┤  │ │
│  │                │              │   │ Local (Room)    │  │ │
│  └────────────────┘              │   └─────────────────┘  │ │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Injection

```kotlin
// NetworkModule provides Retrofit and API
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {
    @Provides
    @Singleton
    fun provideApi(retrofit: Retrofit): EduPathApi
}

// RepositoryModule binds implementations
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {
    @Binds
    abstract fun bindAuthRepository(impl: AuthRepositoryImpl): AuthRepository
}
```

## Features

### Core Features

- **User Authentication**: Login/logout with JWT token management
- **Course Browsing**: Browse courses with category filtering
- **Course Details**: View course info, instructor, and content
- **Video Playback**: ExoPlayer integration for course videos
- **Offline Mode**: Room database caching for offline access
- **Progress Tracking**: Track and sync course progress

### Admin Features

- **Dashboard**: Overview of platform statistics
- **User Management**: View and manage users (admin only)
- **Course Management**: Manage course content (admin only)

## API Integration

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/accounts/api/v1/auth/login/` | POST | User login |
| `/accounts/api/v1/auth/token/refresh/` | POST | Refresh JWT |
| `/accounts/api/v1/profiles/me/` | GET | Current user |
| `/courses/api/v1/courses/` | GET | List courses |
| `/courses/api/v1/courses/{slug}/` | GET | Course details |
| `/courses/api/v1/categories/` | GET | List categories |

### Authentication Flow

```kotlin
// 1. Login
val result = authRepository.login(username, password)

// 2. Token stored in DataStore
tokenManager.saveTokens(accessToken, refreshToken)

// 3. AuthInterceptor adds token to requests
class AuthInterceptor : Interceptor {
    override fun intercept(chain: Chain): Response {
        val token = tokenManager.getAccessToken()
        val request = chain.request().newBuilder()
            .addHeader("Authorization", "Bearer $token")
            .build()
        return chain.proceed(request)
    }
}
```

## Testing

### Unit Tests

```bash
# Run all unit tests
./gradlew test

# Run with coverage
./gradlew testDebugUnitTestCoverage
```

Test files:
- `UseCaseTest.kt` - Business logic tests
- `LoginViewModelTest.kt` - Login flow tests
- `HomeViewModelTest.kt` - Home screen tests
- `CourseRepositoryTest.kt` - Repository tests

### UI Tests

```bash
# Run instrumentation tests
./gradlew connectedAndroidTest
```

## Build Variants

| Variant | Description |
|---------|-------------|
| debug | Development build with debugging enabled |
| release | Production build with ProGuard/R8 |

### Release Build

```bash
# Create signed release APK
./gradlew assembleRelease

# Create App Bundle for Play Store
./gradlew bundleRelease
```

## Dependencies

Key dependencies from `libs.versions.toml`:

```toml
[versions]
compose = "1.6.0"
hilt = "2.50"
retrofit = "2.9.0"
room = "2.6.1"
media3 = "1.2.0"
coroutines = "1.7.3"

[libraries]
# Compose
compose-ui = { module = "androidx.compose.ui:ui" }
compose-material3 = { module = "androidx.compose.material3:material3" }

# DI
hilt-android = { module = "com.google.dagger:hilt-android" }
hilt-navigation-compose = { module = "androidx.hilt:hilt-navigation-compose" }

# Networking
retrofit = { module = "com.squareup.retrofit2:retrofit" }
okhttp = { module = "com.squareup.okhttp3:okhttp" }

# Local Storage
room-runtime = { module = "androidx.room:room-runtime" }
datastore = { module = "androidx.datastore:datastore-preferences" }

# Video
media3-exoplayer = { module = "androidx.media3:media3-exoplayer" }
media3-ui = { module = "androidx.media3:media3-ui" }

# Testing
junit = { module = "junit:junit" }
mockk = { module = "io.mockk:mockk" }
turbine = { module = "app.cash.turbine:turbine" }
```

## Troubleshooting

### Common Issues

**Build fails with "SDK not found"**

- Set `ANDROID_HOME` environment variable
- Or create `local.properties` with `sdk.dir=/path/to/sdk`

**Hilt compilation error**

- Clean and rebuild: `./gradlew clean build`
- Check all `@HiltViewModel` classes have `@Inject constructor`

**Network requests failing**

- Check API base URL in build config
- Verify internet permission in manifest
- Check if emulator has network access

**Room schema errors**

- Increment database version
- Add migration or use `fallbackToDestructiveMigration()`

## Related Projects

| Project | Description |
|---------|-------------|
| [edupath-web](../edupath-web) | Django web application |
| [edupath-desktop](../edupath-desktop) | PyQt6 desktop application |

## License

Proprietary - All rights reserved.
