"""
Course Detail View.

Detailed course information with video player.
"""

import asyncio

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal

from models.course import Course
from services.course_service import CourseService
from services.auth_service import AuthService
from ui.widgets.video_player import VideoPlayer


class CourseDetailView(QWidget):
    """Course detail view with video player."""

    back_requested = pyqtSignal()

    def __init__(self, course_service: CourseService, auth_service: AuthService):
        super().__init__()
        self.course_service = course_service
        self.auth_service = auth_service
        self._current_course = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Back button
        back_btn = QPushButton("← Back to Courses")
        back_btn.setObjectName("back_button")
        back_btn.clicked.connect(self.back_requested.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # Content scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Video player
        self.video_player = VideoPlayer()
        content_layout.addWidget(self.video_player)

        content_layout.addSpacing(20)

        # Course info
        info_layout = QHBoxLayout()

        # Left side - details
        details_frame = QFrame()
        details_layout = QVBoxLayout(details_frame)

        self.title_label = QLabel()
        self.title_label.setObjectName("course_title")
        self.title_label.setWordWrap(True)
        details_layout.addWidget(self.title_label)

        self.instructor_label = QLabel()
        self.instructor_label.setObjectName("course_instructor")
        details_layout.addWidget(self.instructor_label)

        self.category_label = QLabel()
        self.category_label.setObjectName("course_category")
        details_layout.addWidget(self.category_label)

        # Stats row
        stats_layout = QHBoxLayout()
        self.students_label = QLabel()
        self.lessons_label = QLabel()
        self.duration_label = QLabel()
        stats_layout.addWidget(self.students_label)
        stats_layout.addWidget(self.lessons_label)
        stats_layout.addWidget(self.duration_label)
        stats_layout.addStretch()
        details_layout.addLayout(stats_layout)

        info_layout.addWidget(details_frame, 2)

        # Right side - price and actions
        actions_frame = QFrame()
        actions_frame.setObjectName("price_card")
        actions_layout = QVBoxLayout(actions_frame)

        self.price_label = QLabel()
        self.price_label.setObjectName("course_price")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_layout.addWidget(self.price_label)

        enroll_btn = QPushButton("Enroll Now")
        enroll_btn.setObjectName("enroll_button")
        actions_layout.addWidget(enroll_btn)

        info_layout.addWidget(actions_frame, 1)

        content_layout.addLayout(info_layout)

        content_layout.addSpacing(20)

        # Description
        desc_label = QLabel("Description")
        desc_label.setObjectName("section_title")
        content_layout.addWidget(desc_label)

        self.description_text = QLabel()
        self.description_text.setWordWrap(True)
        self.description_text.setObjectName("course_description")
        content_layout.addWidget(self.description_text)

        content_layout.addStretch()

        scroll.setWidget(content)
        layout.addWidget(scroll)

    def load_course(self, slug: str):
        """Load course by slug."""
        asyncio.create_task(self._load_course(slug))

    async def _load_course(self, slug: str):
        """Load course asynchronously."""
        course = await self.course_service.get_course(slug)
        if course:
            self._current_course = course
            self._display_course(course)

    def _display_course(self, course: Course):
        """Display course information."""
        self.title_label.setText(course.title)

        if course.instructor:
            self.instructor_label.setText(f"By {course.instructor.name}")
        else:
            self.instructor_label.setText(f"By {course.name}")

        if course.category:
            self.category_label.setText(course.category.name)

        self.students_label.setText(f"👥 {course.students} students")
        self.lessons_label.setText(f"📚 {course.lessons} lessons")
        self.duration_label.setText(f"⏱️ {course.duration_hours}h")

        self.price_label.setText(course.formatted_price)
        self.description_text.setText(course.desc)

        # Load video if available
        if course.video_url:
            self.video_player.set_source(course.video_url)
