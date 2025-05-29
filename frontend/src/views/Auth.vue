<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-md mx-auto">
      <div class="tabs tabs-border mb-6 transition-all duration-300">
        <button 
          class="tab flex-1  transition-all duration-300" 
          :class="{ 'tab-active': activeTab === 'login' }"
          @click="activeTab = 'login'"
        >
          Вход
        </button>
        <button 
          class="tab flex-1  transition-all duration-300" 
          :class="{ 'tab-active': activeTab === 'register' }"
          @click="activeTab = 'register'"
        >
          Регистрация
        </button>
      </div>

      <div v-if="errorMessage" role="alert" class="alert alert-error mb-4">
        <span>{{ errorMessage }}</span>
        <button @click="errorMessage = ''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
      </div>

      <!-- Форма входа -->
      <form v-if="activeTab === 'login'" @submit.prevent="login" class="space-y-4">
        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <rect width="20" height="16" x="2" y="4" rx="2"></rect>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
            </g>
          </svg>
          <input
            type="email"
            placeholder="Email адрес"
            required
            pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
            v-model="loginForm.email"
          />
        </label>
        <div class="validator-hint hidden mt-0">Проверьте правильность ввода адреса электронной почты</div>

        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <path
                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
              ></path>
              <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
            </g>
          </svg>
          <input
            type="password"
            required
            placeholder="Пароль"
            minlength="8"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            title="Пароль не может быть короче 8 символов, должен включать цифры, заглавные и строчные буквы"
            v-model="loginForm.password"
          />
        </label>
        <p class="validator-hint hidden mt-0">
          Пароль должен быть минимум 8 символов в длину
          <br />
          Должен содержать:
          <br />
          Хотя бы одну цифру <br />
          Хотя бы одну строчную букву <br />
          Хотя бы одну заглавную букву
        </p>

        <button type="submit" class="btn btn-primary w-full">Войти</button>
      </form>

      <!-- Форма регистрации -->
      <form v-else @submit.prevent="register" class="space-y-4">
        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <circle cx="12" cy="8" r="5"></circle>
              <path d="M20 21a8 8 0 1 0-16 0"></path>
            </g>
          </svg>
          <input
            type="text"
            placeholder="Имя"
            required
            minlength="2"
            maxlength="50"
            pattern="[A-Za-zА-Яа-яЁё\s-]+"
            v-model="registerForm.name"
          />
        </label>
        <div class="validator-hint hidden mt-0">Имя может содержать только буквы, пробелы и дефис</div>

        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <rect width="20" height="16" x="2" y="4" rx="2"></rect>
              <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"></path>
            </g>
          </svg>
          <input
            type="email"
            placeholder="Email адрес"
            required
            pattern="[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"
            v-model="registerForm.email"
          />
        </label>
        <div class="validator-hint hidden mt-0">Проверьте правильность ввода адреса электронной почты</div>

        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"></path>
            </g>
          </svg>
          <input
            type="tel"
            placeholder="Телефон"
            required
            pattern="^\+?[0-9]{10,15}$"
            v-model="registerForm.phone"
          />
        </label>
        <div class="validator-hint hidden mt-0">Введите корректный номер телефона</div>

        <label class="input validator w-full">
          <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <g
              stroke-linejoin="round"
              stroke-linecap="round"
              stroke-width="2.5"
              fill="none"
              stroke="currentColor"
            >
              <path
                d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z"
              ></path>
              <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
            </g>
          </svg>
          <input
            type="password"
            required
            placeholder="Пароль"
            minlength="8"
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            title="Пароль не может быть короче 8 символов, должен включать цифры, заглавные и строчные буквы"
            v-model="registerForm.password"
          />
        </label>
        <p class="validator-hint hidden mt-0">
          Пароль должен быть минимум 8 символов в длину
          <br />
          Должен содержать:
          <br />
          Хотя бы одну цифру <br />
          Хотя бы одну строчную букву <br />
          Хотя бы одну заглавную букву
        </p>

        <button type="submit" class="btn btn-primary w-full">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const activeTab = ref('login')
const errorMessage = ref('')

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  name: '',
  email: '',
  phone: '',
  password: ''
})

const login = async () => {
  try {
    await api.post('/auth/login', loginForm.value)
    await auth.fetchUser()
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Ошибка при входе'
  }
}

const register = async () => {
  try {
    await api.post('/auth/register', registerForm.value)
    await auth.fetchUser()
    const redirectPath = route.query.redirect || '/'
    router.push(redirectPath)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Ошибка при регистрации'
  }
}
</script>