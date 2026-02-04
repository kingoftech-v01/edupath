package com.edupath.ui.screens.admin

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.domain.model.Course
import com.edupath.domain.usecase.GetCoursesUseCase
import com.edupath.data.repository.CourseRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the admin dashboard screen.
 *
 * @property totalCourses Total number of courses in the platform
 * @property totalCategories Total number of course categories
 * @property totalInstructors Total number of instructors
 * @property totalStudents Aggregate count of enrolled students
 * @property recentCourses List of recently added courses (up to 5)
 * @property isLoading Whether data is being loaded
 * @property error Error message if loading failed
 */
data class AdminUiState(
    val totalCourses: Int = 0,
    val totalCategories: Int = 0,
    val totalInstructors: Int = 0,
    val totalStudents: Int = 0,
    val recentCourses: List<Course> = emptyList(),
    val isLoading: Boolean = true,
    val error: String? = null
)

/**
 * ViewModel for the admin dashboard screen.
 *
 * Aggregates platform statistics including course counts,
 * categories, and student enrollment numbers.
 *
 * @property getCoursesUseCase Use case for fetching all courses
 * @property courseRepository Repository for category data
 */
@HiltViewModel
class AdminViewModel @Inject constructor(
    private val getCoursesUseCase: GetCoursesUseCase,
    private val courseRepository: CourseRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AdminUiState())
    val uiState: StateFlow<AdminUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    private fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            // Collect courses
            launch {
                getCoursesUseCase().collect { courses ->
                    val totalStudents = courses.sumOf { it.students }
                    _uiState.update {
                        it.copy(
                            totalCourses = courses.size,
                            totalStudents = totalStudents,
                            recentCourses = courses.take(5),
                            isLoading = false
                        )
                    }
                }
            }

            // Collect categories
            launch {
                courseRepository.getCategories().collect { categories ->
                    _uiState.update { it.copy(totalCategories = categories.size) }
                }
            }
        }
    }
}
