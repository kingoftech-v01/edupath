# EduPath iOS

Native iOS application for the EduPath educational platform.

> **Status: Placeholder** - This project is planned for future development.

## Planned Features

- Browse courses and categories
- User authentication
- Course enrollment and progress tracking
- Offline-first architecture
- Dark mode support
- Native iOS design (Human Interface Guidelines)

## Planned Technology Stack

| Category | Technology |
|----------|------------|
| Language | Swift 5.9+ |
| UI | SwiftUI |
| Architecture | MVVM + Clean Architecture |
| Network | URLSession / Alamofire |
| Database | Core Data / SwiftData |
| Async | Swift Concurrency (async/await) |
| DI | Swift Dependencies / Factory |
| Testing | XCTest, Quick/Nimble |

## Requirements (Planned)

- Xcode 15+
- iOS 16.0+ deployment target
- macOS Sonoma or later for development

## Project Structure (Planned)

```
edupath-ios/
├── EduPath/
│   ├── App/
│   │   ├── EduPathApp.swift
│   │   └── AppDelegate.swift
│   ├── Core/
│   │   ├── Network/
│   │   ├── Database/
│   │   └── Extensions/
│   ├── Domain/
│   │   ├── Models/
│   │   ├── Repositories/
│   │   └── UseCases/
│   ├── Data/
│   │   ├── API/
│   │   ├── DTOs/
│   │   └── Repositories/
│   ├── Presentation/
│   │   ├── Theme/
│   │   ├── Components/
│   │   ├── Navigation/
│   │   └── Screens/
│   │       ├── Auth/
│   │       ├── Home/
│   │       ├── Courses/
│   │       ├── Player/
│   │       └── Profile/
│   └── Resources/
│       ├── Assets.xcassets
│       └── Localizable.strings
├── EduPathTests/
├── EduPathUITests/
├── EduPath.xcodeproj
└── README.md
```

## Architecture (Planned)

The app will follow **Clean Architecture** with three main layers:

```
┌──────────────────────────────────────────┐
│           Presentation Layer             │
│  (Views, ViewModels, UI State)           │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│             Domain Layer                 │
│  (Use Cases, Domain Models, Protocols)   │
└──────────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────────┐
│              Data Layer                  │
│  (Repositories, API, Database, Mappers)  │
└──────────────────────────────────────────┘
```

## API Integration

The app will connect to the same EduPath API as other clients:
- Base URL: `https://api.edupath.com/api/v1/`
- Authentication: JWT Bearer token
- See `API_SPECIFICATION.md` in root for full documentation

## Related Projects

| Project | Description |
|---------|-------------|
| [Edupath](../Edupath/) | Django Web Backend + Frontend |
| [edupath-android](../edupath-android/) | Android App (Kotlin/Compose) |
| [edupath-desktop](../edupath-desktop/) | Desktop App (PyQt6) |

## Contributing

This project is currently a placeholder. Implementation will begin in a future phase.

## License

Proprietary - All rights reserved.
