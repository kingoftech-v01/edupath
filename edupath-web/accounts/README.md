# Accounts App

User authentication and profile management module for Edupath.

## Purpose

Handles all user-related functionality:
- User registration and authentication (via django-allauth)
- User profile management
- Social authentication (Google, GitHub, etc.)
- Password reset and change

## Models

| Model | Description |
|-------|-------------|
| `UserProfile` | Extended user profile with avatar, bio, social links |

### UserProfile Fields

| Field | Type | Description |
|-------|------|-------------|
| `user` | OneToOneField | Link to Django User |
| `avatar` | ImageField | Profile picture |
| `bio` | TextField | User biography |
| `website` | URLField | Personal website |
| `twitter` | CharField | Twitter handle |
| `linkedin` | URLField | LinkedIn profile |
| `github` | CharField | GitHub username |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/accounts/users/` | List users (admin) |
| GET | `/api/v1/accounts/users/{id}/` | Get user details |
| GET | `/api/v1/accounts/profile/` | Get current user profile |
| PATCH | `/api/v1/accounts/profile/` | Update current user profile |

## Frontend Views

| URL | View | Description |
|-----|------|-------------|
| `/accounts/profile/` | `profile_view` | View own profile |
| `/accounts/profile/edit/` | `profile_edit` | Edit profile |
| `/accounts/profile/{username}/` | `public_profile` | View user's public profile |

## Authentication Flow

1. User registers via `/accounts/signup/`
2. Email verification sent (if enabled)
3. User logs in via `/accounts/login/`
4. Session created with secure cookies
5. Profile auto-created via signal

## Signals

```python
# Auto-create UserProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```

## Usage Examples

```python
# Get user with profile
user = User.objects.select_related('userprofile').get(username='john')

# Access profile
profile = user.userprofile
avatar_url = profile.avatar.url if profile.avatar else '/static/default-avatar.png'

# Update profile
profile.bio = "Python developer"
profile.save()
```

## Dependencies

- django-allauth (authentication)
- Pillow (image processing for avatars)

## Configuration

Required settings in `settings.py`:
- `AUTH_USER_MODEL`
- `AUTHENTICATION_BACKENDS`
- `ACCOUNT_*` (allauth settings)
