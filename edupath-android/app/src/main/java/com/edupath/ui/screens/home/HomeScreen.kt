package com.edupath.ui.screens.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ExitToApp
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import com.edupath.ui.components.CourseCard

/**
 * Home screen composable displaying the main dashboard.
 *
 * Shows a welcome message, statistics, featured courses, and
 * category chips. Provides navigation to courses list and logout.
 *
 * Sections:
 * - Welcome header with user greeting
 * - Stats row showing total courses, categories, and featured count
 * - Featured courses in a horizontal scrolling row
 * - Categories displayed as filter chips
 *
 * @param onNavigateToCourses Callback to navigate to full courses list
 * @param onCourseClick Callback with course slug when a course is tapped
 * @param onLogout Callback invoked when user logs out
 * @param viewModel ViewModel managing home screen state, injected via Hilt
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onNavigateToCourses: () -> Unit,
    onCourseClick: (String) -> Unit,
    onLogout: () -> Unit,
    viewModel: HomeViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()

    LaunchedEffect(uiState.loggedOut) {
        if (uiState.loggedOut) {
            onLogout()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("EduPath") },
                actions = {
                    IconButton(onClick = viewModel::logout) {
                        Icon(Icons.Default.ExitToApp, contentDescription = "Logout")
                    }
                }
            )
        }
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding),
            contentPadding = PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(24.dp)
        ) {
            // Welcome section
            item {
                Column {
                    Text(
                        text = "Welcome back!",
                        style = MaterialTheme.typography.headlineMedium
                    )
                    Text(
                        text = "Continue your learning journey",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            // Stats row
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    StatCard(
                        title = "Courses",
                        value = uiState.totalCourses.toString(),
                        modifier = Modifier.weight(1f)
                    )
                    StatCard(
                        title = "Categories",
                        value = uiState.totalCategories.toString(),
                        modifier = Modifier.weight(1f)
                    )
                    StatCard(
                        title = "Featured",
                        value = uiState.featuredCourses.size.toString(),
                        modifier = Modifier.weight(1f)
                    )
                }
            }

            // Featured courses section
            item {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "Featured Courses",
                        style = MaterialTheme.typography.titleLarge
                    )
                    TextButton(onClick = onNavigateToCourses) {
                        Text("See All")
                    }
                }
            }

            item {
                if (uiState.isLoading) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(200.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        CircularProgressIndicator()
                    }
                } else {
                    LazyRow(
                        horizontalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(uiState.featuredCourses) { course ->
                            CourseCard(
                                course = course,
                                onClick = { onCourseClick(course.slug) },
                                modifier = Modifier.width(280.dp)
                            )
                        }
                    }
                }
            }

            // Categories section
            item {
                Text(
                    text = "Categories",
                    style = MaterialTheme.typography.titleLarge
                )
            }

            item {
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    items(uiState.categories) { category ->
                        FilterChip(
                            selected = false,
                            onClick = { /* Navigate to category */ },
                            label = { Text("${category.name} (${category.courseCount})") }
                        )
                    }
                }
            }
        }
    }
}

/**
 * Reusable statistic card component for dashboard metrics.
 *
 * Displays a centered value with a title label below it,
 * styled with the primary color for emphasis.
 *
 * @param title Label describing the statistic
 * @param value Numeric or text value to display prominently
 * @param modifier Modifier for layout customization
 */
@Composable
fun StatCard(
    title: String,
    value: String,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
    ) {
        Column(
            modifier = Modifier.padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Text(
                text = title,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
