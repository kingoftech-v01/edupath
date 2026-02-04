"""
Login View.

User authentication interface.
"""

import asyncio

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal

from services.auth_service import AuthService


class LoginView(QWidget):
    """Login view for user authentication."""

    login_successful = pyqtSignal()

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login card
        card = QFrame()
        card.setObjectName("login_card")
        card.setFixedSize(400, 350)
        card_layout = QVBoxLayout(card)

        # Title
        title = QLabel("Welcome to EduPath")
        title.setObjectName("login_title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Sign in to continue learning")
        subtitle.setObjectName("login_subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(20)

        # Username field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("login_input")
        card_layout.addWidget(self.username_input)

        # Password field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setObjectName("login_input")
        card_layout.addWidget(self.password_input)

        card_layout.addSpacing(20)

        # Login button
        self.login_btn = QPushButton("Sign In")
        self.login_btn.setObjectName("login_button")
        self.login_btn.clicked.connect(self._on_login_clicked)
        card_layout.addWidget(self.login_btn)

        # Error label
        self.error_label = QLabel()
        self.error_label.setObjectName("error_label")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)

        layout.addWidget(card)

        # Enter key triggers login
        self.password_input.returnPressed.connect(self._on_login_clicked)

    def _on_login_clicked(self):
        """Handle login button click."""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self._show_error("Please enter username and password")
            return

        self.login_btn.setEnabled(False)
        self.login_btn.setText("Signing in...")

        # Run async login
        asyncio.create_task(self._do_login(username, password))

    async def _do_login(self, username: str, password: str):
        """Perform login."""
        try:
            result = await self.auth_service.login(username, password)

            if result.success:
                self.error_label.hide()
                self.login_successful.emit()
            else:
                self._show_error(result.error or "Login failed")

        except Exception as e:
            self._show_error(str(e))

        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Sign In")

    def _show_error(self, message: str):
        """Show error message."""
        self.error_label.setText(message)
        self.error_label.show()
