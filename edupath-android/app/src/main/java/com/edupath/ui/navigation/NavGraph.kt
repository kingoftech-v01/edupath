package com.edupath.ui.navigation

import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.edupath.ui.screens.auth.LoginScreen
import com.edupath.ui.screens.home.HomeScreen
import com.edupath.ui.screens.courses.CoursesScreen
import com.edupath.ui.screens.courses.CourseDetailScreen
import com.edupath.ui.screens.player.VideoPlayerScreen
import com.edupath.ui.screens.admin.AdminDashboardScreen

/**
 * Sealed class defining all navigation destinations in the app.
 *
 * Each screen is represented as an object with its route pattern.
 * Some screens accept arguments (slug, courseId) which are embedded in the route.
 */
sealed class Screen(val route: String) {
    /** Login screen for unauthenticated users. */
    object Login : Screen("login")

    /** Home screen with featured courses and categories. */
    object Home : Screen("home")

    /** Course listing screen with filtering. */
    object Courses : Screen("courses")

    /** Course detail screen, requires course slug. */
    object CourseDetail : Screen("course/{slug}") {
        /**
         * Creates navigation route with the course slug.
         * @param slug Course identifier
         */
        fun createRoute(slug: String) = "course/$slug"
    }

    /** Video player screen, requires course ID. */
    object VideoPlayer : Screen("player/{courseId}") {
        /**
         * Creates navigation route with the course ID.
         * @param courseId Course identifier
         */
        fun createRoute(courseId: Int) = "player/$courseId"
    }

    /** Admin dashboard (staff only). */
    object Admin : Screen("admin")

    /** User profile screen. */
    object Profile : Screen("profile")
}

/**
 * Main navigation graph for the EduPath app.
 *
 * Defines all composable destinations and their navigation transitions.
 * Uses Jetpack Compose Navigation with type-safe arguments.
 *
 * @param navController The navigation controller for managing back stack
 * @param startDestination Initial screen route (Login or Home based on auth)
 */
@Composable
fun EduPathNavGraph(
    navController: NavHostController,
    startDestination: String = Screen.Login.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        // Login screen - navigates to Home on success
        composable(Screen.Login.route) {
            LoginScreen(
                onLoginSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Login.route) { inclusive = true }
                    }
                }
            )
        }

        // Home screen - main entry point after login
        composable(Screen.Home.route) {
            HomeScreen(
                onNavigateToCourses = {
                    navController.navigate(Screen.Courses.route)
                },
                onCourseClick = { slug ->
                    navController.navigate(Screen.CourseDetail.createRoute(slug))
                },
                onLogout = {
                    navController.navigate(Screen.Login.route) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }

        // Course listing screen
        composable(Screen.Courses.route) {
            CoursesScreen(
                onCourseClick = { slug ->
                    navController.navigate(Screen.CourseDetail.createRoute(slug))
                },
                onBackClick = {
                    navController.popBackStack()
                }
            )
        }

        // Course detail screen with slug argument
        composable(
            route = Screen.CourseDetail.route,
            arguments = listOf(navArgument("slug") { type = NavType.StringType })
        ) { backStackEntry ->
            val slug = backStackEntry.arguments?.getString("slug") ?: ""
            CourseDetailScreen(
                slug = slug,
                onBackClick = {
                    navController.popBackStack()
                },
                onPlayVideo = { courseId ->
                    navController.navigate(Screen.VideoPlayer.createRoute(courseId))
                }
            )
        }

        // Video player screen with courseId argument
        composable(
            route = Screen.VideoPlayer.route,
            arguments = listOf(navArgument("courseId") { type = NavType.IntType })
        ) { backStackEntry ->
            val courseId = backStackEntry.arguments?.getInt("courseId") ?: 0
            VideoPlayerScreen(
                courseId = courseId,
                onBackClick = {
                    navController.popBackStack()
                }
            )
        }

        // Admin dashboard screen
        composable(Screen.Admin.route) {
            AdminDashboardScreen(
                onBackClick = {
                    navController.popBackStack()
                }
            )
        }
    }
}
