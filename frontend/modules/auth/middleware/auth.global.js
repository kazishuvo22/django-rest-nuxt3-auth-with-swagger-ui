import { useAuthStore } from '@auth/stores/auth'

export default defineNuxtRouteMiddleware(async () => {
    const authStore = useAuthStore()
    authStore.loadTokens()

    if (!authStore.isAuthenticated) {
        return navigateTo('/login')
    }

    // Refresh token if needed
    await authStore.autoRefreshAccessToken()
})