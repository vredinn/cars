import axios from 'axios'

function getCookie(name) {
    if (typeof document === 'undefined' || !document.cookie) return null
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'))
    return match ? match[2] : null
}

const api = axios.create({
    baseURL: '/api',
    withCredentials: true,
})

const REFRESH_INTERVAL = 14 * 60 * 1000 // 14 минут
let lastRefresh = 0
let refreshingPromise = null

async function maybeRefreshToken() {
    const now = Date.now()
    if (now - lastRefresh > REFRESH_INTERVAL) {
        if (!refreshingPromise) {
            const csrfToken = getCookie('csrf_refresh_token')
            refreshingPromise = api.post('/auth/refresh', null, {
                headers: { 'X-CSRF-TOKEN': csrfToken },
                withCredentials: true,
                skipAuthRefresh: true,
            })
                .then(() => {
                    lastRefresh = Date.now()
                    console.log('[Auth] Token refreshed')
                })
                .catch(err => {
                    console.warn('[Auth] Token refresh failed', err)
                    throw err
                })
                .finally(() => {
                    refreshingPromise = null
                })
        }
        return refreshingPromise
    }
    return Promise.resolve()
}

let isRefreshing = false
let failedQueue = []

function processQueue(error) {
    failedQueue.forEach(({ resolve, reject }) => (error ? reject(error) : resolve()))
    failedQueue = []
}

async function refreshAuthToken() {
    const csrfToken = getCookie('csrf_refresh_token')
    return api.post('/auth/refresh', null, {
        headers: { 'X-CSRF-TOKEN': csrfToken },
        withCredentials: true,
        skipAuthRefresh: true,
    })
}

api.interceptors.request.use(
    async config => {
        if (!config.skipAuthRefresh) {
            try {
                await maybeRefreshToken()
            } catch {
                // игнорируем ошибку, чтобы запрос всё равно пошёл
            }
        }

        const method = config.method?.toLowerCase()
        const needsCSRF = ['post', 'put', 'delete', 'patch'].includes(method)
        const csrfAccessToken = getCookie('csrf_access_token')

        if (csrfAccessToken && needsCSRF && !config.headers['X-CSRF-TOKEN']) {
            config.headers['X-CSRF-TOKEN'] = csrfAccessToken
        }

        return config
    },
    error => Promise.reject(error)
)

api.interceptors.response.use(
    res => res,
    async err => {
        const originalRequest = err.config
        if (!originalRequest) return Promise.reject(err)

        if (
            (err.response?.status === 401 || err.response?.status === 422) &&
            !originalRequest._retry &&
            !originalRequest.skipAuthRefresh
        ) {
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
                    headers: { 'X-CSRF-TOKEN': csrfToken },
                    withCredentials: true,
                    skipAuthRefresh: true,
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
export { refreshAuthToken, getCookie }
