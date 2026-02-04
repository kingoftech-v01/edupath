# App (Legacy)

Legacy application module - being migrated to specialized apps.

## Status: DEPRECATED

This app contains the original monolithic models and views.
New development should use the specialized apps:
- `accounts` - User management
- `courses` - Course management
- `blog` - Blog posts
- `core` - Site configuration

## Migration Status

| Component | Status | Migrated To |
|-----------|--------|-------------|
| Category | Migrated | `courses.Category` |
| Instructor | Migrated | `courses.Instructor` |
| Course | Migrated | `courses.Course` |
| Review | Migrated | `courses.Review` |
| Blog | Migrated | `blog.Blog` |
| Feature | Migrated | `core.Feature` |
| BusinessPartner | Migrated | `core.BusinessPartner` |
| SiteStatistic | Migrated | `core.SiteStatistic` |
| PricingPlan | Migrated | `core.PricingPlan` |
| ContactInfo | Migrated | `core.ContactInfo` |
| ContactSubmission | Migrated | `core.ContactSubmission` |
| SiteConfiguration | Migrated | `core.SiteConfiguration` |

## Usage

**DO NOT** add new code to this app.

For backward compatibility, imports are maintained:
```python
# Legacy import (deprecated)
from App.models import Course

# New import (preferred)
from courses.models import Course
```

## Cleanup Plan

1. Update all imports to use new apps
2. Remove duplicate model definitions
3. Remove legacy views
4. Archive or delete this app

## Notes

- Database tables remain with `app_` prefix for compatibility
- Migrations should not be modified
- Admin registrations moved to respective apps
