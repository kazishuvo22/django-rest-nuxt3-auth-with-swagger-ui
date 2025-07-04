import { defineStore } from 'pinia'
import { authApi } from '@auth/api/authApi'
import { useRuntimeConfig, navigateTo } from '#app'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: null,
        refreshToken: null,
        isRefreshing: false,
        refreshPromise: null,
        userProfile: null,
        isActiveUser: false,
        isAdmin: false,
        isSuperAdmin: false,
    }),

    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        isUserAdmin: (state) => state.isAdmin,
        isUserSuperAdmin: (state) => state.isSuperAdmin,
        isUserActive: (state) => state.isActiveUser,
    },

    actions: {
        async login(credentials) {
            try {
                const config = useRuntimeConfig()
                const response = await authApi.login(credentials, {
                    $fetch,
                    apiBase: config.public.apiBase,
                })

                // Extract tokens and user info
                this.accessToken = response.access_token
                this.refreshToken = response.refresh_token
                this.isActiveUser = !!response.user.is_active
                this.isAdmin = !!response.user.is_staff
                this.isSuperAdmin = !!response.user.is_superuser
                this.userProfile = {
                    id: response.user.id,
                    username: response.user.username,
                    email: response.user.email,
                }

                // Save tokens to localStorage
                localStorage.setItem('accessToken', response.access_token)
                localStorage.setItem('refreshToken', response.refresh_token)

                // Save expiration time for auto-refresh
                const expirationTime = Date.now() + response.expires_in * 1000
                localStorage.setItem('accessTokenExpiresAt', expirationTime)

                console.log('Login successful:', response)
                return response
            } catch (error) {
                console.error('Login failed:', error)
                throw error
            }
        },

        async refreshAccessToken() {
            if (this.isRefreshing) {
                return this.refreshPromise
            }

            if (!this.refreshToken) {
                throw new Error('No refresh token available')
            }

            this.isRefreshing = true
            this.refreshPromise = authApi.refresh(this.refreshToken, {
                $fetch,
                apiBase: useRuntimeConfig().public.apiBase,
            })

            try {
                const response = await this.refreshPromise
                this.accessToken = response.access_token
                const expirationTime = Date.now() + response.expires_in * 1000
                localStorage.setItem('accessToken', response.access_token)
                localStorage.setItem('accessTokenExpiresAt', expirationTime)
                console.log('Token refreshed successfully')
                return response.access_token
            } catch (error) {
                console.error('Token refresh error:', error)
                this.logout()
                throw error
            } finally {
                this.isRefreshing = false
                this.refreshPromise = null
            }
        },

        async autoRefreshAccessToken() {
            const expirationTime = localStorage.getItem('accessTokenExpiresAt')
            if (expirationTime && Date.now() > expirationTime) {
                console.log('Access token expired. Refreshing...')
                await this.refreshAccessToken()
            }
        },

        async fetchUserProfile() {
            if (!this.accessToken) {
                throw new Error('No access token available')
            }

            try {
                const config = useRuntimeConfig()
                const profile = await authApi.getProfile({
                    $fetch,
                    apiBase: config.public.apiBase,
                    accessToken: this.accessToken,
                })

                this.userProfile = profile

                // Update user roles
                this.isActiveUser = !!profile.is_active
                this.isAdmin = !!profile.is_staff
                this.isSuperAdmin = !!profile.is_superuser

                console.log('User profile fetched:', profile)
                return profile
            } catch (error) {
                console.error('Failed to fetch user profile:', error)
                throw error
            }
        },

        loadTokens() {
            this.accessToken = localStorage.getItem('accessToken')
            this.refreshToken = localStorage.getItem('refreshToken')
            const expirationTime = localStorage.getItem('accessTokenExpiresAt')
            if (expirationTime && Date.now() > expirationTime) {
                this.accessToken = null
            }
        },

        logout() {
            this.accessToken = null
            this.refreshToken = null
            this.userProfile = null
            this.isActiveUser = false
            this.isAdmin = false
            this.isSuperAdmin = false
            localStorage.removeItem('accessToken')
            localStorage.removeItem('refreshToken')
            localStorage.removeItem('accessTokenExpiresAt')
            navigateTo('/login')
        },
    },
})
