"""
Cache Service.

Handles local caching using SQLite for offline support.
"""

import json
from typing import List, Optional
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from models.course import Course, Category

Base = declarative_base()


class CacheEntry(Base):
    """
    Cache entry model.

    SQLAlchemy model for storing cached data with expiration.
    """

    __tablename__ = "cache"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, index=True)
    value = Column(Text)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


class CacheService:
    """
    Local cache service using SQLite.

    Provides key-value caching with automatic expiration.
    Includes specialized methods for courses and categories.
    """

    def __init__(self, cache_dir: Path, db_path: Path, expiry_hours: int = 24):
        """
        Initialize the cache service.

        Args:
            cache_dir: Directory for cache files.
            db_path: Path to SQLite database file.
            expiry_hours: Cache entry lifetime in hours.
        """
        self.cache_dir = cache_dir
        self.db_path = db_path
        self.expiry_hours = expiry_hours

        # Initialize database
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def _get_session(self):
        """
        Get database session.

        Returns:
            Session: SQLAlchemy session instance.
        """
        return self.Session()

    def _get_expiry(self) -> datetime:
        """
        Get expiry datetime.

        Returns:
            datetime: Expiration time based on expiry_hours.
        """
        return datetime.now() + timedelta(hours=self.expiry_hours)

    def set(self, key: str, value: any) -> None:
        """
        Set cache value.

        Args:
            key: Cache key.
            value: Value to cache (will be JSON serialized).
        """
        session = self._get_session()
        try:
            entry = session.query(CacheEntry).filter_by(key=key).first()
            if entry:
                entry.value = json.dumps(value, default=str)
                entry.expires_at = self._get_expiry()
            else:
                entry = CacheEntry(
                    key=key,
                    value=json.dumps(value, default=str),
                    expires_at=self._get_expiry(),
                )
                session.add(entry)
            session.commit()
        finally:
            session.close()

    def get(self, key: str) -> Optional[any]:
        """
        Get cache value if not expired.

        Args:
            key: Cache key to retrieve.

        Returns:
            Optional[any]: Cached value or None if expired/missing.
        """
        session = self._get_session()
        try:
            entry = session.query(CacheEntry).filter_by(key=key).first()
            if entry and entry.expires_at > datetime.now():
                return json.loads(entry.value)
            return None
        finally:
            session.close()

    def delete(self, key: str) -> None:
        """
        Delete cache entry.

        Args:
            key: Cache key to delete.
        """
        session = self._get_session()
        try:
            session.query(CacheEntry).filter_by(key=key).delete()
            session.commit()
        finally:
            session.close()

    def clear(self) -> None:
        """
        Clear all cache.

        Removes all entries from the cache database.
        """
        session = self._get_session()
        try:
            session.query(CacheEntry).delete()
            session.commit()
        finally:
            session.close()

    def clear_expired(self) -> None:
        """
        Clear expired cache entries.

        Removes entries where expires_at is in the past.
        """
        session = self._get_session()
        try:
            session.query(CacheEntry).filter(
                CacheEntry.expires_at < datetime.now()
            ).delete()
            session.commit()
        finally:
            session.close()

    # Course-specific cache methods

    def cache_courses(self, key: str, courses: List[Course]) -> None:
        """
        Cache courses list.

        Args:
            key: Cache key for the course list.
            courses: List of Course objects to cache.
        """
        self.set(key, [c.model_dump() for c in courses])

    def get_courses(self, key: str) -> Optional[List[Course]]:
        """
        Get cached courses.

        Args:
            key: Cache key to retrieve.

        Returns:
            Optional[List[Course]]: List of courses or None.
        """
        data = self.get(key)
        if data:
            return [Course(**c) for c in data]
        return None

    def cache_course(self, course: Course) -> None:
        """
        Cache single course.

        Args:
            course: Course object to cache.
        """
        self.set(f"course:{course.slug}", course.model_dump())

    def get_course(self, slug: str) -> Optional[Course]:
        """
        Get cached course.

        Args:
            slug: Course slug to retrieve.

        Returns:
            Optional[Course]: Course object or None.
        """
        data = self.get(f"course:{slug}")
        if data:
            return Course(**data)
        return None

    def cache_categories(self, categories: List[Category]) -> None:
        """
        Cache categories list.

        Args:
            categories: List of Category objects to cache.
        """
        self.set("categories", [c.model_dump() for c in categories])

    def get_categories(self) -> Optional[List[Category]]:
        """
        Get cached categories.

        Returns:
            Optional[List[Category]]: List of categories or None.
        """
        data = self.get("categories")
        if data:
            return [Category(**c) for c in data]
        return None
