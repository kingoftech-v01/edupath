"""
EduPath Desktop Application - Main Entry Point.

A PyQt6-based desktop client for the EduPath learning platform.
"""

import sys
import asyncio
from typing import Optional

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon

from config import config
from api.client import APIClient
from services.auth_service import AuthService
from services.cache_service import CacheService
from services.course_service import CourseService
from ui.main_window import MainWindow


class EduPathApp:
    """
    Main application class.

    Initializes PyQt6 application, services, and main window.
    Manages application lifecycle and resource cleanup.
    """

    def __init__(self):
        """
        Initialize the application.

        Sets up PyQt6 application, creates service instances,
        and initializes the main window.
        """
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(config.APP_NAME)
        self.app.setApplicationVersion(config.APP_VERSION)

        # Apply high DPI settings
        self.app.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        # Initialize services
        self.api_client = APIClient(config.API_BASE_URL)
        self.cache_service = CacheService(config.CACHE_DIR, config.DB_PATH)
        self.auth_service = AuthService(self.api_client)
        self.course_service = CourseService(self.api_client, self.cache_service)

        # Initialize main window
        self.main_window = MainWindow(
            auth_service=self.auth_service,
            course_service=self.course_service,
            cache_service=self.cache_service,
        )

        # Load styles
        self._load_styles()

    def _load_styles(self):
        """
        Load QSS stylesheet from resources.

        Applies custom Qt styling from theme.qss file.
        Fails silently if stylesheet not found.
        """
        try:
            style_path = config.APP_DIR.parent / "resources" / "styles" / "theme.qss"
            if style_path.exists():
                with open(style_path, "r") as f:
                    self.app.setStyleSheet(f.read())
        except Exception:
            pass  # Use default styles

    def run(self) -> int:
        """
        Run the application event loop.

        Shows main window and starts Qt event processing.

        Returns:
            int: Application exit code.
        """
        self.main_window.show()
        return self.app.exec()


def main():
    """
    Application entry point.

    Creates EduPathApp instance and runs the event loop.
    Exits with the application's return code.
    """
    app = EduPathApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
