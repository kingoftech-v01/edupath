"""
Dashboard View.

Main dashboard showing featured courses and statistics.
"""

import asyncio

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QScrollArea, QFrame, QGridLayout
)
from PyQt6.QtCore import Qt

from services.course_service import CourseService
from ui.widgets.course_card import CourseCard


class StatCard(QFrame):
    """Statistics card widget."""

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent)
        self.setObjectName("stat_card")
        self._setup_ui(title, value)

    def _setup_ui(self, title: str, value: str):
        layout = QVBoxLayout(self)

        value_label = QLabel(value)
        value_label.setObjectName("stat_value")
        layout.addWidget(value_label)

        title_label = QLabel(title)
        title_label.setObjectName("stat_title")
        layout.addWidget(title_label)


class DashboardView(QWidget):
    """Dashboard view showing overview and featured courses."""

    def __init__(self, course_service: CourseService):
        super().__init__()
        self.course_service = course_service
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Welcome header
        welcome_label = QLabel("Welcome back!")
        welcome_label.setObjectName("dashboard_title")
        layout.addWidget(welcome_label)

        subtitle = QLabel("Continue your learning journey")
        subtitle.setObjectName("dashboard_subtitle")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Stats row
        stats_layout = QHBoxLayout()
        self.courses_stat = StatCard("Total Courses", "0")
        self.categories_stat = StatCard("Categories", "0")
        self.featured_stat = StatCard("Featured", "0")
        stats_layout.addWidget(self.courses_stat)
        stats_layout.addWidget(self.categories_stat)
        stats_layout.addWidget(self.featured_stat)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        layout.addSpacing(20)

        # Featured courses section
        featured_header = QLabel("Featured Courses")
        featured_header.setObjectName("section_title")
        layout.addWidget(featured_header)

        # Scroll area for courses
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.courses_grid = QGridLayout(scroll_content)
        self.courses_grid.setSpacing(20)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)

    def load_data(self):
        """Load dashboard data."""
        asyncio.create_task(self._load_data())

    async def _load_data(self):
        """Load data asynchronously."""
        # Load categories count
        categories = await self.course_service.get_categories()
        self.categories_stat.findChild(QLabel, "stat_value").setText(str(len(categories)))

        # Load featured courses
        featured = await self.course_service.get_featured_courses()
        self.featured_stat.findChild(QLabel, "stat_value").setText(str(len(featured)))

        # Load all courses count
        result = await self.course_service.get_courses()
        if result.success:
            self.courses_stat.findChild(QLabel, "stat_value").setText(str(len(result.courses)))

        # Display featured courses
        self._display_courses(featured)

    def _display_courses(self, courses):
        """Display courses in grid."""
        # Clear existing
        while self.courses_grid.count():
            item = self.courses_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add course cards
        row, col = 0, 0
        for course in courses[:6]:  # Show max 6 featured
            card = CourseCard(course)
            self.courses_grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1
