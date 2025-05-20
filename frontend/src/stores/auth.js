import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { refreshAuthToken } from '@/api'

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const refreshTimer = ref(null)

    const isAuthenticated = computed(() => !!user.value)

    async function fetchUser() {
        try {
            const res = await api.get('/auth/me')
            user.value = res.data
            startAutoRefresh()
        } catch (e) {
            user.value = null
            stopAutoRefresh()
            throw e
        }
    }

    async function refreshSession() {
        try {
            await refreshAuthToken()
            // После обновления токена можно обновить user или состояние сессии:
            await fetchUser()
        } catch (e) {
            console.warn('Auto-refresh failed', e)
            await logout()
        }
    }

    function startAutoRefresh() {
        stopAutoRefresh()
        refreshTimer.value = setInterval(refreshSession, 14 * 60 * 1000) // 14 минут
    }

    function stopAutoRefresh() {
        if (refreshTimer.value) {
            clearInterval(refreshTimer.value)
            refreshTimer.value = null
        }
    }

    async function logout() {
        try {
            await api.post('/auth/logout')
        } catch (e) {
            console.warn('Logout failed', e)
        } finally {
            stopAutoRefresh()
            user.value = null
            // Можно сделать редирект или перезагрузку, как хотите:
            window.location.reload()
        }
    }

    return {
        user,
        isAuthenticated,
        fetchUser,
        refreshSession,
        startAutoRefresh,
        stopAutoRefresh,
        logout
    }
})
