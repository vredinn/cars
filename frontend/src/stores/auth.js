import { defineStore } from 'pinia'
import { ref } from 'vue'
import api, { refreshAuthToken } from '@/api'

let refreshTimer

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)

    async function fetchUser() {
        try {
            const res = await api.get('/auth/me')
            user.value = res.data
        } catch (e) {
            user.value = null
            throw e
        }
    }

    async function refreshSession() {
        try {
            await refreshAuthToken()
        } catch (e) {
            console.warn('Auto-refresh failed', e)
        }
    }

    function startAutoRefresh() {
        stopAutoRefresh()
        refreshTimer = setInterval(refreshSession, 14 * 60 * 1000)
    }

    function stopAutoRefresh() {
        if (refreshTimer) clearInterval(refreshTimer)
    }

    async function logout() {
        await api.post('/auth/logout')
        stopAutoRefresh()
        user.value = null
        window.location.reload()
    }

    return {
        user,
        fetchUser,
        refreshSession,
        startAutoRefresh,
        stopAutoRefresh,
        logout
    }
})