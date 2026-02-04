# from django.shortcuts import render , redirect
from django.shortcuts import render, get_object_or_404
# for form 
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Course
from .models import Blog
import re

# Create your views here.

def index(request):
    return render(request,'pages/index.html')

def index_two(request):
    return render(request,'pages/index-two.html')

def index_three(request):
    return render(request,'pages/index-three.html')

def index_four(request):
    return render(request,'pages/index-four.html')

def index_five(request):
    return render(request,'pages/index-five.html')

def grid(request):
    return render(request,'pages/grid.html')

def grid_sidebar(request):
    return render(request,'pages/grid-sidebar.html')

def list(request):
    return render(request,'pages/list.html')

def list_sidebar(request):
    return render(request,'pages/list-sidebar.html')

def youtube_listing(request):
    return render(request,'pages/youtube-listing.html')

def video_listing(request):
    return render(request,'pages/video-listing.html')

def course_list_or_default(request):
    # Get courses from the database
    courses = Course.objects.all()  # or any filter you need
    return render(request, 'pages/course-detail.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'pages/course-detail.html', {'course': course})

def course_list_or_default1(request):
    # Get courses from the database
    courses = Course.objects.all()  # or any filter you need
    return render(request, 'pages/course-detail-two.html', {'courses': courses})

def course_detail_two(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request,'pages/course-detail-two.html', {'course': course})

def aboutus(request):
    return render(request,'pages/aboutus.html')

def features(request):
    return render(request,'pages/features.html')

def pricing(request):
    return render(request,'pages/pricing.html')

def instructors(request):
    return render(request,'pages/instructors.html')

def faqs(request):
    return render(request,'pages/faqs.html')

def terms(request):
    return render(request,'pages/terms.html')

def privacy(request):
    return render(request,'pages/privacy.html')

def login(request):
    return render(request,'pages/login.html')

def signup(request):
    return render(request,'pages/signup.html')

def forgot_password(request):
    return render(request,'pages/forgot-password.html')

def blogs(request):
    return render(request,'pages/blogs.html')

def blog_sidebar(request):
    return render(request,'pages/blog-sidebar.html')

def blog_list_or_default(request):
    # Get blogs from the database
    blogs = Blog.objects.all()  # or any filter you need
    return render(request, 'pages/blog-detail.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request,'pages/blog-detail.html', {'blog': blog})

def comingsoon(request):
    return render(request,'pages/comingsoon.html')

def maintenance(request):
    return render(request,'pages/maintenance.html')

def notFound(request):
    return render(request,'pages/404.html')

def contactus(request):
    return render(request,'pages/contactus.html')