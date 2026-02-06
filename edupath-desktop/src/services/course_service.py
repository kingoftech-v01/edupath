"""
Course Service.

Handles course-related operations with caching support.
"""

from typing import List, Optional
from dataclasses import dataclass

from api.client import APIClient
from config import Endpoints
from models.course import Course, Category, Instructor, Review
from .cache_service import CacheService


@dataclass
class CoursesResult:
    """
    Courses fetch result.

    Contains success status, course list, and cache indicator.
    """

    success: bool
    courses: List[Course] = None
    error: Optional[str] = None
    from_cache: bool = False

    def __post_init__(self):
        if self.courses is None:
            self.courses = []


class CourseService:
    """
    Course service with caching.

    Provides methods for fetching courses, categories, and reviews.
    Implements local caching to reduce API calls.
    """

    def __init__(self, api_client: APIClient, cache_service: CacheService):
        """
        Initialize the course service.

        Args:
            api_client: The API client for making requests.
            cache_service: The cache service for local storage.
        """
        self.api_client = api_client
        self.cache = cache_service

    async def get_courses(
        self,
        category: Optional[str] = None,
        search: Optional[str] = None,
        is_free: Optional[bool] = None,
        use_cache: bool = True,
    ) -> CoursesResult:
        """
        Get courses with optional filters.

        Args:
            category: Filter by category slug.
            search: Search term for title/description.
            is_free: Filter by free courses only.
            use_cache: Whether to use cached results.

        Returns:
            CoursesResult: Result with courses list.
        """
        # Build cache key
        cache_key = f"courses:{category}:{search}:{is_free}"

        # Try cache first
        if use_cache:
            cached = self.cache.get_courses(cache_key)
            if cached:
                return CoursesResult(success=True, courses=cached, from_cache=True)

        # Fetch from API
        params = {}
        if category:
            params["category__slug"] = category
        if search:
            params["search"] = search
        if is_free is not None:
            params["is_free"] = str(is_free).lower()

        response = await self.api_client.get(Endpoints.COURSES, params=params)

        if response.success:
            results = response.data.get("results", []) if isinstance(response.data, dict) else response.data
            courses = [Course(**c) for c in results]

            # Cache results
            self.cache.cache_courses(cache_key, courses)

            return CoursesResult(success=True, courses=courses)

        return CoursesResult(success=False, error=response.error)

    async def get_course(self, slug: str) -> Optional[Course]:
        """
        Get single course by slug.

        Args:
            slug: The course's URL slug.

        Returns:
            Optional[Course]: Course object or None.
        """
        # Try cache first
        cached = self.cache.get_course(slug)
        if cached:
            return cached

        response = await self.api_client.get(f"{Endpoints.COURSES}{slug}/")
        if response.success and response.data:
            course = Course(**response.data)
            self.cache.cache_course(course)
            return course

        return None

    async def get_featured_courses(self) -> List[Course]:
        """
        Get featured courses.

        Returns:
            List[Course]: List of featured courses.
        """
        response = await self.api_client.get(Endpoints.COURSES_FEATURED)
        if response.success:
            return [Course(**c) for c in response.data]
        return []

    async def get_free_courses(self) -> List[Course]:
        """
        Get free courses.

        Returns:
            List[Course]: List of free courses.
        """
        response = await self.api_client.get(Endpoints.COURSES_FREE)
        if response.success:
            return [Course(**c) for c in response.data]
        return []

    async def get_categories(self) -> List[Category]:
        """
        Get all categories.

        Returns cached categories or fetches from API.

        Returns:
            List[Category]: List of course categories.
        """
        # Try cache
        cached = self.cache.get_categories()
        if cached:
            return cached

        response = await self.api_client.get(Endpoints.CATEGORIES)
        if response.success:
            results = response.data.get("results", []) if isinstance(response.data, dict) else response.data
            categories = [Category(**c) for c in results]
            self.cache.cache_categories(categories)
            return categories

        return []

    async def get_instructors(self) -> List[Instructor]:
        """
        Get all instructors.

        Returns:
            List[Instructor]: List of course instructors.
        """
        response = await self.api_client.get(Endpoints.INSTRUCTORS)
        if response.success:
            results = response.data.get("results", []) if isinstance(response.data, dict) else response.data
            return [Instructor(**i) for i in results]
        return []

    async def get_course_reviews(self, course_id: int) -> List[Review]:
        """
        Get reviews for a course.

        Args:
            course_id: The course ID to get reviews for.

        Returns:
            List[Review]: List of course reviews.
        """
        response = await self.api_client.get(
            Endpoints.REVIEWS,
            params={"course": course_id},
        )
        if response.success:
            results = response.data.get("results", []) if isinstance(response.data, dict) else response.data
            return [Review(**r) for r in results]
        return []

    async def submit_review(
        self, course_id: int, rating: int, description: str
    ) -> tuple[bool, Optional[str]]:
        """
        Submit a course review.

        Args:
            course_id: The course ID to review.
            rating: Rating from 1-5.
            description: Review text.

        Returns:
            tuple[bool, Optional[str]]: Success status and error message.
        """
        response = await self.api_client.post(
            Endpoints.REVIEWS,
            data={
                "course": course_id,
                "rating": rating,
                "desc": description,
            },
        )
        if response.success:
            return True, None
        return False, response.error
