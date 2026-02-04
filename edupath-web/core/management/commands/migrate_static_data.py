"""
Management command to populate the database with initial data.

Usage:
    python manage.py migrate_static_data

This command populates all models with sample data for development and testing.
It maintains compatibility with existing templates by matching expected data structures.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with initial sample data for all apps'

    def handle(self, *args, **options):
        self.stdout.write('Starting data migration...\n')

        # Create data in order of dependencies
        self.create_site_config()
        self.create_features()
        self.create_business_partners()
        self.create_statistics()
        self.create_contact_info()
        self.create_pricing_plans()
        self.create_categories()
        self.create_instructors()
        self.create_courses()
        self.create_reviews()
        self.create_blogs()

        self.stdout.write(self.style.SUCCESS('\nData migration completed successfully!'))

    def create_site_config(self):
        """Create site configuration."""
        from core.models import SiteConfiguration

        config, created = SiteConfiguration.objects.get_or_create(pk=1)
        if created or not config.site_name:
            config.site_name = 'EduPath'
            config.tagline = 'Learn Without Limits'
            config.description = 'EduPath is a premier online learning platform offering courses in technology, business, design, and more.'
            config.logo = ''
            config.favicon = ''
            config.facebook_url = 'https://facebook.com/edupath'
            config.twitter_url = 'https://twitter.com/edupath'
            config.linkedin_url = 'https://linkedin.com/company/edupath'
            config.instagram_url = 'https://instagram.com/edupath'
            config.youtube_url = 'https://youtube.com/edupath'
            config.copyright_text = '© 2024 EduPath. All rights reserved.'
            config.save()
            self.stdout.write(self.style.SUCCESS('  [OK] Site configuration created'))
        else:
            self.stdout.write('  - Site configuration already exists')

    def create_features(self):
        """Create platform features."""
        from core.models import Feature

        features_data = [
            {
                'icon': 'uil uil-airplay',
                'title': 'Digital Marketing',
                'desc': 'Learn modern digital marketing strategies to grow your business and reach more customers.',
                'link_url': '/courses/?category=marketing',
            },
            {
                'icon': 'uil uil-camera',
                'title': 'Photography',
                'desc': 'Master the art of photography from basics to advanced techniques.',
                'link_url': '/courses/?category=photography',
            },
            {
                'icon': 'uil uil-ruler-combined',
                'title': 'Development',
                'desc': 'Build professional websites and applications with modern technologies.',
                'link_url': '/courses/?category=development',
            },
            {
                'icon': 'uil uil-microphone',
                'title': 'Music & Audio',
                'desc': 'Create, produce, and master music with industry-standard tools.',
                'link_url': '/courses/?category=music',
            },
        ]

        created_count = 0
        for i, data in enumerate(features_data, 1):
            obj, created = Feature.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Features: {created_count} created, {len(features_data) - created_count} existed')

    def create_business_partners(self):
        """Create business partners."""
        from core.models import BusinessPartner

        partners_data = [
            {'name': 'Amazon', 'img': 'assets/images/client/amazon.png', 'website_url': 'https://amazon.com'},
            {'name': 'Google', 'img': 'assets/images/client/google.png', 'website_url': 'https://google.com'},
            {'name': 'LinkedIn', 'img': 'assets/images/client/linkedin.png', 'website_url': 'https://linkedin.com'},
            {'name': 'Facebook', 'img': 'assets/images/client/facebook.png', 'website_url': 'https://facebook.com'},
            {'name': 'Spotify', 'img': 'assets/images/client/spotify.png', 'website_url': 'https://spotify.com'},
            {'name': 'Shopify', 'img': 'assets/images/client/shopify.png', 'website_url': 'https://shopify.com'},
        ]

        created_count = 0
        for i, data in enumerate(partners_data, 1):
            obj, created = BusinessPartner.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Business Partners: {created_count} created, {len(partners_data) - created_count} existed')

    def create_statistics(self):
        """Create site statistics for CTA sections."""
        from core.models import SiteStatistic

        stats_data = [
            {'title': 'Courses', 'number': 0, 'target': 25, 'symbol': '+'},
            {'title': 'Countries', 'number': 0, 'target': 100, 'symbol': '+'},
            {'title': 'Students', 'number': 0, 'target': 50, 'symbol': 'K'},
            {'title': 'Instructors', 'number': 0, 'target': 35, 'symbol': '+'},
        ]

        created_count = 0
        for i, data in enumerate(stats_data, 1):
            obj, created = SiteStatistic.objects.get_or_create(
                title=data['title'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Statistics: {created_count} created, {len(stats_data) - created_count} existed')

    def create_contact_info(self):
        """Create contact information."""
        from core.models import ContactInfo

        contacts_data = [
            {
                'icon': 'uil uil-phone',
                'name': 'Phone',
                'title': 'Mon to Fri 10am to 6pm',
                'info': '+1 234-567-8900',
                'link_url': 'tel:+12345678900',
            },
            {
                'icon': 'uil uil-envelope',
                'name': 'Email',
                'title': 'We reply within 24 hours',
                'info': 'contact@edupath.com',
                'link_url': 'mailto:contact@edupath.com',
            },
            {
                'icon': 'uil uil-map-marker',
                'name': 'Location',
                'title': 'Visit our headquarters',
                'info': '123 Education Street, New York, NY 10001',
                'link_url': 'https://maps.google.com',
            },
        ]

        created_count = 0
        for i, data in enumerate(contacts_data, 1):
            obj, created = ContactInfo.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Contact Info: {created_count} created, {len(contacts_data) - created_count} existed')

    def create_pricing_plans(self):
        """Create pricing plans."""
        from core.models import PricingPlan

        plans_data = [
            {
                'name': 'Weekly',
                'price': '9.99',
                'duration': 'Week',
                'button_text': 'Get Started',
                'style': 'bg-white dark:bg-slate-900',
                'button_style': 'btn bg-violet-600 hover:bg-violet-700 border-violet-600 hover:border-violet-700 text-white rounded-md',
                'features': [
                    'Access to 10 courses',
                    'Basic support',
                    'Mobile app access',
                    'Download resources',
                ],
            },
            {
                'name': 'Monthly',
                'price': '29.99',
                'duration': 'Month',
                'button_text': 'Get Started',
                'style': 'bg-violet-600 dark:bg-violet-600',
                'button_style': 'btn bg-white hover:bg-slate-100 text-violet-600 rounded-md',
                'features': [
                    'Access to all courses',
                    'Priority support',
                    'Mobile app access',
                    'Download resources',
                    'Certificate of completion',
                ],
            },
            {
                'name': 'Yearly',
                'price': '199.99',
                'duration': 'Year',
                'button_text': 'Get Started',
                'style': 'bg-white dark:bg-slate-900',
                'button_style': 'btn bg-violet-600 hover:bg-violet-700 border-violet-600 hover:border-violet-700 text-white rounded-md',
                'features': [
                    'Access to all courses',
                    'Priority support',
                    'Mobile app access',
                    'Download resources',
                    'Certificate of completion',
                    'Exclusive webinars',
                    '2 months free',
                ],
            },
        ]

        created_count = 0
        for i, data in enumerate(plans_data, 1):
            obj, created = PricingPlan.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Pricing Plans: {created_count} created, {len(plans_data) - created_count} existed')

    def create_categories(self):
        """Create course categories."""
        from courses.models import Category

        categories_data = [
            {'name': 'Development', 'slug': 'development', 'icon': 'uil uil-brackets-curly', 'description': 'Web, mobile, and software development courses'},
            {'name': 'Business', 'slug': 'business', 'icon': 'uil uil-chart-line', 'description': 'Business strategy, management, and entrepreneurship'},
            {'name': 'Design', 'slug': 'design', 'icon': 'uil uil-brush-alt', 'description': 'Graphic design, UI/UX, and visual arts'},
            {'name': 'Marketing', 'slug': 'marketing', 'icon': 'uil uil-megaphone', 'description': 'Digital marketing, SEO, and social media'},
            {'name': 'Photography', 'slug': 'photography', 'icon': 'uil uil-camera', 'description': 'Photography fundamentals and advanced techniques'},
            {'name': 'Music', 'slug': 'music', 'icon': 'uil uil-music', 'description': 'Music production, instruments, and theory'},
            {'name': 'Health', 'slug': 'health', 'icon': 'uil uil-heart', 'description': 'Fitness, nutrition, and wellness'},
            {'name': 'Language', 'slug': 'language', 'icon': 'uil uil-comment', 'description': 'Learn new languages from native speakers'},
        ]

        created_count = 0
        for i, data in enumerate(categories_data, 1):
            obj, created = Category.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Categories: {created_count} created, {len(categories_data) - created_count} existed')

    def create_instructors(self):
        """Create instructors."""
        from courses.models import Instructor

        instructors_data = [
            {
                'name': 'John Smith',
                'slug': 'john-smith',
                'title': 'Senior Web Developer',
                'bio': 'John has 10+ years of experience in web development and has worked with Fortune 500 companies.',
                'img': 'assets/images/team/01.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Sarah Johnson',
                'slug': 'sarah-johnson',
                'title': 'UX Design Lead',
                'bio': 'Sarah is a certified UX designer with expertise in user research and interface design.',
                'img': 'assets/images/team/02.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Michael Chen',
                'slug': 'michael-chen',
                'title': 'Data Scientist',
                'bio': 'Michael specializes in machine learning and has taught over 50,000 students worldwide.',
                'img': 'assets/images/team/03.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Emily Brown',
                'slug': 'emily-brown',
                'title': 'Marketing Strategist',
                'bio': 'Emily is a digital marketing expert with experience in SEO, content marketing, and social media.',
                'img': 'assets/images/team/04.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'David Wilson',
                'slug': 'david-wilson',
                'title': 'Mobile App Developer',
                'bio': 'David has built numerous mobile applications for iOS and Android platforms.',
                'img': 'assets/images/team/05.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Lisa Anderson',
                'slug': 'lisa-anderson',
                'title': 'Business Consultant',
                'bio': 'Lisa helps entrepreneurs and businesses grow with strategic planning and execution.',
                'img': 'assets/images/team/06.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Robert Taylor',
                'slug': 'robert-taylor',
                'title': 'Photography Expert',
                'bio': 'Robert is an award-winning photographer with work featured in major publications.',
                'img': 'assets/images/team/07.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
            {
                'name': 'Jennifer Martinez',
                'slug': 'jennifer-martinez',
                'title': 'Music Producer',
                'bio': 'Jennifer has produced music for various artists and teaches music production techniques.',
                'img': 'assets/images/team/08.jpg',
                'facebook_url': 'https://facebook.com',
                'twitter_url': 'https://twitter.com',
                'linkedin_url': 'https://linkedin.com',
            },
        ]

        created_count = 0
        for i, data in enumerate(instructors_data, 1):
            obj, created = Instructor.objects.get_or_create(
                slug=data['slug'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Instructors: {created_count} created, {len(instructors_data) - created_count} existed')

    def create_courses(self):
        """Create courses."""
        from courses.models import Category, Instructor, Course

        # Get categories and instructors
        categories = {c.slug: c for c in Category.objects.all()}
        instructors = {i.slug: i for i in Instructor.objects.all()}

        courses_data = [
            {
                'name': 'Complete Web Development Bootcamp',
                'slug': 'complete-web-development-bootcamp',
                'title': 'Learn HTML, CSS, JavaScript, and more',
                'desc': 'A comprehensive course covering all aspects of modern web development from beginner to advanced.',
                'img': 'assets/images/courses/01.jpg',
                'price': '99.99',
                'category_slug': 'development',
                'instructor_slug': 'john-smith',
                'lessons': 48,
                'students': 2500,
                'is_featured': True,
            },
            {
                'name': 'Python for Data Science',
                'slug': 'python-data-science',
                'title': 'Master Python for data analysis',
                'desc': 'Learn Python programming with focus on data science, pandas, numpy, and visualization.',
                'img': 'assets/images/courses/02.jpg',
                'price': '79.99',
                'category_slug': 'development',
                'instructor_slug': 'michael-chen',
                'lessons': 36,
                'students': 1800,
                'is_featured': True,
            },
            {
                'name': 'UI/UX Design Fundamentals',
                'slug': 'ui-ux-design-fundamentals',
                'title': 'Create stunning user interfaces',
                'desc': 'Learn the principles of UI/UX design and create beautiful, user-friendly interfaces.',
                'img': 'assets/images/courses/03.jpg',
                'price': '69.99',
                'category_slug': 'design',
                'instructor_slug': 'sarah-johnson',
                'lessons': 28,
                'students': 1200,
                'is_featured': True,
            },
            {
                'name': 'Digital Marketing Mastery',
                'slug': 'digital-marketing-mastery',
                'title': 'Become a marketing expert',
                'desc': 'Master digital marketing strategies including SEO, social media, and content marketing.',
                'img': 'assets/images/courses/04.jpg',
                'price': '89.99',
                'category_slug': 'marketing',
                'instructor_slug': 'emily-brown',
                'lessons': 42,
                'students': 980,
                'is_featured': True,
            },
            {
                'name': 'Mobile App Development with React Native',
                'slug': 'react-native-mobile-development',
                'title': 'Build cross-platform mobile apps',
                'desc': 'Create iOS and Android apps with a single codebase using React Native.',
                'img': 'assets/images/courses/05.jpg',
                'price': '109.99',
                'category_slug': 'development',
                'instructor_slug': 'david-wilson',
                'lessons': 52,
                'students': 750,
                'is_featured': True,
            },
            {
                'name': 'Business Strategy Fundamentals',
                'slug': 'business-strategy-fundamentals',
                'title': 'Strategic thinking for success',
                'desc': 'Learn how to develop and execute effective business strategies.',
                'img': 'assets/images/courses/06.jpg',
                'price': '59.99',
                'category_slug': 'business',
                'instructor_slug': 'lisa-anderson',
                'lessons': 24,
                'students': 620,
                'is_featured': True,
            },
            {
                'name': 'Photography Masterclass',
                'slug': 'photography-masterclass',
                'title': 'Capture stunning photos',
                'desc': 'From camera basics to advanced techniques, become a professional photographer.',
                'img': 'assets/images/courses/07.jpg',
                'price': '74.99',
                'category_slug': 'photography',
                'instructor_slug': 'robert-taylor',
                'lessons': 32,
                'students': 890,
                'is_featured': False,
                'video_url': 'https://www.youtube.com/embed/example1',
            },
            {
                'name': 'Music Production Basics',
                'slug': 'music-production-basics',
                'title': 'Create your own music',
                'desc': 'Learn music production from scratch using professional tools and techniques.',
                'img': 'assets/images/courses/08.jpg',
                'price': '84.99',
                'category_slug': 'music',
                'instructor_slug': 'jennifer-martinez',
                'lessons': 38,
                'students': 560,
                'is_featured': False,
                'video_url': 'https://www.youtube.com/embed/example2',
            },
            {
                'name': 'Advanced JavaScript',
                'slug': 'advanced-javascript',
                'title': 'Deep dive into JavaScript',
                'desc': 'Master advanced JavaScript concepts including ES6+, async programming, and more.',
                'img': 'assets/images/courses/09.jpg',
                'price': '89.99',
                'category_slug': 'development',
                'instructor_slug': 'john-smith',
                'lessons': 40,
                'students': 1100,
                'is_featured': False,
            },
            {
                'name': 'SEO Optimization Course',
                'slug': 'seo-optimization-course',
                'title': 'Rank higher on search engines',
                'desc': 'Learn SEO strategies to improve your website visibility and organic traffic.',
                'img': 'assets/images/courses/10.jpg',
                'price': '49.99',
                'category_slug': 'marketing',
                'instructor_slug': 'emily-brown',
                'lessons': 18,
                'students': 730,
                'is_featured': False,
            },
            {
                'name': 'Machine Learning Fundamentals',
                'slug': 'machine-learning-fundamentals',
                'title': 'Introduction to ML algorithms',
                'desc': 'Understand machine learning concepts and implement algorithms from scratch.',
                'img': 'assets/images/courses/11.jpg',
                'price': '119.99',
                'category_slug': 'development',
                'instructor_slug': 'michael-chen',
                'lessons': 56,
                'students': 1350,
                'is_featured': False,
            },
            {
                'name': 'Graphic Design Essentials',
                'slug': 'graphic-design-essentials',
                'title': 'Design like a pro',
                'desc': 'Learn graphic design principles and tools like Photoshop and Illustrator.',
                'img': 'assets/images/courses/12.jpg',
                'price': '64.99',
                'category_slug': 'design',
                'instructor_slug': 'sarah-johnson',
                'lessons': 30,
                'students': 920,
                'is_featured': False,
            },
        ]

        created_count = 0
        for i, data in enumerate(courses_data, 1):
            category = categories.get(data.pop('category_slug'))
            instructor = instructors.get(data.pop('instructor_slug'))

            if category and instructor:
                obj, created = Course.objects.get_or_create(
                    slug=data['slug'],
                    defaults={
                        **data,
                        'category': category,
                        'instructor': instructor,
                        'order': i
                    }
                )
                if created:
                    created_count += 1

        self.stdout.write(f'  [OK] Courses: {created_count} created, {len(courses_data) - created_count} existed')

    def create_reviews(self):
        """Create course reviews."""
        from courses.models import Review

        reviews_data = [
            {
                'name': 'Alex Turner',
                'title': 'Web Developer Student',
                'img': 'assets/images/client/01.jpg',
                'desc': 'The web development bootcamp was exactly what I needed. The instructor explains concepts clearly and the projects are practical.',
                'rating': 5,
            },
            {
                'name': 'Maria Garcia',
                'title': 'UX Designer',
                'img': 'assets/images/client/02.jpg',
                'desc': 'Excellent course on UI/UX design. I learned so much about user research and prototyping. Highly recommended!',
                'rating': 5,
            },
            {
                'name': 'James Wilson',
                'title': 'Marketing Manager',
                'img': 'assets/images/client/03.jpg',
                'desc': 'The digital marketing course helped me understand modern marketing strategies. Very practical and up-to-date content.',
                'rating': 4,
            },
            {
                'name': 'Sophie Chen',
                'title': 'Data Analyst',
                'img': 'assets/images/client/04.jpg',
                'desc': 'Python for Data Science is comprehensive and well-structured. Perfect for beginners wanting to enter the data field.',
                'rating': 5,
            },
            {
                'name': 'Daniel Brown',
                'title': 'Entrepreneur',
                'img': 'assets/images/client/05.jpg',
                'desc': 'The business strategy course gave me insights I needed to grow my startup. Practical advice from an experienced instructor.',
                'rating': 4,
            },
            {
                'name': 'Emma Davis',
                'title': 'Photographer',
                'img': 'assets/images/client/06.jpg',
                'desc': 'Amazing photography course! I improved my skills significantly. The instructor shares professional tips that really work.',
                'rating': 5,
            },
        ]

        created_count = 0
        for i, data in enumerate(reviews_data, 1):
            obj, created = Review.objects.get_or_create(
                name=data['name'],
                defaults={**data, 'order': i}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Reviews: {created_count} created, {len(reviews_data) - created_count} existed')

    def create_blogs(self):
        """Create blog posts."""
        from blog.models import Blog
        from courses.models import Instructor

        # Get an instructor for the blog author
        instructor = Instructor.objects.first()

        blogs_data = [
            {
                'title': '10 Tips for Effective Online Learning',
                'slug': '10-tips-effective-online-learning',
                'excerpt': 'Discover strategies to maximize your online learning experience and achieve your educational goals.',
                'content': '''Online learning has become increasingly popular, but it requires discipline and the right approach. Here are 10 tips to help you succeed:

1. **Create a dedicated study space** - Find a quiet, comfortable place for studying.
2. **Set a regular schedule** - Consistency is key to building study habits.
3. **Take notes actively** - Engage with the material by writing notes.
4. **Participate in discussions** - Connect with fellow learners.
5. **Take regular breaks** - Use the Pomodoro technique for better focus.
6. **Eliminate distractions** - Turn off notifications during study time.
7. **Set clear goals** - Know what you want to achieve each session.
8. **Review regularly** - Spaced repetition helps retention.
9. **Ask questions** - Don't hesitate to seek clarification.
10. **Celebrate progress** - Acknowledge your achievements.

By following these tips, you can make the most of your online learning journey.''',
                'img': 'assets/images/blog/01.jpg',
            },
            {
                'title': 'The Future of EdTech in 2024',
                'slug': 'future-edtech-2024',
                'excerpt': 'Explore emerging trends in educational technology and how they will shape learning.',
                'content': '''Educational technology is evolving rapidly. Here's what to expect in 2024:

**AI-Powered Personalization**
Artificial intelligence is making learning more personalized than ever. Adaptive learning systems can now tailor content to individual student needs.

**Virtual Reality Classrooms**
VR technology is creating immersive learning experiences that were impossible before. Students can explore historical sites, conduct virtual experiments, and more.

**Microlearning**
Short, focused learning modules are becoming more popular as people seek to learn on-the-go.

**Gamification**
Game elements in education are increasing engagement and motivation among learners.

The future of education is exciting, and technology will play a central role in making learning more accessible and effective.''',
                'img': 'assets/images/blog/02.jpg',
            },
            {
                'title': 'How to Choose the Right Online Course',
                'slug': 'choose-right-online-course',
                'excerpt': 'A comprehensive guide to selecting online courses that match your learning goals.',
                'content': '''With thousands of online courses available, choosing the right one can be overwhelming. Here's how to make the best choice:

**Define Your Goals**
What do you want to achieve? A career change, skill upgrade, or personal interest? Your goal will guide your choice.

**Research the Instructor**
Look for instructors with relevant experience and positive reviews. Their teaching style matters.

**Check the Curriculum**
Review the course outline. Does it cover what you need to learn? Is the content up-to-date?

**Consider the Format**
Video lectures, interactive exercises, projects - different formats suit different learning styles.

**Read Reviews**
Learn from others' experiences. Look for reviews from people with similar goals.

**Evaluate the Investment**
Consider both time and money. Some courses require significant commitment.

Take your time in choosing, as the right course can make a significant difference in your learning journey.''',
                'img': 'assets/images/blog/03.jpg',
            },
            {
                'title': 'Building a Career in Web Development',
                'slug': 'career-web-development',
                'excerpt': 'Your roadmap to becoming a successful web developer in today\'s competitive market.',
                'content': '''Web development is a rewarding career with great opportunities. Here's how to get started:

**Learn the Fundamentals**
Start with HTML, CSS, and JavaScript. These are the building blocks of the web.

**Choose Your Path**
Frontend, backend, or full-stack? Each has different skill requirements and job opportunities.

**Build Projects**
Theory is important, but employers want to see what you can build. Create a portfolio of projects.

**Stay Updated**
Web technologies evolve quickly. Keep learning new frameworks and tools.

**Network**
Join developer communities, attend meetups, and contribute to open source.

**Apply Strategically**
Tailor your applications to each job. Highlight relevant skills and projects.

With dedication and continuous learning, you can build a successful career in web development.''',
                'img': 'assets/images/blog/04.jpg',
            },
            {
                'title': 'The Importance of Soft Skills in Tech',
                'slug': 'soft-skills-tech',
                'excerpt': 'Why communication and collaboration skills are essential for tech professionals.',
                'content': '''Technical skills get you the interview, but soft skills often determine your success. Here's why they matter:

**Communication**
Can you explain complex concepts to non-technical stakeholders? Clear communication is essential.

**Collaboration**
Modern tech work is team-based. You need to work effectively with designers, product managers, and other developers.

**Problem-Solving**
Beyond coding, you need to approach problems creatively and think critically.

**Adaptability**
Technology changes fast. Being open to change and learning new things is crucial.

**Time Management**
Meeting deadlines and managing multiple tasks requires strong organizational skills.

**Empathy**
Understanding user needs and teammate perspectives leads to better products and teamwork.

Invest in developing these skills alongside your technical abilities for a well-rounded career.''',
                'img': 'assets/images/blog/05.jpg',
            },
            {
                'title': 'Introduction to Machine Learning',
                'slug': 'introduction-machine-learning',
                'excerpt': 'A beginner\'s guide to understanding machine learning concepts and applications.',
                'content': '''Machine learning is transforming industries. Here's a beginner's overview:

**What is Machine Learning?**
ML is a subset of AI where computers learn from data without being explicitly programmed.

**Types of Machine Learning**
- Supervised Learning: Learn from labeled data
- Unsupervised Learning: Find patterns in unlabeled data
- Reinforcement Learning: Learn through trial and error

**Common Applications**
- Recommendation systems (Netflix, Spotify)
- Image recognition
- Natural language processing
- Fraud detection

**Getting Started**
Learn Python, understand statistics, and practice with datasets from Kaggle.

Machine learning is a vast field with exciting opportunities for those willing to learn.''',
                'img': 'assets/images/blog/06.jpg',
            },
            {
                'title': 'Design Principles Every Developer Should Know',
                'slug': 'design-principles-developers',
                'excerpt': 'Essential design concepts that can help developers create better user interfaces.',
                'content': '''Even if you're not a designer, understanding design principles can improve your work:

**Hierarchy**
Guide users' attention to the most important elements first.

**Consistency**
Use consistent patterns throughout your application.

**Whitespace**
Don't fear empty space - it improves readability and focus.

**Color**
Use color purposefully. Consider accessibility and contrast ratios.

**Typography**
Choose readable fonts and maintain a clear typographic hierarchy.

**Alignment**
Align elements to create order and professionalism.

These principles can help you create more polished and user-friendly interfaces.''',
                'img': 'assets/images/blog/07.jpg',
            },
            {
                'title': 'Remote Work Best Practices',
                'slug': 'remote-work-best-practices',
                'excerpt': 'Tips for staying productive and maintaining work-life balance while working remotely.',
                'content': '''Remote work offers flexibility but requires discipline. Here are best practices:

**Set Up Your Workspace**
Create a comfortable, dedicated work area that separates work from personal life.

**Establish Boundaries**
Set clear working hours and communicate them to your team and family.

**Over-Communicate**
In remote settings, err on the side of more communication rather than less.

**Use the Right Tools**
Invest in good equipment and learn to use collaboration tools effectively.

**Take Breaks**
Step away from the screen regularly to maintain productivity and health.

**Stay Connected**
Make an effort to maintain social connections with colleagues.

With the right approach, remote work can be highly productive and rewarding.''',
                'img': 'assets/images/blog/08.jpg',
            },
            {
                'title': 'Understanding SEO Basics',
                'slug': 'understanding-seo-basics',
                'excerpt': 'A practical guide to search engine optimization for content creators and marketers.',
                'content': '''SEO helps your content get found online. Here are the basics:

**Keywords**
Research and use relevant keywords that your audience is searching for.

**Quality Content**
Create valuable, original content that answers users' questions.

**Technical SEO**
Ensure your site loads fast, is mobile-friendly, and has a clear structure.

**Backlinks**
Earn links from reputable sites to increase your authority.

**User Experience**
Google considers how users interact with your site. Make it easy to navigate.

**Regular Updates**
Keep content fresh and up-to-date for better rankings.

SEO is an ongoing process, but these fundamentals will give you a strong foundation.''',
                'img': 'assets/images/blog/09.jpg',
            },
        ]

        created_count = 0
        for i, data in enumerate(blogs_data, 1):
            obj, created = Blog.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    **data,
                    'author': instructor,
                    'order': i
                }
            )
            if created:
                created_count += 1

        self.stdout.write(f'  [OK] Blogs: {created_count} created, {len(blogs_data) - created_count} existed')
