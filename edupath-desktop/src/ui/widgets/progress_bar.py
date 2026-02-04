"""
Progress Bar Widget.

A custom progress bar for course completion tracking.
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt


class ProgressBar(QWidget):
    """Custom progress bar with label."""

    def __init__(self, label: str = "", parent=None):
        super().__init__(parent)
        self._setup_ui(label)

    def _setup_ui(self, label: str):
        """Setup UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Label
        if label:
            self.label = QLabel(label)
            self.label.setObjectName("progress_label")
            layout.addWidget(self.label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)

        # Percentage label
        self.percentage_label = QLabel("0%")
        self.percentage_label.setObjectName("percentage_label")
        self.percentage_label.setMinimumWidth(40)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(self.percentage_label)

    def set_value(self, value: int):
        """Set progress value (0-100)."""
        value = max(0, min(100, value))
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")

    def set_label(self, text: str):
        """Set label text."""
        if hasattr(self, 'label'):
            self.label.setText(text)

    def value(self) -> int:
        """Get current value."""
        return self.progress_bar.value()
