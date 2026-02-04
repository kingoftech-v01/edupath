"""
Course Card Widget.

A card component displaying course information.
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap

from models.course import Course


class CourseCard(QFrame):
    """Course card widget displaying course preview."""

    clicked = pyqtSignal()

    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.course = course
        self.setObjectName("course_card")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        self.setFixedSize(280, 320)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Image placeholder
        image_frame = QFrame()
        image_frame.setObjectName("course_image")
        image_frame.setFixedHeight(160)
        layout.addWidget(image_frame)

        # Content
        content = QFrame()
        content.setObjectName("course_content")
        content_layout = QVBoxLayout(content)

        # Category badge
        if self.course.category:
            category_label = QLabel(self.course.category.name)
            category_label.setObjectName("course_category_badge")
            content_layout.addWidget(category_label)

        # Title
        title = QLabel(self.course.title)
        title.setObjectName("course_card_title")
        title.setWordWrap(True)
        title.setMaximumHeight(50)
        content_layout.addWidget(title)

        # Instructor
        instructor_name = self.course.instructor.name if self.course.instructor else self.course.name
        instructor = QLabel(f"By {instructor_name}")
        instructor.setObjectName("course_card_instructor")
        content_layout.addWidget(instructor)

        content_layout.addStretch()

        # Footer with stats
        footer = QHBoxLayout()

        # Students
        students = QLabel(f"👥 {self.course.students}")
        students.setObjectName("course_stat")
        footer.addWidget(students)

        # Lessons
        lessons = QLabel(f"📚 {self.course.lessons}")
        lessons.setObjectName("course_stat")
        footer.addWidget(lessons)

        footer.addStretch()

        # Price
        price = QLabel(self.course.formatted_price)
        price.setObjectName("course_price_badge")
        footer.addWidget(price)

        content_layout.addLayout(footer)
        layout.addWidget(content)

    def mousePressEvent(self, event):
        """Handle mouse press."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
