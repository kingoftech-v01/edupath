"""
Management command to migrate hardcoded data from context_processors to database.

Usage:
    python manage.py migrate_static_data

This command populates the database with the static data that was previously
hardcoded in context_processors.py, ensuring the site works identically
but with database-driven content.
"""

from django.core.management.base import BaseCommand
from App.models import (
    Category, Instructor, Course, Blog, Review, Feature,
    BusinessPartner, SiteStatistic, PricingPlan, ContactInfo,
    SiteConfiguration
)


class Command(BaseCommand):
    help = 'Migrate static data from context_processors to database'

    def handle(self, *args, **options):
        self.stdout.write('Starting data migration...\n')

        # Migrate in order (respecting foreign key dependencies)
        self.migrate_business_partners()
        self.migrate_features()
        self.migrate_categories()
        self.migrate_instructors()
        self.migrate_courses()
        self.migrate_blogs()
        self.migrate_reviews()
        self.migrate_statistics()
        self.migrate_pricing_plans()
        self.migrate_contact_info()
        self.create_site_config()

        self.stdout.write(self.style.SUCCESS('\nData migration completed successfully!'))

    def migrate_business_partners(self):
        """Migrate business partner logos."""
        partners = [
            {'name': 'Amazon', 'img': '/static/assets/images/client/amazon.svg'},
            {'name': 'Google', 'img': '/static/assets/images/client/google.svg'},
            {'name': 'Lenovo', 'img': '/static/assets/images/client/lenovo.svg'},
            {'name': 'PayPal', 'img': '/static/assets/images/client/paypal.svg'},
            {'name': 'Shopify', 'img': '/static/assets/images/client/shopify.svg'},
            {'name': 'Spotify', 'img': '/static/assets/images/client/spotify.svg'},
        ]
        for i, p in enumerate(partners):
            BusinessPartner.objects.get_or_create(
                name=p['name'],
                defaults={'img': p['img'], 'order': i}
            )
        self.stdout.write(f'  Migrated {len(partners)} business partners')

    def migrate_features(self):
        """Migrate platform features."""
        features = [
            {
                'icon': 'iconoir-thumbs-up text-3xl',
                'title': 'Relaxing & Learning',
                'desc': "The phrasal sequence of the is now so that many campaign and benefit",
            },
            {
                'icon': 'iconoir-medal text-3xl',
                'title': 'Certificate',
                'desc': "The phrasal sequence of the is now so that many campaign and benefit",
            },
            {
                'icon': 'iconoir-laptop-dev-mode text-3xl',
                'title': 'Private Mentoring',
                'desc': "The phrasal sequence of the is now so that many campaign and benefit",
            },
            {
                'icon': 'iconoir-emoji text-3xl',
                'title': 'Creative Thinking',
                'desc': "The phrasal sequence of the is now so that many campaign and benefit",
            }
        ]
        for i, f in enumerate(features):
            Feature.objects.get_or_create(
                title=f['title'],
                defaults={'icon': f['icon'], 'desc': f['desc'], 'order': i}
            )
        self.stdout.write(f'  Migrated {len(features)} features')

    def migrate_categories(self):
        """Migrate course categories."""
        categories = [
            {'icon': 'iconoir-laptop-dev-mode text-2xl', 'name': 'Art & Design'},
            {'icon': 'iconoir-antenna-signal text-2xl', 'name': 'Web Development'},
            {'icon': 'iconoir-network-reverse text-2xl', 'name': 'Digital Marketing'},
            {'icon': 'iconoir-html5 text-2xl', 'name': 'HTML CSS'},
            {'icon': 'iconoir-cube-replace-face text-2xl', 'name': 'Leadership'},
            {'icon': 'iconoir-cpu text-2xl', 'name': 'Data Science'},
            {'icon': 'iconoir-chat-bubble-check text-2xl', 'name': 'ChatGPT'},
            {'icon': 'iconoir-learning text-2xl', 'name': 'Deep Learning'},
        ]
        for i, c in enumerate(categories):
            Category.objects.get_or_create(
                name=c['name'],
                defaults={'icon': c['icon'], 'order': i}
            )
        self.stdout.write(f'  Migrated {len(categories)} categories')

    def migrate_instructors(self):
        """Migrate instructor profiles."""
        instructors = [
            {'img': '/static/assets/images/team/1.jpg', 'name': 'Megan Cade', 'title': "UI/UX Expert"},
            {'img': '/static/assets/images/team/2.jpg', 'name': 'Ramon Gibson', 'title': "Science Teacher"},
            {'img': '/static/assets/images/team/3.jpg', 'name': 'Stella Robinson', 'title': "Math Specialist"},
            {'img': '/static/assets/images/team/4.jpg', 'name': 'Paul Phelan', 'title': "Assistant Teacher"},
            {'img': '/static/assets/images/team/5.jpg', 'name': 'Nancy Hall', 'title': "UI/UX Expert"},
            {'img': '/static/assets/images/team/6.jpg', 'name': 'Wendy Buckley', 'title': "Science Teacher"},
            {'img': '/static/assets/images/team/7.jpg', 'name': 'Sammy Adkins', 'title': "Math Specialist"},
            {'img': '/static/assets/images/team/8.jpg', 'name': 'Cornelia Jefferson', 'title': "Assistant Teacher"},
        ]
        for i, inst in enumerate(instructors):
            Instructor.objects.get_or_create(
                name=inst['name'],
                defaults={'title': inst['title'], 'order': i}
            )
        self.stdout.write(f'  Migrated {len(instructors)} instructors')

    def migrate_courses(self):
        """Migrate course data."""
        # Get default instructor for courses
        default_instructor = Instructor.objects.first()
        web_dev_category = Category.objects.filter(name='Web Development').first()

        courses = [
            {
                'id': 1,
                'img': '/static/assets/images/course/1.jpg',
                'name': 'Calvin Carlo',
                'price': 0,
                'lessons': 10,
                'students': 49,
                'title': 'The Ultimate Course Bundle',
                'desc': "The phrasal sequence of the is now so many campaign",
                'is_featured': True,
            },
            {
                'id': 2,
                'img': '/static/assets/images/course/2.jpg',
                'name': 'Calvin Carlo',
                'price': 19,
                'lessons': 10,
                'students': 49,
                'title': 'App Development Course',
                'desc': "The phrasal sequence of the is now so many campaign",
                'is_featured': True,
            },
            {
                'id': 3,
                'img': '/static/assets/images/course/3.jpg',
                'name': 'Calvin Carlo',
                'price': 29,
                'lessons': 10,
                'students': 49,
                'title': 'Spoken English Popular Course',
                'desc': "The phrasal sequence of the is now so many campaign",
                'is_featured': True,
            },
            {
                'id': 4,
                'img': '/static/assets/images/course/4.jpg',
                'name': 'Calvin Carlo',
                'price': 15,
                'lessons': 10,
                'students': 49,
                'title': 'Back-end Development Course',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 5,
                'img': '/static/assets/images/course/5.jpg',
                'name': 'Calvin Carlo',
                'price': 24,
                'lessons': 10,
                'students': 49,
                'title': 'Front-end Development Course',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 6,
                'img': '/static/assets/images/course/6.jpg',
                'name': 'Calvin Carlo',
                'price': 29,
                'lessons': 10,
                'students': 49,
                'title': 'Full stack Project in Nextjs Course',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 7,
                'img': '/static/assets/images/course/7.jpg',
                'name': 'Calvin Carlo',
                'price': 15,
                'lessons': 10,
                'students': 49,
                'title': 'Why Is Education So Famous?',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 8,
                'img': '/static/assets/images/course/8.jpg',
                'name': 'Calvin Carlo',
                'price': 24,
                'lessons': 10,
                'students': 49,
                'title': 'Difficult Things About Education.',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 9,
                'img': '/static/assets/images/course/9.jpg',
                'name': 'Calvin Carlo',
                'price': 29,
                'lessons': 10,
                'students': 49,
                'title': 'Online Courses from Edupath',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 10,
                'img': '/static/assets/images/course/10.jpg',
                'name': 'Calvin Carlo',
                'price': 15,
                'lessons': 10,
                'students': 49,
                'title': 'Financial Investing Course',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 11,
                'img': '/static/assets/images/course/11.jpg',
                'name': 'Calvin Carlo',
                'price': 24,
                'lessons': 10,
                'students': 49,
                'title': 'Learning Digital Marketing',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
            {
                'id': 12,
                'img': '/static/assets/images/course/12.jpg',
                'name': 'Calvin Carlo',
                'price': 29,
                'lessons': 10,
                'students': 49,
                'title': 'Master the Fundamentals of Math',
                'desc': "The phrasal sequence of the is now so many campaign",
            },
        ]

        for i, c in enumerate(courses):
            Course.objects.get_or_create(
                title=c['title'],
                defaults={
                    'name': c['name'],
                    'price': c['price'],
                    'lessons': c['lessons'],
                    'students': c['students'],
                    'desc': c['desc'],
                    'is_featured': c.get('is_featured', False),
                    'instructor': default_instructor,
                    'category': web_dev_category,
                    'order': i,
                }
            )
        self.stdout.write(f'  Migrated {len(courses)} courses')

    def migrate_blogs(self):
        """Migrate blog posts."""
        default_instructor = Instructor.objects.first()

        blogs = [
            {'id': 1, 'name': 'Degree', 'title': "The Future of Remote Work: Trending Now"},
            {'id': 2, 'name': 'University', 'title': "The Psychology of Learning: How Cognitive"},
            {'id': 3, 'name': 'Developer', 'title': "Crafting Compelling Presentations: Design"},
            {'id': 4, 'name': 'HTML5', 'title': "Demystifying Data Science: A Beginner's"},
            {'id': 5, 'name': 'Institution', 'title': "The Art of Effective Online Collaboration"},
            {'id': 6, 'name': 'Graduation', 'title': "Student Success Stories: From Learning"},
            {'id': 7, 'name': 'Certification', 'title': "Instructor Spotlight: Meet the Faces Behind"},
            {'id': 8, 'name': 'Frontend', 'title': "Navigating the Job Market: Career Tips"},
            {'id': 9, 'name': 'Mobile', 'title': "Building a Growth is Mindset: Strategie"},
        ]

        for i, b in enumerate(blogs):
            Blog.objects.get_or_create(
                title=b['title'],
                defaults={
                    'name': b['name'],
                    'author': default_instructor,
                    'order': i,
                }
            )
        self.stdout.write(f'  Migrated {len(blogs)} blogs')

    def migrate_reviews(self):
        """Migrate student reviews."""
        reviews = [
            {
                'name': 'Megan Cade',
                'title': "Student",
                'desc': "Online education has allowed me to balance work and study easily. The flexibility of choosing when to study has made it a perfect fit for my busy schedule!",
            },
            {
                'name': 'Ramon Gibson',
                'title': "Student",
                'desc': "I was surprised by how interactive online courses can be. The live discussions and group projects kept me engaged, and I felt connected to my classmates.",
            },
            {
                'name': 'Stella Robinson',
                'title': "Student",
                'desc': "Studying online saved me a lot of money, and I didn't have to commute. The quality of the courses was fantastic, and I could learn at my own pace.",
            },
            {
                'name': 'Paul Phelan',
                'title': "Student",
                'desc': "Online learning requires discipline, but it's worth it. I had to work on time management, but the flexibility and quality of the content made it rewarding.",
            },
            {
                'name': 'Christa Smith',
                'title': "Student",
                'desc': "Taking online courses has helped me grow professionally. I could apply what I learned immediately at work, and the knowledge I gained was practical and up-to-date.",
            },
            {
                'name': 'Calvin Carlo',
                'title': "Student",
                'desc': "The biggest advantage of online education is convenience, but it requires self-motivation. If you're committed, it's a great way to advance your skills.",
            }
        ]

        for i, r in enumerate(reviews):
            Review.objects.get_or_create(
                name=r['name'],
                desc=r['desc'],
                defaults={'title': r['title'], 'order': i, 'rating': 5}
            )
        self.stdout.write(f'  Migrated {len(reviews)} reviews')

    def migrate_statistics(self):
        """Migrate CTA statistics."""
        statistics = [
            {'title': 'Courses', 'number': 1010, 'target': 1548, 'symbol': '+'},
            {'title': 'Countries', 'number': 2, 'target': 12, 'symbol': '+'},
            {'title': 'Students', 'number': 0, 'target': 500, 'symbol': 'K'},
            {'title': 'Instructors', 'number': 0, 'target': 80, 'symbol': '+'},
        ]

        for i, s in enumerate(statistics):
            SiteStatistic.objects.get_or_create(
                title=s['title'],
                defaults={
                    'number': s['number'],
                    'target': s['target'],
                    'symbol': s['symbol'],
                    'order': i
                }
            )
        self.stdout.write(f'  Migrated {len(statistics)} statistics')

    def migrate_pricing_plans(self):
        """Migrate pricing plans."""
        plans = [
            {
                'name': 'Weekly',
                'price': 9,
                'duration': 'Week',
                'button_text': 'Login Now',
                'style': 'group md:flex items-center justify-between p-6 rounded-lg shadow hover:shadow-md shadow-slate-100 dark:shadow-slate-800 transition-all duration-500',
                'button_style': 'h-8 px-3 tracking-wide inline-flex items-center justify-center font-medium rounded-md border border-violet-600/20 hover:bg-violet-600 text-violet-600 hover:text-white text-sm md:mt-0 mt-4',
            },
            {
                'name': 'Monthly',
                'price': 29,
                'duration': 'Month',
                'button_text': 'Join Now',
                'style': 'group md:flex items-center justify-between p-6 rounded-lg shadow hover:shadow-md shadow-slate-100 dark:shadow-slate-800 transition-all duration-500 mt-6',
                'button_style': 'h-8 px-3 tracking-wide inline-flex items-center justify-center font-medium rounded-md bg-violet-600/10 hover:bg-violet-600 text-violet-600 hover:text-white text-sm md:mt-0 mt-4',
            },
            {
                'name': 'Yearly',
                'price': 299,
                'duration': 'Year',
                'button_text': 'Subscribe Now',
                'style': 'group md:flex items-center justify-between p-6 rounded-lg shadow hover:shadow-md shadow-slate-100 dark:shadow-slate-800 transition-all duration-500 mt-6',
                'button_style': 'h-8 px-3 tracking-wide inline-flex items-center justify-center font-medium rounded-md bg-violet-600 text-white text-sm md:mt-0 mt-4',
            }
        ]

        for i, p in enumerate(plans):
            PricingPlan.objects.get_or_create(
                name=p['name'],
                defaults={
                    'price': p['price'],
                    'duration': p['duration'],
                    'button_text': p['button_text'],
                    'style': p['style'],
                    'button_style': p['button_style'],
                    'order': i
                }
            )
        self.stdout.write(f'  Migrated {len(plans)} pricing plans')

    def migrate_contact_info(self):
        """Migrate contact information."""
        contacts = [
            {
                'icon': 'iconoir-phone text-3xl',
                'name': 'Phone',
                'title': 'The phrasal sequence of the is now so that many campaign and benefit',
                'info': '+152 534-468-854'
            },
            {
                'icon': 'iconoir-mail text-3xl',
                'name': 'Email',
                'title': 'The phrasal sequence of the is now so that many campaign and benefit',
                'info': 'contact@example.com'
            },
            {
                'icon': 'iconoir-map-pin text-3xl',
                'name': 'Location',
                'title': 'C/54 Northwest Freeway, Suite 558, Houston, USA 485',
                'info': 'View on Google map'
            }
        ]

        for i, c in enumerate(contacts):
            ContactInfo.objects.get_or_create(
                name=c['name'],
                defaults={
                    'icon': c['icon'],
                    'title': c['title'],
                    'info': c['info'],
                    'order': i
                }
            )
        self.stdout.write(f'  Migrated {len(contacts)} contact info entries')

    def create_site_config(self):
        """Create site configuration."""
        config, created = SiteConfiguration.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'EduPath',
                'tagline': 'Learn Without Limits',
                'email': 'contact@edupath.com',
                'phone': '+152 534-468-854',
                'copyright_text': '2024',
            }
        )
        status = 'Created' if created else 'Already exists'
        self.stdout.write(f'  Site configuration: {status}')
