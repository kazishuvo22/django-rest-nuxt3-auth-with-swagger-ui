import { useAuthStore } from '@auth/stores/auth'
import { computed } from 'vue'

export const useAuth = () => {
    const authStore = useAuthStore()

    return {
        // Reactive state
        accessToken: computed(() => authStore.accessToken),
        refreshToken: computed(() => authStore.refreshToken),
        userProfile: computed(() => authStore.userProfile),
        isActiveUser: computed(() => authStore.isActiveUser),
        isAdmin: computed(() => authStore.isAdmin),
        isSuperAdmin: computed(() => authStore.isSuperAdmin),

        // Getters
        isAuthenticated: computed(() => authStore.isAuthenticated),

        // Actions
        login: authStore.login,
        logout: authStore.logout,
        refreshAccessToken: authStore.refreshAccessToken,
        fetchUserProfile: authStore.fetchUserProfile,
        loadTokens: authStore.loadTokens,
    }
}