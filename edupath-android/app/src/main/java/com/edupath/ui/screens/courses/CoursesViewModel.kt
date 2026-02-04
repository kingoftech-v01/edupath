package com.edupath.ui.screens.courses

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.edupath.domain.model.Category
import com.edupath.domain.model.Course
import com.edupath.domain.usecase.GetCoursesUseCase
import com.edupath.domain.usecase.SearchCoursesUseCase
import com.edupath.data.repository.CourseRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI state for the courses list screen.
 *
 * @property courses List of courses to display
 * @property categories Available categories for filtering
 * @property selectedCategory Currently selected category slug (null = all)
 * @property searchQuery Current search query
 * @property isLoading Whether data is being loaded
 * @property error Error message if loading failed
 */
data class CoursesUiState(
    val courses: List<Course> = emptyList(),
    val categories: List<Category> = emptyList(),
    val selectedCategory: String? = null,
    val searchQuery: String = "",
    val isLoading: Boolean = true,
    val error: String? = null
)

/**
 * ViewModel for the courses list screen.
 *
 * Manages course listing with search and category filtering.
 * Supports debounced search to avoid excessive API calls.
 *
 * @property getCoursesUseCase Use case for fetching all courses
 * @property searchCoursesUseCase Use case for searching courses
 * @property courseRepository Repository for category data
 */
@HiltViewModel
class CoursesViewModel @Inject constructor(
    private val getCoursesUseCase: GetCoursesUseCase,
    private val searchCoursesUseCase: SearchCoursesUseCase,
    private val courseRepository: CourseRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(CoursesUiState())

    /** Observable courses UI state. */
    val uiState: StateFlow<CoursesUiState> = _uiState.asStateFlow()

    private var searchJob: Job? = null

    init {
        loadData()
    }

    /**
     * Loads courses and categories from the repository.
     */
    private fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            // Collect courses
            launch {
                getCoursesUseCase().collect { courses ->
                    _uiState.update { state ->
                        val filteredCourses = filterCourses(courses, state.selectedCategory)
                        state.copy(courses = filteredCourses, isLoading = false)
                    }
                }
            }

            // Collect categories
            launch {
                courseRepository.getCategories().collect { categories ->
                    _uiState.update { it.copy(categories = categories) }
                }
            }
        }
    }

    /**
     * Handles search query changes with debouncing.
     *
     * Waits 300ms after last input before searching to reduce
     * unnecessary API calls.
     *
     * @param query New search query
     */
    fun onSearchQueryChange(query: String) {
        _uiState.update { it.copy(searchQuery = query) }

        searchJob?.cancel()
        searchJob = viewModelScope.launch {
            delay(300) // Debounce
            if (query.isBlank()) {
                loadData()
            } else {
                _uiState.update { it.copy(isLoading = true) }
                val results = searchCoursesUseCase(query)
                _uiState.update { it.copy(courses = results, isLoading = false) }
            }
        }
    }

    /**
     * Filters courses by selected category.
     *
     * @param categorySlug Category slug to filter by, or null for all
     */
    fun onCategorySelect(categorySlug: String?) {
        _uiState.update { it.copy(selectedCategory = categorySlug) }

        viewModelScope.launch {
            getCoursesUseCase().first().let { allCourses ->
                val filtered = filterCourses(allCourses, categorySlug)
                _uiState.update { it.copy(courses = filtered) }
            }
        }
    }

    /**
     * Filters courses by category.
     *
     * @param courses Full course list
     * @param categorySlug Category to filter by, or null for all
     * @return Filtered course list
     */
    private fun filterCourses(courses: List<Course>, categorySlug: String?): List<Course> {
        return if (categorySlug == null) {
            courses
        } else {
            courses.filter { it.categoryId != null }
        }
    }
}
