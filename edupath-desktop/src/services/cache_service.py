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
    """Cache entry model."""

    __tablename__ = "cache"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), unique=True, index=True)
    value = Column(Text)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


class CacheService:
    """Local cache service using SQLite."""

    def __init__(self, cache_dir: Path, db_path: Path, expiry_hours: int = 24):
        self.cache_dir = cache_dir
        self.db_path = db_path
        self.expiry_hours = expiry_hours

        # Initialize database
        # Note: SQLite file is not encrypted. Restrict file permissions to owner-only.
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

        # Restrict database file permissions (owner read/write only)
        import os
        import stat
        try:
            os.chmod(db_path, stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # Best effort — may fail on some platforms

    def _get_session(self):
        """Get database session."""
        return self.Session()

    def _get_expiry(self) -> datetime:
        """Get expiry datetime."""
        return datetime.now() + timedelta(hours=self.expiry_hours)

    def set(self, key: str, value: any) -> None:
        """Set cache value."""
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
        """Get cache value if not expired."""
        session = self._get_session()
        try:
            entry = session.query(CacheEntry).filter_by(key=key).first()
            if entry and entry.expires_at > datetime.now():
                return json.loads(entry.value)
            return None
        finally:
            session.close()

    def delete(self, key: str) -> None:
        """Delete cache entry."""
        session = self._get_session()
        try:
            session.query(CacheEntry).filter_by(key=key).delete()
            session.commit()
        finally:
            session.close()

    def clear(self) -> None:
        """Clear all cache."""
        session = self._get_session()
        try:
            session.query(CacheEntry).delete()
            session.commit()
        finally:
            session.close()

    def clear_expired(self) -> None:
        """Clear expired cache entries."""
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
        """Cache courses list."""
        self.set(key, [c.model_dump() for c in courses])

    def get_courses(self, key: str) -> Optional[List[Course]]:
        """Get cached courses."""
        data = self.get(key)
        if data:
            return [Course(**c) for c in data]
        return None

    def cache_course(self, course: Course) -> None:
        """Cache single course."""
        self.set(f"course:{course.slug}", course.model_dump())

    def get_course(self, slug: str) -> Optional[Course]:
        """Get cached course."""
        data = self.get(f"course:{slug}")
        if data:
            return Course(**data)
        return None

    def cache_categories(self, categories: List[Category]) -> None:
        """Cache categories list."""
        self.set("categories", [c.model_dump() for c in categories])

    def get_categories(self) -> Optional[List[Category]]:
        """Get cached categories."""
        data = self.get("categories")
        if data:
            return [Category(**c) for c in data]
        return None
