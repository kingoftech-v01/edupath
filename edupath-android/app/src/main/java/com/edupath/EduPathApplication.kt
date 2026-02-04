package com.edupath

import android.app.Application
import dagger.hilt.android.HiltAndroidApp

/**
 * Main Application class for EduPath.
 * Initializes Hilt dependency injection.
 */
@HiltAndroidApp
class EduPathApplication : Application()
