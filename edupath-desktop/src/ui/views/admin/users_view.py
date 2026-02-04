"""
Users Admin View.

Admin interface for managing users.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QHeaderView
)
from PyQt6.QtCore import Qt


class UsersAdminView(QWidget):
    """Admin view for user management."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("User Management")
        title.setObjectName("admin_title")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Search
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search users...")
        self.search_input.setMaximumWidth(250)
        header_layout.addWidget(self.search_input)

        # Add user button
        add_btn = QPushButton("Add User")
        add_btn.setObjectName("primary_button")
        header_layout.addWidget(add_btn)

        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # Users table
        self.table = QTableWidget()
        self.table.setObjectName("admin_table")
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Username", "Email", "Full Name", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

    def load_users(self, users: list):
        """Load users into table."""
        self.table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.table.setItem(row, 0, QTableWidgetItem(user.username))
            self.table.setItem(row, 1, QTableWidgetItem(user.email))
            self.table.setItem(row, 2, QTableWidgetItem(user.full_name))

            status = "Active" if user.is_active else "Inactive"
            self.table.setItem(row, 3, QTableWidgetItem(status))

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)

            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("small_button")
            actions_layout.addWidget(edit_btn)

            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("danger_button")
            actions_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 4, actions_widget)
