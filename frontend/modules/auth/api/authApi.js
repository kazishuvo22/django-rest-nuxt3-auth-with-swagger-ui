export const authApi = {
    login: async (credentials, { $fetch, apiBase }) => {
        return await $fetch('auth/login/', {
            baseURL: apiBase,
            method: 'POST',
            body: credentials,
        })
    },
    refresh: async (refreshToken, { $fetch, apiBase }) => {
        return await $fetch('auth/token/refresh/', {
            baseURL: apiBase,
            method: 'POST',
            body: { refresh: refreshToken },
        })
    },
    getProfile: async ({ $fetch, apiBase, accessToken }) => {
        return await $fetch('auth/users/me/', {
            baseURL: apiBase,
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        })
    },
}