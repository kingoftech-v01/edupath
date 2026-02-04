package com.edupath.ui.screens.courses

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.domain.model.Course
import com.edupath.domain.usecase.GetCourseBySlugUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the course detail screen.
 *
 * @property course The course data (null while loading or if not found)
 * @property isLoading Whether the course is being loaded
 * @property error Error message if loading failed
 */
data class CourseDetailUiState(
    val course: Course? = null,
    val isLoading: Boolean = true,
    val error: String? = null
)

/**
 * ViewModel for the course detail screen.
 *
 * Loads and manages the state for displaying a single course's
 * detailed information.
 *
 * @property getCourseBySlugUseCase Use case for fetching course by slug
 */
@HiltViewModel
class CourseDetailViewModel @Inject constructor(
    private val getCourseBySlugUseCase: GetCourseBySlugUseCase
) : ViewModel() {

    private val _uiState = MutableStateFlow(CourseDetailUiState())

    /** Observable course detail UI state. */
    val uiState: StateFlow<CourseDetailUiState> = _uiState.asStateFlow()

    /**
     * Loads a course by its URL slug.
     *
     * Sets isLoading during fetch and populates course data
     * or error message based on the result.
     *
     * @param slug Unique course identifier
     */
    fun loadCourse(slug: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            val course = getCourseBySlugUseCase(slug)

            _uiState.update {
                it.copy(
                    course = course,
                    isLoading = false,
                    error = if (course == null) "Course not found" else null
                )
            }
        }
    }
}
