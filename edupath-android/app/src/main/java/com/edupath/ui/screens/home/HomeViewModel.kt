package com.edupath.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.domain.model.Category
import com.edupath.domain.model.Course
import com.edupath.domain.usecase.*
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the home screen dashboard.
 *
 * @property featuredCourses List of featured courses for the carousel
 * @property categories Available course categories
 * @property totalCourses Total number of courses in the system
 * @property totalCategories Total number of categories
 * @property isLoading Whether data is being loaded
 * @property error Error message if loading failed
 * @property loggedOut Whether the user has logged out
 */
data class HomeUiState(
    val featuredCourses: List<Course> = emptyList(),
    val categories: List<Category> = emptyList(),
    val totalCourses: Int = 0,
    val totalCategories: Int = 0,
    val isLoading: Boolean = true,
    val error: String? = null,
    val loggedOut: Boolean = false
)

/**
 * ViewModel for the home screen dashboard.
 *
 * Manages loading and displaying featured courses, categories,
 * and aggregate statistics. Handles user logout.
 *
 * @property getFeaturedCoursesUseCase Use case for fetching featured courses
 * @property getCoursesUseCase Use case for fetching all courses
 * @property refreshCoursesUseCase Use case for refreshing course data from API
 * @property logoutUseCase Use case for user logout
 * @property courseRepository Repository for category data
 */
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getFeaturedCoursesUseCase: GetFeaturedCoursesUseCase,
    private val getCoursesUseCase: GetCoursesUseCase,
    private val refreshCoursesUseCase: RefreshCoursesUseCase,
    private val logoutUseCase: LogoutUseCase,
    private val courseRepository: com.edupath.data.repository.CourseRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    private fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            // Refresh data from API
            refreshCoursesUseCase()
            courseRepository.refreshCategories()

            // Collect featured courses
            launch {
                getFeaturedCoursesUseCase().collect { courses ->
                    _uiState.update { it.copy(featuredCourses = courses) }
                }
            }

            // Collect all courses count
            launch {
                getCoursesUseCase().collect { courses ->
                    _uiState.update { it.copy(totalCourses = courses.size, isLoading = false) }
                }
            }

            // Collect categories
            launch {
                courseRepository.getCategories().collect { categories ->
                    _uiState.update {
                        it.copy(
                            categories = categories,
                            totalCategories = categories.size
                        )
                    }
                }
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            logoutUseCase()
            _uiState.update { it.copy(loggedOut = true) }
        }
    }

    fun refresh() {
        loadData()
    }
}
