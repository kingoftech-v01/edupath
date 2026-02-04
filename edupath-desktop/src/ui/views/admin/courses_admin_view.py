"""
Courses Admin View.

Admin interface for managing courses.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QLineEdit, QComboBox, QHeaderView, QDialog,
    QFormLayout, QTextEdit, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt

from models.course import Course


class CourseEditDialog(QDialog):
    """Dialog for editing course."""

    def __init__(self, course: Course = None, parent=None):
        super().__init__(parent)
        self.course = course
        self.setWindowTitle("Edit Course" if course else "Add Course")
        self.setMinimumSize(500, 400)
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QFormLayout(self)

        # Title
        self.title_input = QLineEdit()
        if self.course:
            self.title_input.setText(self.course.title)
        layout.addRow("Title:", self.title_input)

        # Description
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        if self.course:
            self.desc_input.setText(self.course.desc)
        layout.addRow("Description:", self.desc_input)

        # Price
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0, 9999)
        self.price_input.setDecimals(2)
        if self.course:
            self.price_input.setValue(float(self.course.price))
        layout.addRow("Price:", self.price_input)

        # Lessons
        self.lessons_input = QSpinBox()
        self.lessons_input.setRange(0, 999)
        if self.course:
            self.lessons_input.setValue(self.course.lessons)
        layout.addRow("Lessons:", self.lessons_input)

        # Duration
        self.duration_input = QSpinBox()
        self.duration_input.setRange(0, 999)
        if self.course:
            self.duration_input.setValue(self.course.duration_hours)
        layout.addRow("Duration (hours):", self.duration_input)

        # Buttons
        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setObjectName("primary_button")
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)

        layout.addRow("", buttons_layout)

    def get_data(self) -> dict:
        """Get form data."""
        return {
            "title": self.title_input.text(),
            "desc": self.desc_input.toPlainText(),
            "price": self.price_input.value(),
            "lessons": self.lessons_input.value(),
            "duration_hours": self.duration_input.value(),
        }


class CoursesAdminView(QWidget):
    """Admin view for course management."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._courses = []
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Course Management")
        title.setObjectName("admin_title")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Filters
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories", "")
        self.category_combo.setMinimumWidth(150)
        header_layout.addWidget(self.category_combo)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses...")
        self.search_input.setMaximumWidth(250)
        header_layout.addWidget(self.search_input)

        # Add course button
        add_btn = QPushButton("Add Course")
        add_btn.setObjectName("primary_button")
        add_btn.clicked.connect(self._on_add_course)
        header_layout.addWidget(add_btn)

        layout.addLayout(header_layout)
        layout.addSpacing(20)

        # Courses table
        self.table = QTableWidget()
        self.table.setObjectName("admin_table")
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Title", "Category", "Instructor", "Price", "Students", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)

        layout.addWidget(self.table)

    def load_courses(self, courses: list):
        """Load courses into table."""
        self._courses = courses
        self.table.setRowCount(len(courses))

        for row, course in enumerate(courses):
            self.table.setItem(row, 0, QTableWidgetItem(course.title))

            category = course.category.name if course.category else "-"
            self.table.setItem(row, 1, QTableWidgetItem(category))

            instructor = course.instructor.name if course.instructor else course.name
            self.table.setItem(row, 2, QTableWidgetItem(instructor))

            self.table.setItem(row, 3, QTableWidgetItem(course.formatted_price))
            self.table.setItem(row, 4, QTableWidgetItem(str(course.students)))

            status = "Active" if course.is_active else "Inactive"
            self.table.setItem(row, 5, QTableWidgetItem(status))

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)

            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("small_button")
            edit_btn.clicked.connect(lambda checked, c=course: self._on_edit_course(c))
            actions_layout.addWidget(edit_btn)

            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("danger_button")
            actions_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 6, actions_widget)

    def _on_add_course(self):
        """Handle add course."""
        dialog = CourseEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            # TODO: Send to API

    def _on_edit_course(self, course: Course):
        """Handle edit course."""
        dialog = CourseEditDialog(course=course, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            # TODO: Send to API
