// src/api.js
import axios from 'axios'

function getCookie(name) {
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if (parts.length === 2) return parts.pop().split(';').shift()
}

const api = axios.create({
    baseURL: '/api',
    withCredentials: true,
})

let isRefreshing = false
let failedQueue = []

function processQueue(error) {
    failedQueue.forEach(p => (error ? p.reject(error) : p.resolve()))
    failedQueue = []
}

async function refreshAuthToken() {
    const csrfToken = getCookie('csrf_refresh_token')
    return api.post('/auth/refresh', null, {
        headers: {
            'X-CSRF-TOKEN': csrfToken
        },
        skipAuthRefresh: true
    })
}

// Перехват 401
api.interceptors.response.use(
    res => res,
    async err => {
        const originalRequest = err.config

        if ((err.response?.status === 401 || err.response?.status === 422) && !originalRequest._retry && !originalRequest.skipAuthRefresh) {

            if (isRefreshing) {
                return new Promise((resolve, reject) => {
                    failedQueue.push({ resolve, reject })
                }).then(() => api(originalRequest))
            }

            originalRequest._retry = true
            isRefreshing = true

            try {
                const csrfToken = getCookie('csrf_refresh_token')
                await api.post('/auth/refresh', null, {
                    headers: {
                        'X-CSRF-TOKEN': csrfToken
                    },
                    skipAuthRefresh: true
                })
                processQueue(null)
                return api(originalRequest)
            } catch (refreshErr) {
                processQueue(refreshErr)
                return Promise.reject(refreshErr)
            } finally {
                isRefreshing = false
            }
        }

        return Promise.reject(err)
    }
)

export default api
export { refreshAuthToken }
