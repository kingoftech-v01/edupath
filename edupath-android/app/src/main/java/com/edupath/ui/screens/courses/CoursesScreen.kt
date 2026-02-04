package com.edupath.ui.screens.courses

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.edupath.ui.components.CourseCard

/**
 * Courses listing screen with search and category filtering.
 *
 * Displays all courses in an adaptive grid with search functionality
 * and category tabs for filtering. Shows loading and empty states.
 *
 * Features:
 * - Search bar with debounced query input
 * - Scrollable category tabs for filtering
 * - Adaptive grid that adjusts columns based on screen width
 * - Loading spinner and empty state handling
 *
 * @param onCourseClick Callback with course slug when a course is tapped
 * @param onBackClick Callback to navigate back
 * @param viewModel ViewModel managing courses state, injected via Hilt
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun CoursesScreen(
    onCourseClick: (String) -> Unit,
    onBackClick: () -> Unit,
    viewModel: CoursesViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("All Courses") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            // Search bar
            OutlinedTextField(
                value = uiState.searchQuery,
                onValueChange = viewModel::onSearchQueryChange,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                placeholder = { Text("Search courses...") },
                leadingIcon = {
                    Icon(Icons.Default.Search, contentDescription = "Search")
                },
                singleLine = true
            )

            // Category filters
            ScrollableTabRow(
                selectedTabIndex = uiState.categories.indexOfFirst { it.slug == uiState.selectedCategory }
                    .coerceAtLeast(0),
                modifier = Modifier.fillMaxWidth()
            ) {
                Tab(
                    selected = uiState.selectedCategory == null,
                    onClick = { viewModel.onCategorySelect(null) },
                    text = { Text("All") }
                )
                uiState.categories.forEach { category ->
                    Tab(
                        selected = category.slug == uiState.selectedCategory,
                        onClick = { viewModel.onCategorySelect(category.slug) },
                        text = { Text(category.name) }
                    )
                }
            }

            // Courses grid
            if (uiState.isLoading) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            } else if (uiState.courses.isEmpty()) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "No courses found",
                        style = MaterialTheme.typography.bodyLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            } else {
                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 300.dp),
                    contentPadding = PaddingValues(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.courses) { course ->
                        CourseCard(
                            course = course,
                            onClick = { onCourseClick(course.slug) }
                        )
                    }
                }
            }
        }
    }
}
