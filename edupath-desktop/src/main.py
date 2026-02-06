"""EduPath desktop client (PyQt6)."""

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
    """Main application: initializes services and runs event loop."""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName(config.APP_NAME)
        self.app.setApplicationVersion(config.APP_VERSION)

        # PassThrough avoids blurry UI on high-DPI displays
        self.app.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        self.api_client = APIClient(config.API_BASE_URL)
        self.cache_service = CacheService(config.CACHE_DIR, config.DB_PATH)
        self.auth_service = AuthService(self.api_client)
        self.course_service = CourseService(self.api_client, self.cache_service)

        self.main_window = MainWindow(
            auth_service=self.auth_service,
            course_service=self.course_service,
            cache_service=self.cache_service,
        )

        self._load_styles()

    def _load_styles(self):
        """Load QSS theme. Falls back to Qt defaults if missing."""
        try:
            style_path = config.APP_DIR.parent / "resources" / "styles" / "theme.qss"
            if style_path.exists():
                with open(style_path, "r") as f:
                    self.app.setStyleSheet(f.read())
        except Exception:
            pass

    def run(self) -> int:
        self.main_window.show()
        return self.app.exec()


def main():
    app = EduPathApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
