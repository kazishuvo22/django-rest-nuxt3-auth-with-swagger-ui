import {authApi} from '@auth/api/authApi.js'
import {useAuthStore} from '@auth/stores/auth.js'

export default defineNuxtPlugin((nuxtApp) => {
    const authStore = useAuthStore()
    const runtimeConfig = useRuntimeConfig()

    const api = async (url, options = {}) => {
        try {
            return await $fetch(url, {
                ...options,
                baseURL: runtimeConfig.public.apiBase,
                headers: {
                    ...options.headers,
                    Authorization: authStore.accessToken ? `Bearer ${authStore.accessToken}` : '',
                },
            })
        } catch (error) {
            if (error.status === 401) {
                try {
                    await authStore.refreshAccessToken()
                    return await $fetch(url, {
                        ...options,
                        baseURL: runtimeConfig.public.apiBase,
                        headers: {
                            ...options.headers,
                            Authorization: `Bearer ${authStore.accessToken}`,
                        },
                    })
                } catch (refreshError) {
                    navigateTo('/login')
                    throw refreshError
                }
            }
            throw error
        }
    }

    const compositeAuthApi = {
        auth: {
            login: (credentials) => authStore.login(credentials, {$fetch, apiBase: runtimeConfig.public.apiBase}),
            refresh: () => authApi.refresh(authStore.refreshToken, {$fetch, apiBase: runtimeConfig.public.apiBase}),
            getProfile: () => authApi.getProfile({
                $fetch,
                apiBase: runtimeConfig.public.apiBase,
                accessToken: authStore.accessToken
            }),
        },
    }

    return {
        provide: {
            api,
            compositeAuthApi,
        },
    }
})