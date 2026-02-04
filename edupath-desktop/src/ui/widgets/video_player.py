"""
Video Player Widget.

A video player using Qt Multimedia.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QSlider, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QWidget):
    """Video player widget with controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_media()

    def _setup_ui(self):
        """Setup UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Video widget
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(400)
        self.video_widget.setObjectName("video_widget")
        layout.addWidget(self.video_widget)

        # Controls
        controls = QFrame()
        controls.setObjectName("video_controls")
        controls_layout = QHBoxLayout(controls)

        # Play/Pause button
        self.play_btn = QPushButton("▶")
        self.play_btn.setObjectName("play_button")
        self.play_btn.setFixedSize(40, 40)
        self.play_btn.clicked.connect(self._toggle_play)
        controls_layout.addWidget(self.play_btn)

        # Progress slider
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setObjectName("progress_slider")
        self.progress_slider.sliderMoved.connect(self._seek)
        controls_layout.addWidget(self.progress_slider)

        # Time label
        self.time_label = QLabel("00:00 / 00:00")
        self.time_label.setObjectName("time_label")
        controls_layout.addWidget(self.time_label)

        # Volume slider
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setObjectName("volume_slider")
        self.volume_slider.setMaximumWidth(100)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self._set_volume)
        controls_layout.addWidget(self.volume_slider)

        layout.addWidget(controls)

    def _setup_media(self):
        """Setup media player."""
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)

        # Connect signals
        self.player.positionChanged.connect(self._on_position_changed)
        self.player.durationChanged.connect(self._on_duration_changed)
        self.player.playbackStateChanged.connect(self._on_state_changed)

    def set_source(self, url: str):
        """Set video source URL."""
        self.player.setSource(QUrl(url))

    def play(self):
        """Play video."""
        self.player.play()

    def pause(self):
        """Pause video."""
        self.player.pause()

    def stop(self):
        """Stop video."""
        self.player.stop()

    def _toggle_play(self):
        """Toggle play/pause."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.pause()
        else:
            self.play()

    def _seek(self, position: int):
        """Seek to position."""
        self.player.setPosition(position)

    def _set_volume(self, value: int):
        """Set volume."""
        self.audio_output.setVolume(value / 100)

    def _on_position_changed(self, position: int):
        """Handle position change."""
        self.progress_slider.setValue(position)
        self._update_time_label(position, self.player.duration())

    def _on_duration_changed(self, duration: int):
        """Handle duration change."""
        self.progress_slider.setRange(0, duration)
        self._update_time_label(self.player.position(), duration)

    def _on_state_changed(self, state: QMediaPlayer.PlaybackState):
        """Handle playback state change."""
        if state == QMediaPlayer.PlaybackState.PlayingState:
            self.play_btn.setText("⏸")
        else:
            self.play_btn.setText("▶")

    def _update_time_label(self, position: int, duration: int):
        """Update time label."""
        pos_str = self._format_time(position)
        dur_str = self._format_time(duration)
        self.time_label.setText(f"{pos_str} / {dur_str}")

    def _format_time(self, ms: int) -> str:
        """Format milliseconds to MM:SS."""
        seconds = ms // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
