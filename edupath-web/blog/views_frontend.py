"""
Blog Frontend Views - Blog listing and detail views.
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Blog


def blog_list(request):
    """
    Blog listing page.

    Shows all active blog posts in a grid layout.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered blog listing template.
    """
    return render(request, 'pages/blogs.html')


def blog_sidebar(request):
    """
    Blog listing with sidebar layout.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered blog-sidebar template.
    """
    return render(request, 'pages/blog-sidebar.html')


def blog_detail(request, slug):
    """
    Blog detail page by slug.

    Shows full blog content with recent posts sidebar.

    Args:
        request: The HTTP request object.
        slug: Blog post URL slug.

    Returns:
        HttpResponse: Rendered blog detail template.
    """
    blog = get_object_or_404(Blog, slug=slug, is_active=True)
    # Show recent posts in sidebar, excluding current to avoid redundancy.
    recent_blogs = Blog.objects.filter(is_active=True).exclude(pk=blog.pk)[:5]

    context = {
        'blog': blog,
        # selected_blog used by context processor to highlight current in nav.
        'selected_blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'pages/blog-detail.html', context)


def blog_detail_by_id(request, blog_id):
    """
    Blog detail page by ID.

    Maintains backward compatibility with old numeric ID URLs.

    Args:
        request: The HTTP request object.
        blog_id: Numeric blog post ID.

    Returns:
        HttpResponse: Rendered blog detail template.
    """
    blog = get_object_or_404(Blog, id=blog_id, is_active=True)
    recent_blogs = Blog.objects.filter(is_active=True).exclude(pk=blog.pk)[:5]

    context = {
        'blog': blog,
        'selected_blog': blog,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'pages/blog-detail.html', context)
