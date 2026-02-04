"""
Courses View.

Course listing with search and filtering.
"""

import asyncio

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QComboBox, QPushButton, QScrollArea,
    QGridLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal

from services.course_service import CourseService
from ui.widgets.course_card import CourseCard


class CoursesView(QWidget):
    """Courses listing view with filters."""

    course_selected = pyqtSignal(str)  # Emits course slug

    def __init__(self, course_service: CourseService):
        super().__init__()
        self.course_service = course_service
        self._categories = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header = QLabel("All Courses")
        header.setObjectName("page_title")
        layout.addWidget(header)

        # Filters row
        filters_layout = QHBoxLayout()

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.setObjectName("search_input")
        self.search_input.returnPressed.connect(self._on_search)
        filters_layout.addWidget(self.search_input)

        # Category filter
        self.category_combo = QComboBox()
        self.category_combo.setObjectName("filter_combo")
        self.category_combo.addItem("All Categories", "")
        self.category_combo.currentIndexChanged.connect(self._on_filter_changed)
        filters_layout.addWidget(self.category_combo)

        # Price filter
        self.price_combo = QComboBox()
        self.price_combo.setObjectName("filter_combo")
        self.price_combo.addItem("All Prices", "")
        self.price_combo.addItem("Free", "free")
        self.price_combo.addItem("Paid", "paid")
        self.price_combo.currentIndexChanged.connect(self._on_filter_changed)
        filters_layout.addWidget(self.price_combo)

        # Search button
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._on_search)
        filters_layout.addWidget(search_btn)

        layout.addLayout(filters_layout)
        layout.addSpacing(20)

        # Courses scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        self.courses_grid = QGridLayout(scroll_content)
        self.courses_grid.setSpacing(20)
        scroll.setWidget(scroll_content)

        layout.addWidget(scroll)

        # Loading/empty state label
        self.status_label = QLabel("Loading courses...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.hide()
        layout.addWidget(self.status_label)

    def load_courses(self):
        """Load courses list."""
        asyncio.create_task(self._load_courses())

    async def _load_courses(self):
        """Load courses asynchronously."""
        self.status_label.setText("Loading courses...")
        self.status_label.show()

        # Load categories for filter
        if not self._categories:
            self._categories = await self.course_service.get_categories()
            for cat in self._categories:
                self.category_combo.addItem(cat.name, cat.slug)

        # Get filter values
        search = self.search_input.text().strip() or None
        category = self.category_combo.currentData() or None
        price_filter = self.price_combo.currentData()
        is_free = None
        if price_filter == "free":
            is_free = True
        elif price_filter == "paid":
            is_free = False

        # Load courses
        result = await self.course_service.get_courses(
            category=category,
            search=search,
            is_free=is_free,
        )

        if result.success:
            self._display_courses(result.courses)
            if not result.courses:
                self.status_label.setText("No courses found")
                self.status_label.show()
            else:
                self.status_label.hide()
        else:
            self.status_label.setText(f"Error: {result.error}")
            self.status_label.show()

    def _display_courses(self, courses):
        """Display courses in grid."""
        # Clear existing
        while self.courses_grid.count():
            item = self.courses_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add course cards
        row, col = 0, 0
        for course in courses:
            card = CourseCard(course)
            card.clicked.connect(lambda slug=course.slug: self.course_selected.emit(slug))
            self.courses_grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def _on_search(self):
        """Handle search."""
        self.load_courses()

    def _on_filter_changed(self):
        """Handle filter change."""
        self.load_courses()
