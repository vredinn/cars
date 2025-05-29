import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './style.css' // Подключение глобальных стилей

// Suppress Suspense warning
const originalWarn = console.warn
console.warn = (...args) => {
    if (args[0] && args[0].includes && args[0].includes('<Suspense> is an experimental feature')) return
    return originalWarn(...args)
}

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')