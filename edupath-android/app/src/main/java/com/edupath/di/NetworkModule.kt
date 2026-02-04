package com.edupath.di

import com.edupath.BuildConfig
import com.edupath.data.api.AuthInterceptor
import com.edupath.data.api.EduPathApi
import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

/**
 * Hilt module that provides network-related dependencies.
 *
 * This module configures and provides singleton instances of:
 * - Moshi for JSON serialization/deserialization
 * - OkHttpClient with authentication and logging interceptors
 * - Retrofit for REST API communication
 * - EduPathApi interface implementation
 */
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    /**
     * Provides the Moshi instance for JSON parsing.
     *
     * Configured with KotlinJsonAdapterFactory for proper Kotlin class support.
     *
     * @return Configured Moshi instance
     */
    @Provides
    @Singleton
    fun provideMoshi(): Moshi = Moshi.Builder()
        .add(KotlinJsonAdapterFactory())
        .build()

    /**
     * Provides the OkHttpClient instance for HTTP communication.
     *
     * Configured with:
     * - Authentication interceptor for JWT token injection
     * - Logging interceptor (BODY level in debug, NONE in release)
     * - 30 second timeouts for connect, read, and write operations
     *
     * @param authInterceptor The authentication interceptor for adding JWT tokens
     * @return Configured OkHttpClient instance
     */
    @Provides
    @Singleton
    fun provideOkHttpClient(authInterceptor: AuthInterceptor): OkHttpClient {
        val loggingInterceptor = HttpLoggingInterceptor().apply {
            level = if (BuildConfig.DEBUG) {
                HttpLoggingInterceptor.Level.BODY
            } else {
                HttpLoggingInterceptor.Level.NONE
            }
        }

        return OkHttpClient.Builder()
            .addInterceptor(authInterceptor)
            .addInterceptor(loggingInterceptor)
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .writeTimeout(30, TimeUnit.SECONDS)
            .build()
    }

    /**
     * Provides the Retrofit instance for API communication.
     *
     * Configured with the base URL from BuildConfig and Moshi converter.
     *
     * @param okHttpClient The HTTP client for network requests
     * @param moshi The JSON converter
     * @return Configured Retrofit instance
     */
    @Provides
    @Singleton
    fun provideRetrofit(okHttpClient: OkHttpClient, moshi: Moshi): Retrofit = Retrofit.Builder()
        .baseUrl(BuildConfig.API_BASE_URL)
        .client(okHttpClient)
        .addConverterFactory(MoshiConverterFactory.create(moshi))
        .build()

    /**
     * Provides the EduPath API interface implementation.
     *
     * @param retrofit The Retrofit instance to create the API from
     * @return Implementation of EduPathApi interface
     */
    @Provides
    @Singleton
    fun provideEduPathApi(retrofit: Retrofit): EduPathApi =
        retrofit.create(EduPathApi::class.java)
}
