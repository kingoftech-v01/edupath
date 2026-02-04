"""
Blog Frontend Views - Blog listing and detail views.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Blog


def blog_list(request):
    """Blog listing page."""
    return render(request, 'pages/blogs.html')


def blog_sidebar(request):
    """Blog listing with sidebar."""
    return render(request, 'pages/blog-sidebar.html')


def blog_detail(request, slug):
    """Blog detail page by slug."""
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).exclude(pk=blog.pk)[:5]

    context = {
        'blog': blog,
        'selected_blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'pages/blog-detail.html', context)


def blog_detail_by_id(request, blog_id):
    """Blog detail page by ID (for legacy URLs)."""
    blog = get_object_or_404(Blog, id=blog_id, is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).exclude(pk=blog.pk)[:5]

    context = {
        'blog': blog,
        'selected_blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'pages/blog-detail.html', context)
