<template>
  <button class="btn btn-ghost flex items-center" @click="openLoginModal">
    <svg class="w-3 h-3 fill-base-content">
      <use href="#icon_login"></use>
    </svg>
    Вход
  </button>

  <dialog ref="loginModal" id="login_modal" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h3 class="text-lg font-bold mb-4">Вход</h3>

      <div v-if="errorMessage" role="alert" class="alert alert-error alert-soft">
        <span>{{ errorMessage }}</span>
        <button @click="errorMessage = ''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
      </div>

      <div class="modal-action">
        <form method="dialog">
          <button class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
        </form>

        <form class="grid w-full" @submit.prevent="login">
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
              v-model="email"
            />
          </label>

          <div class="validator-hint hidden mt-0">Проверьте правильность ввода адреса электронной почты</div>

          <label class="input validator w-full mt-4">
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
              v-model="password"
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

          <button class="btn btn-primary mt-4">Вход</button>
        </form>
      </div>
    </div>

    <form method="dialog" class="modal-backdrop">
      <button>close</button>
    </form>
  </dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loginModal = ref(null)
const auth = useAuthStore()
const router = useRouter()

const openLoginModal = () => {
  loginModal.value?.showModal()
}

const login = async () => {
  try {
    await api.post(
      '/auth/login',
      {
        email: email.value,
        password: password.value,
      },
      {
        skipAuthRefresh: true,
      }
    )

    errorMessage.value = ''
    await auth.fetchUser()
    router.go()
  } catch (err) {
    if (err.response && err.response.status === 401) {
      errorMessage.value = 'Неверный email или пароль'
    } else {
      errorMessage.value = 'Сетевая ошибка. Попробуйте позже.'
    }
  }
}
</script>
