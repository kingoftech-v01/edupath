package com.edupath.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.edupath.data.repository.AuthRepository
import com.edupath.ui.navigation.EduPathNavGraph
import com.edupath.ui.navigation.Screen
import com.edupath.ui.theme.EduPathTheme
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * Main entry point for the EduPath Android application.
 *
 * This single-activity architecture hosts all Compose screens via navigation.
 * On startup, checks authentication status to determine the initial screen:
 * - Authenticated users go to Home screen
 * - Unauthenticated users go to Login screen
 */
@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    /**
     * Auth repository for checking login status.
     */
    @Inject
    lateinit var authRepository: AuthRepository

    /**
     * Sets up the Compose UI with theme and navigation.
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            EduPathTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val navController = rememberNavController()
                    var startDestination by remember { mutableStateOf<String?>(null) }
                    val scope = rememberCoroutineScope()

                    // Check auth status to determine start screen
                    LaunchedEffect(Unit) {
                        scope.launch {
                            startDestination = if (authRepository.isLoggedIn()) {
                                Screen.Home.route
                            } else {
                                Screen.Login.route
                            }
                        }
                    }

                    // Only show navigation after determining start destination
                    startDestination?.let { destination ->
                        EduPathNavGraph(
                            navController = navController,
                            startDestination = destination
                        )
                    }
                }
            }
        }
    }
}
