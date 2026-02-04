# Core App

Site configuration and static pages module for Edupath.

## Purpose

Handles site-wide functionality:
- Site configuration (singleton)
- Contact form submissions
- Static pages (about, pricing, etc.)
- Platform features display
- Business partners/logos
- Site statistics

## Models

| Model | Description |
|-------|-------------|
| `Feature` | Platform features for homepage |
| `BusinessPartner` | Partner/sponsor logos |
| `SiteStatistic` | Counter statistics |
| `PricingPlan` | Subscription plans |
| `ContactInfo` | Contact information entries |
| `ContactSubmission` | Contact form submissions |
| `SiteConfiguration` | Site-wide settings (singleton) |

### Feature Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | CharField | Feature title |
| `description` | TextField | Feature description |
| `icon` | CharField | Icon class |
| `order` | PositiveIntegerField | Display order |
| `is_active` | BooleanField | Visibility |

### SiteConfiguration Fields (Singleton)

| Field | Type | Description |
|-------|------|-------------|
| `site_name` | CharField | Platform name |
| `tagline` | CharField | Site tagline |
| `logo` | ImageField | Site logo |
| `favicon` | ImageField | Site favicon |
| `primary_color` | CharField | Brand color |
| `contact_email` | EmailField | Contact email |
| `phone` | CharField | Contact phone |
| `address` | TextField | Physical address |
| `facebook/twitter/linkedin/youtube` | URLField | Social links |
| `google_analytics_id` | CharField | GA tracking ID |

### PricingPlan Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | CharField | Plan name |
| `price` | DecimalField | Monthly price |
| `features` | JSONField | List of features |
| `is_featured` | BooleanField | Highlight this plan |
| `order` | PositiveIntegerField | Display order |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/core/config/` | Get site configuration |
| GET | `/api/v1/core/features/` | List features |
| GET | `/api/v1/core/partners/` | List partners |
| GET | `/api/v1/core/stats/` | Get statistics |
| GET | `/api/v1/core/pricing/` | Get pricing plans |
| POST | `/api/v1/core/contact/` | Submit contact form |

## Frontend Views

| URL | View | Description |
|-----|------|-------------|
| `/` | `home` | Homepage |
| `/about/` | `about` | About page |
| `/features/` | `features` | Platform features |
| `/pricing/` | `pricing` | Pricing plans |
| `/contact/` | `contact` | Contact form |

## SiteConfiguration Usage

```python
# Get site configuration (singleton)
config = SiteConfiguration.get_solo()

# Access settings
site_name = config.site_name
contact_email = config.contact_email

# In templates (via context processor)
{{ site_config.site_name }}
{{ site_config.logo.url }}
```

## Context Processor

```python
# context_processors.py
def site_config(request):
    return {
        'site_config': SiteConfiguration.get_solo()
    }
```

## Contact Form Handling

```python
# Handle contact submission
def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.ip_address = get_client_ip(request)
            submission.save()

            # Send notification email (async)
            send_contact_notification.delay(submission.id)

            messages.success(request, 'Message sent!')
            return redirect('core:contact')
```

## Admin Features

- SiteConfiguration: Single-instance editing
- Contact submissions: Mark as read, reply tracking
- Drag-and-drop ordering for features/partners

## Dependencies

- django-solo (for singleton SiteConfiguration)
- Pillow (image processing)
