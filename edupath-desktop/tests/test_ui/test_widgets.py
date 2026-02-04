"""
Tests for UI widgets.
"""

import pytest
from PyQt6.QtCore import Qt

from models.course import Course
from ui.widgets.course_card import CourseCard
from ui.widgets.progress_bar import ProgressBar


class TestCourseCard:
    """Tests for CourseCard widget."""

    def test_course_card_creation(self, qapp, sample_course):
        """Test course card creation."""
        course = Course(**sample_course)
        card = CourseCard(course)
        assert card.course == course

    def test_course_card_emits_clicked(self, qapp, sample_course, qtbot):
        """Test course card emits clicked signal."""
        course = Course(**sample_course)
        card = CourseCard(course)

        with qtbot.waitSignal(card.clicked, timeout=1000):
            qtbot.mouseClick(card, Qt.MouseButton.LeftButton)


class TestProgressBar:
    """Tests for ProgressBar widget."""

    def test_progress_bar_creation(self, qapp):
        """Test progress bar creation."""
        bar = ProgressBar("Progress")
        assert bar.value() == 0

    def test_progress_bar_set_value(self, qapp):
        """Test setting progress value."""
        bar = ProgressBar()
        bar.set_value(50)
        assert bar.value() == 50

    def test_progress_bar_clamps_value(self, qapp):
        """Test progress value is clamped to 0-100."""
        bar = ProgressBar()

        bar.set_value(150)
        assert bar.value() == 100

        bar.set_value(-10)
        assert bar.value() == 0

    def test_progress_bar_percentage_label(self, qapp):
        """Test percentage label is updated."""
        bar = ProgressBar()
        bar.set_value(75)
        assert bar.percentage_label.text() == "75%"
