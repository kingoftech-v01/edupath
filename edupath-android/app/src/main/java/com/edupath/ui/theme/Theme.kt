package com.edupath.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

/**
 * Dark color scheme using EduPath brand colors.
 */
private val DarkColorScheme = darkColorScheme(
    primary = Violet600,
    onPrimary = TextPrimary,
    secondary = Violet700,
    onSecondary = TextPrimary,
    tertiary = Violet800,
    onTertiary = TextPrimary,
    background = DarkBackground,
    onBackground = TextPrimary,
    surface = DarkSurface,
    onSurface = TextPrimary,
    surfaceVariant = DarkSurfaceVariant,
    onSurfaceVariant = TextSecondary,
    error = Error,
    onError = TextPrimary
)

/**
 * Light color scheme using EduPath brand colors.
 */
private val LightColorScheme = lightColorScheme(
    primary = Violet600,
    onPrimary = LightSurface,
    secondary = Violet700,
    onSecondary = LightSurface,
    tertiary = Violet800,
    onTertiary = LightSurface,
    background = LightBackground,
    onBackground = TextDark,
    surface = LightSurface,
    onSurface = TextDark,
    surfaceVariant = LightBackground,
    onSurfaceVariant = TextDark,
    error = Error,
    onError = LightSurface
)

/**
 * EduPath application theme wrapper.
 *
 * Applies Material 3 theming with EduPath brand colors.
 * Supports dark/light mode and Android 12+ dynamic colors.
 *
 * @param darkTheme Whether to use dark theme (default: system setting)
 * @param dynamicColor Whether to use Android 12+ dynamic colors
 * @param content The composable content to wrap with the theme
 */
@Composable
fun EduPathTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    // Determine color scheme based on settings
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    // Update status bar color to match theme
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.background.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
