import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import { createYmaps } from 'vue-yandex-maps'
import './style.css' // Подключение глобальных стилей

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.use(createYmaps({
    apikey: '249a7a27-d3cf-46ac-8920-d1f2c656a79b',
}));
app.mount('#app')