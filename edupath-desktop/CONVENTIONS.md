# Edupath Desktop Development Conventions

**Version**: 1.0
**Last Updated**: 2026-01-28
**Status**: MANDATORY - Follow after technology selection

---

## Table of Contents

1. [Overview](#1-overview)
2. [Project Structure](#2-project-structure)
3. [Naming Conventions](#3-naming-conventions)
4. [Architecture](#4-architecture)
5. [UI Patterns](#5-ui-patterns)
6. [State Management](#6-state-management)
7. [API Integration](#7-api-integration)
8. [Error Handling](#8-error-handling)
9. [Testing](#9-testing)
10. [Build & Release](#10-build--release)

---

## 1. Overview

### 1.1 Supported Platforms

| Platform | Version | Status |
|----------|---------|--------|
| Windows | 10, 11 | Primary |
| macOS | 12+ | Future |
| Linux | Ubuntu 22+ | Future |

### 1.2 Core Principles

1. **Offline First** - App works without internet
2. **Secure by Default** - Encrypt sensitive data
3. **Native Feel** - Respect platform conventions
4. **Performance** - Fast startup, low memory
5. **Accessibility** - Support screen readers

---

## 2. Project Structure

### 2.1 Tauri Project Structure (Recommended)

```
edupath-desktop/
├── src-tauri/                    # Rust backend
│   ├── src/
│   │   ├── main.rs              # Entry point
│   │   ├── commands/            # Tauri commands
│   │   │   ├── mod.rs
│   │   │   ├── auth.rs
│   │   │   └── courses.rs
│   │   ├── storage/             # Local storage
│   │   │   ├── mod.rs
│   │   │   ├── secure.rs
│   │   │   └── cache.rs
│   │   └── utils/
│   ├── Cargo.toml
│   └── tauri.conf.json
│
├── src/                          # Frontend (TypeScript)
│   ├── main.ts                  # Entry point
│   ├── App.vue                  # Root component
│   ├── components/              # Reusable components
│   │   ├── CourseCard.vue
│   │   ├── Sidebar.vue
│   │   └── Loading.vue
│   ├── views/                   # Page components
│   │   ├── HomeView.vue
│   │   ├── CoursesView.vue
│   │   └── ProfileView.vue
│   ├── stores/                  # State management
│   │   ├── auth.ts
│   │   └── courses.ts
│   ├── api/                     # API client
│   │   ├── client.ts
│   │   ├── courses.ts
│   │   └── auth.ts
│   ├── types/                   # TypeScript types
│   │   ├── course.ts
│   │   └── user.ts
│   └── utils/
│
├── public/                       # Static assets
├── tests/                        # Test files
├── package.json
├── vite.config.ts
├── tsconfig.json
├── CONVENTIONS.md
├── SECURITY.md
└── README.md
```

### 2.2 .NET MAUI Structure (Alternative)

```
edupath-desktop/
├── EdupathDesktop/
│   ├── App.xaml
│   ├── App.xaml.cs
│   ├── MauiProgram.cs
│   ├── Views/
│   │   ├── MainPage.xaml
│   │   ├── CoursesPage.xaml
│   │   └── ProfilePage.xaml
│   ├── ViewModels/
│   │   ├── MainViewModel.cs
│   │   └── CoursesViewModel.cs
│   ├── Models/
│   │   ├── Course.cs
│   │   └── User.cs
│   ├── Services/
│   │   ├── IApiService.cs
│   │   ├── ApiService.cs
│   │   └── StorageService.cs
│   └── Resources/
├── EdupathDesktop.Tests/
└── EdupathDesktop.sln
```

---

## 3. Naming Conventions

### 3.1 Files

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `CourseCard.vue` |
| Views | PascalCase + View | `CoursesView.vue` |
| Stores | camelCase | `authStore.ts` |
| Types | PascalCase | `Course.ts` |
| Utils | camelCase | `formatDate.ts` |
| Tests | *.test.ts | `auth.test.ts` |

### 3.2 Code

| Type | Convention | Example |
|------|------------|---------|
| Variables | camelCase | `courseList` |
| Constants | UPPER_SNAKE | `API_BASE_URL` |
| Functions | camelCase | `fetchCourses()` |
| Classes | PascalCase | `CourseService` |
| Interfaces | PascalCase + I | `ICourse` |
| Types | PascalCase | `CourseResponse` |

### 3.3 Tauri Commands

```rust
// Rust: snake_case for commands
#[tauri::command]
fn get_courses() -> Result<Vec<Course>, String> { }

#[tauri::command]
fn save_auth_token(token: String) -> Result<(), String> { }
```

```typescript
// TypeScript: camelCase when invoking
await invoke('get_courses');
await invoke('save_auth_token', { token: 'xyz' });
```

---

## 4. Architecture

### 4.1 Layer Separation

```
┌─────────────────────────────────────────────┐
│              Presentation Layer              │
│   (Vue Components, React Components, XAML)   │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│              State Management                │
│        (Pinia, Zustand, MVVM)               │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│               Service Layer                  │
│     (API Client, Storage, Utilities)        │
└─────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│              Native Bridge                   │
│    (Tauri Commands, .NET Interop)           │
└─────────────────────────────────────────────┘
```

### 4.2 Data Flow

```typescript
// 1. User action triggers store
const coursesStore = useCoursesStore();
await coursesStore.loadCourses();

// 2. Store calls service
export const useCoursesStore = defineStore('courses', () => {
  const courses = ref<Course[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function loadCourses() {
    loading.value = true;
    error.value = null;
    try {
      courses.value = await courseService.getCourses();
    } catch (e) {
      error.value = e.message;
    } finally {
      loading.value = false;
    }
  }

  return { courses, loading, error, loadCourses };
});

// 3. Service calls Tauri command or API
export const courseService = {
  async getCourses(): Promise<Course[]> {
    // Try local cache first
    const cached = await invoke<Course[]>('get_cached_courses');
    if (cached.length > 0) return cached;

    // Fetch from API
    const response = await apiClient.get('/courses/');
    await invoke('cache_courses', { courses: response.data });
    return response.data;
  }
};
```

---

## 5. UI Patterns

### 5.1 Component Structure (Vue)

```vue
<script setup lang="ts">
/**
 * CourseCard - Displays a single course preview.
 *
 * Props:
 *   course: Course object to display
 *
 * Events:
 *   click: Emitted when card is clicked
 */
import type { Course } from '@/types/course';

interface Props {
  course: Course;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  click: [courseId: string];
}>();

function handleClick() {
  emit('click', props.course.id);
}
</script>

<template>
  <div class="course-card" @click="handleClick">
    <img :src="course.thumbnail" :alt="course.title" />
    <h3>{{ course.title }}</h3>
    <p>{{ course.instructor.name }}</p>
    <span class="price">{{ formatPrice(course.price) }}</span>
  </div>
</template>

<style scoped>
.course-card {
  /* Component-scoped styles */
}
</style>
```

### 5.2 Responsive Layout

```css
/* Support different window sizes */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 16px;
}

/* Adapt to window resize */
@media (max-width: 768px) {
  .sidebar {
    display: none;
  }
}
```

### 5.3 Theme Support

```typescript
// theme.ts
export const lightTheme = {
  background: '#ffffff',
  text: '#1a1a1a',
  primary: '#4f46e5',
  secondary: '#6b7280',
};

export const darkTheme = {
  background: '#1a1a1a',
  text: '#ffffff',
  primary: '#818cf8',
  secondary: '#9ca3af',
};

// Use system preference
function getPreferredTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';
}
```

---

## 6. State Management

### 6.1 Store Pattern (Pinia)

```typescript
// stores/auth.ts
import { defineStore } from 'pinia';
import { invoke } from '@tauri-apps/api/tauri';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: null,
    isAuthenticated: false,
  }),

  actions: {
    async login(email: string, password: string) {
      const response = await apiClient.post('/auth/login/', {
        email,
        password,
      });

      this.token = response.data.access_token;
      this.user = response.data.user;
      this.isAuthenticated = true;

      // Store securely in native keychain
      await invoke('save_auth_token', { token: this.token });
    },

    async logout() {
      this.token = null;
      this.user = null;
      this.isAuthenticated = false;
      await invoke('clear_auth_token');
    },

    async restoreSession() {
      const token = await invoke<string | null>('get_auth_token');
      if (token) {
        this.token = token;
        this.isAuthenticated = true;
        // Fetch user profile
        await this.fetchProfile();
      }
    },
  },
});
```

---

## 7. API Integration

### 7.1 API Client

```typescript
// api/client.ts
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore();
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`;
  }
  return config;
});

// Handle errors globally
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore();
      await authStore.logout();
      // Navigate to login
    }
    return Promise.reject(error);
  }
);

export { apiClient };
```

### 7.2 Offline Support

```typescript
// services/offlineService.ts
import { invoke } from '@tauri-apps/api/tauri';

export const offlineService = {
  async getCourses(): Promise<Course[]> {
    // Check network status
    const online = navigator.onLine;

    if (online) {
      try {
        const response = await apiClient.get('/courses/');
        // Cache for offline
        await invoke('cache_courses', { courses: response.data });
        return response.data;
      } catch (e) {
        // Fallback to cache on network error
        return invoke('get_cached_courses');
      }
    }

    // Offline: use cache
    return invoke('get_cached_courses');
  },
};
```

---

## 8. Error Handling

### 8.1 Error Types

```typescript
// types/errors.ts
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public recoverable: boolean = true
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class NetworkError extends AppError {
  constructor(message = 'Network connection failed') {
    super(message, 'NETWORK_ERROR', true);
  }
}

export class AuthError extends AppError {
  constructor(message = 'Authentication failed') {
    super(message, 'AUTH_ERROR', true);
  }
}
```

### 8.2 Global Error Handler

```typescript
// main.ts
app.config.errorHandler = (error, instance, info) => {
  console.error('Global error:', error);

  // Log to error tracking service
  if (import.meta.env.PROD) {
    // Sentry.captureException(error);
  }

  // Show user-friendly message
  if (error instanceof AppError && error.recoverable) {
    showToast(error.message, 'error');
  } else {
    showToast('An unexpected error occurred', 'error');
  }
};
```

---

## 9. Testing

### 9.1 Unit Tests

```typescript
// tests/stores/auth.test.ts
import { setActivePinia, createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth';
import { vi } from 'vitest';

describe('AuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('should login successfully', async () => {
    const store = useAuthStore();

    vi.mock('@/api/client', () => ({
      apiClient: {
        post: vi.fn().mockResolvedValue({
          data: {
            access_token: 'test-token',
            user: { id: '1', name: 'Test' },
          },
        }),
      },
    }));

    await store.login('test@example.com', 'password');

    expect(store.isAuthenticated).toBe(true);
    expect(store.token).toBe('test-token');
  });

  it('should clear state on logout', async () => {
    const store = useAuthStore();
    store.token = 'test-token';
    store.isAuthenticated = true;

    await store.logout();

    expect(store.isAuthenticated).toBe(false);
    expect(store.token).toBeNull();
  });
});
```

### 9.2 E2E Tests

```typescript
// tests/e2e/login.test.ts
import { test, expect } from '@playwright/test';

test('user can login', async ({ page }) => {
  await page.goto('/');

  await page.fill('[data-testid="email-input"]', 'test@example.com');
  await page.fill('[data-testid="password-input"]', 'password123');
  await page.click('[data-testid="login-button"]');

  await expect(page.locator('[data-testid="home-screen"]')).toBeVisible();
});
```

---

## 10. Build & Release

### 10.1 Build Configuration

```json
// tauri.conf.json
{
  "build": {
    "beforeBuildCommand": "npm run build",
    "beforeDevCommand": "npm run dev",
    "devPath": "http://localhost:5173",
    "distDir": "../dist"
  },
  "package": {
    "productName": "Edupath",
    "version": "1.0.0"
  },
  "tauri": {
    "bundle": {
      "active": true,
      "identifier": "com.edupath.desktop",
      "icon": ["icons/icon.ico"],
      "windows": {
        "wix": {
          "language": "en-US"
        }
      }
    },
    "updater": {
      "active": true,
      "endpoints": ["https://releases.edupath.com/{{target}}/{{current_version}}"],
      "pubkey": "YOUR_PUBLIC_KEY"
    }
  }
}
```

### 10.2 Release Process

```bash
# Build for production
npm run tauri build

# Output:
# - Windows: src-tauri/target/release/bundle/msi/Edupath_1.0.0_x64.msi
# - macOS: src-tauri/target/release/bundle/dmg/Edupath_1.0.0_x64.dmg
```

### 10.3 Auto-Update

```rust
// src-tauri/src/main.rs
use tauri::Manager;

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            let handle = app.handle();
            tauri::async_runtime::spawn(async move {
                match tauri::updater::builder(handle).check().await {
                    Ok(update) => {
                        if update.is_update_available() {
                            update.download_and_install().await.unwrap();
                        }
                    }
                    Err(e) => {
                        println!("Update check failed: {}", e);
                    }
                }
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

---

## Quick Reference

### Commands

```bash
# Development
npm run tauri dev

# Build
npm run tauri build

# Test
npm run test
npm run test:e2e

# Lint
npm run lint
npm run lint:fix
```

### Key Files

| File | Purpose |
|------|---------|
| `tauri.conf.json` | Tauri configuration |
| `vite.config.ts` | Build configuration |
| `src/stores/` | State management |
| `src-tauri/src/commands/` | Native commands |

---

**This convention applies after technology selection.**

*Last updated: 2026-01-28*
