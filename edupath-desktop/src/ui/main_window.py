"""
Main Window.

The main application window with navigation and view management.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon

from config import config
from services.auth_service import AuthService
from services.course_service import CourseService
from services.cache_service import CacheService


class Sidebar(QFrame):
    """Navigation sidebar."""

    navigation_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(250)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Logo
        logo_label = QLabel("EduPath")
        logo_label.setObjectName("logo")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Navigation buttons
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Courses", "courses"),
            ("Categories", "categories"),
            ("Instructors", "instructors"),
            ("My Learning", "learning"),
            ("Profile", "profile"),
        ]

        for label, view_name in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("nav_button")
            btn.clicked.connect(lambda checked, v=view_name: self.navigation_requested.emit(v))
            layout.addWidget(btn)

        layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logout_button")
        logout_btn.clicked.connect(lambda: self.navigation_requested.emit("logout"))
        layout.addWidget(logout_btn)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        auth_service: AuthService,
        course_service: CourseService,
        cache_service: CacheService,
    ):
        super().__init__()
        self.auth_service = auth_service
        self.course_service = course_service
        self.cache_service = cache_service

        self._setup_window()
        self._setup_ui()
        self._connect_signals()

        # Show login or dashboard based on auth state
        if self.auth_service.is_authenticated():
            self._show_main_view()
        else:
            self._show_login_view()

    def _setup_window(self):
        """Configure window properties."""
        self.setWindowTitle(config.APP_NAME)
        self.setMinimumSize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)

    def _setup_ui(self):
        """Setup UI components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.hide()
        main_layout.addWidget(self.sidebar)

        # Content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)

        # Add views to stack
        self._setup_views()

    def _setup_views(self):
        """Setup all views."""
        from ui.views.login_view import LoginView
        from ui.views.dashboard_view import DashboardView
        from ui.views.courses_view import CoursesView
        from ui.views.course_detail_view import CourseDetailView

        # Login view
        self.login_view = LoginView(self.auth_service)
        self.login_view.login_successful.connect(self._on_login_success)
        self.content_stack.addWidget(self.login_view)

        # Dashboard view
        self.dashboard_view = DashboardView(self.course_service)
        self.content_stack.addWidget(self.dashboard_view)

        # Courses view
        self.courses_view = CoursesView(self.course_service)
        self.courses_view.course_selected.connect(self._on_course_selected)
        self.content_stack.addWidget(self.courses_view)

        # Course detail view
        self.course_detail_view = CourseDetailView(self.course_service, self.auth_service)
        self.content_stack.addWidget(self.course_detail_view)

    def _connect_signals(self):
        """Connect signals to slots."""
        self.sidebar.navigation_requested.connect(self._on_navigation)

    def _show_login_view(self):
        """Show login view."""
        self.sidebar.hide()
        self.content_stack.setCurrentWidget(self.login_view)

    def _show_main_view(self):
        """Show main view with sidebar."""
        self.sidebar.show()
        self.content_stack.setCurrentWidget(self.dashboard_view)
        self.dashboard_view.load_data()

    def _on_login_success(self):
        """Handle successful login."""
        self._show_main_view()

    def _on_navigation(self, view_name: str):
        """Handle navigation requests."""
        if view_name == "logout":
            import asyncio
            asyncio.create_task(self._logout())
        elif view_name == "dashboard":
            self.content_stack.setCurrentWidget(self.dashboard_view)
            self.dashboard_view.load_data()
        elif view_name == "courses":
            self.content_stack.setCurrentWidget(self.courses_view)
            self.courses_view.load_courses()
        elif view_name == "profile":
            pass  # TODO: Implement profile view

    def _on_course_selected(self, slug: str):
        """Handle course selection."""
        self.course_detail_view.load_course(slug)
        self.content_stack.setCurrentWidget(self.course_detail_view)

    async def _logout(self):
        """Logout and show login view."""
        await self.auth_service.logout()
        self._show_login_view()
