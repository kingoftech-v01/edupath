package com.edupath.ui.screens.player

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.data.repository.CourseRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the video player screen.
 *
 * @property courseTitle Title of the course being played
 * @property courseDescription Course description text
 * @property videoUrl URL of the video to play
 * @property isLoading Whether course data is being loaded
 * @property error Error message if loading failed
 */
data class PlayerUiState(
    val courseTitle: String = "",
    val courseDescription: String = "",
    val videoUrl: String = "",
    val isLoading: Boolean = true,
    val error: String? = null
)

/**
 * ViewModel for the video player screen.
 *
 * Loads course metadata and video URL for playback.
 * The actual video playback is handled by ExoPlayer in the composable.
 *
 * @property courseRepository Repository for fetching course data
 */
@HiltViewModel
class PlayerViewModel @Inject constructor(
    private val courseRepository: CourseRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(PlayerUiState())
    val uiState: StateFlow<PlayerUiState> = _uiState.asStateFlow()

    fun loadCourse(courseId: Int) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            try {
                val courses = courseRepository.getCourses().first()
                val course = courses.find { it.id == courseId }

                if (course != null) {
                    _uiState.update {
                        it.copy(
                            courseTitle = course.title,
                            courseDescription = course.desc,
                            videoUrl = course.videoUrl,
                            isLoading = false
                        )
                    }
                } else {
                    _uiState.update {
                        it.copy(isLoading = false, error = "Course not found")
                    }
                }
            } catch (e: Exception) {
                _uiState.update {
                    it.copy(isLoading = false, error = e.message)
                }
            }
        }
    }
}
