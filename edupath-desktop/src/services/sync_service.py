"""
Sync Service.

Handles offline synchronization between local cache and remote API.
"""

import asyncio
from typing import List, Callable, Optional
from dataclasses import dataclass
from datetime import datetime

from .cache_service import CacheService
from .course_service import CourseService


@dataclass
class SyncStatus:
    """
    Sync status information.

    Tracks synchronization state and progress.
    """

    is_syncing: bool = False
    last_sync: Optional[datetime] = None
    error: Optional[str] = None
    items_synced: int = 0


class SyncService:
    """
    Handles offline data synchronization.

    Syncs data between local cache and remote API.
    Provides callbacks for UI status updates.
    """

    def __init__(self, course_service: CourseService, cache_service: CacheService):
        """
        Initialize the sync service.

        Args:
            course_service: Service for fetching course data.
            cache_service: Service for local caching.
        """
        self.course_service = course_service
        self.cache_service = cache_service
        self.status = SyncStatus()
        self._callbacks: List[Callable[[SyncStatus], None]] = []

    def add_callback(self, callback: Callable[[SyncStatus], None]):
        """
        Add sync status callback.

        Args:
            callback: Function to call on status changes.
        """
        self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[SyncStatus], None]):
        """
        Remove sync status callback.

        Args:
            callback: Function to remove from callbacks.
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def _notify_callbacks(self):
        """
        Notify all callbacks of status change.

        Called after any sync status update.
        """
        for callback in self._callbacks:
            callback(self.status)

    async def sync_all(self) -> bool:
        """
        Sync all data from remote.

        Downloads categories, featured courses, and all courses.

        Returns:
            bool: True if sync completed successfully.
        """
        if self.status.is_syncing:
            return False

        self.status.is_syncing = True
        self.status.error = None
        self.status.items_synced = 0
        self._notify_callbacks()

        try:
            # Sync categories
            categories = await self.course_service.get_categories()
            if categories:
                self.cache_service.cache_categories(categories)
                self.status.items_synced += len(categories)

            # Sync featured courses
            featured = await self.course_service.get_featured_courses()
            self.cache_service.cache_courses("featured", featured)
            self.status.items_synced += len(featured)

            # Sync all courses (paginated)
            result = await self.course_service.get_courses(use_cache=False)
            if result.success:
                self.cache_service.cache_courses("all_courses", result.courses)
                self.status.items_synced += len(result.courses)

            self.status.last_sync = datetime.now()
            return True

        except Exception as e:
            self.status.error = str(e)
            return False

        finally:
            self.status.is_syncing = False
            self._notify_callbacks()

    async def sync_course(self, slug: str) -> bool:
        """
        Sync a specific course.

        Args:
            slug: Course slug to sync.

        Returns:
            bool: True if sync succeeded.
        """
        try:
            course = await self.course_service.get_course(slug)
            if course:
                self.cache_service.cache_course(course)
                return True
            return False
        except Exception:
            return False

    def clear_cache(self):
        """
        Clear all cached data.

        Removes local cache and resets sync status.
        """
        self.cache_service.clear()
        self.status.last_sync = None
        self._notify_callbacks()

    def is_offline_ready(self) -> bool:
        """
        Check if enough data is cached for offline use.

        Returns:
            bool: True if categories and courses are cached.
        """
        categories = self.cache_service.get_categories()
        courses = self.cache_service.get_courses("all_courses")
        return bool(categories and courses)
