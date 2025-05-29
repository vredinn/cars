<template>
  <header class="container mx-auto navbar w-full px-4 py-0">
    <!-- Мобильное меню -->
    <div class="dropdown" ref="mobileMenuRef">
      <input type="checkbox" v-model="isMobileMenuOpen" class="hidden" />
      <label tabindex="0" class="btn btn-ghost mr-2 lg:hidden" @click="toggleMobileMenu">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
        </svg>
      </label>
      <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-200 rounded-box z-10 mt-3 w-64 p-2 shadow gap-2" :class="{ 'hidden': !isMobileMenuOpen }">
        <li><router-link to="/" class="btn btn-ghost" active-class="btn btn-outline" @click="closeMobileMenu">Главная</router-link></li>
        <li><router-link to="/catalog" class="btn btn-ghost" active-class="btn btn-outline" @click="closeMobileMenu">Поиск</router-link></li>
      </ul>
    </div>

    <!-- Логотип -->
    <router-link to="/" class="flex-1">
      <div class="h-8">
        <img src="/src/assets/logo_White.svg" alt="Logo" class="h-full dark:block hidden" />
        <img src="/src/assets/logo_Black.svg" alt="Logo" class="h-full block dark:hidden" />
      </div>
    </router-link>

    <!-- Основное меню -->
    <nav class="flex-none hidden lg:flex">
      <ul class="menu menu-horizontal space-x-2">
        <li><router-link to="/" class="btn btn-ghost" active-class="btn btn-outline">Главная</router-link></li>
        <li><router-link to="/catalog" class="btn btn-ghost" active-class="btn btn-outline">Поиск</router-link></li>
      </ul>
    </nav>

    <!-- Аутентификация / Меню -->
    <div class="flex space-x-2">
      <template v-if="!isAuthenticated">
        <LoginForm />
      </template>

      <template v-else>
        <router-link to="/chats" class="btn btn-primary hidden md:inline-flex">Сообщения</router-link>

        <!-- Профиль -->
        <div class="dropdown dropdown-end" ref="profileMenuRef">
          <input type="checkbox" v-model="isProfileMenuOpen" class="hidden" />
          <label tabindex="0" class="btn btn-ghost btn-circle avatar" @click="toggleProfileMenu">
            <div class="w-10 rounded-full">
              <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar" />
            </div>
          </label>
          <ul tabindex="0" class="menu dropdown-content z-[1] mt-3 w-64 rounded-box bg-base-200 p-2 shadow gap-2" :class="{ 'hidden': !isProfileMenuOpen }">
            <div class="flex flex-col gap-2">
              <div class="avatar">
                <div class="h-36 w-full rounded-box">
                  <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar" />
                </div>
              </div>
              <div class="text-center text-pretty">{{ user.name }} <br /> {{ user.email }}</div>
            </div>
            <li><router-link to="/chats" class="btn btn-primary md:hidden" @click="closeProfileMenu">Сообщения</router-link></li>
            <li><router-link to="/create_car" class="btn btn-primary" @click="closeProfileMenu">Создать объявление</router-link></li>
            <li><router-link :to="`/user/${user.uuid}`" class="btn btn-outline" @click="closeProfileMenu">Профиль</router-link></li>
            <li><label for="logout-modal" class="btn btn-soft btn-error" @click="closeProfileMenu">Выйти</label></li>
          </ul>

          <!-- Модалка подтверждения -->
          <input type="checkbox" id="logout-modal" class="modal-toggle" v-model="showLogoutModal" />
          <div class="modal modal-bottom sm:modal-middle">
            <div class="modal-box">
              <h3 class="font-bold text-lg">Выход</h3>
              <p class="py-4">Вы уверены, что хотите выйти?</p>
              <div class="modal-action">
                <label for="logout-modal" class="btn btn-primary">Отмена</label>
                <button @click="confirmLogout" class="btn btn-soft btn-error">Выйти</button>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'
import LoginForm from '@/components/LoginForm.vue'

const showLogoutModal = ref(false)
const isMobileMenuOpen = ref(false)
const isProfileMenuOpen = ref(false)
const mobileMenuRef = ref(null)
const profileMenuRef = ref(null)

const route = useRoute()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const isAuthenticated = computed(() => authStore.isAuthenticated)

// Закрываем меню при изменении маршрута
watch(() => route.fullPath, () => {
  isMobileMenuOpen.value = false
  isProfileMenuOpen.value = false
})

function toggleMobileMenu() {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
  if (isMobileMenuOpen.value) {
    isProfileMenuOpen.value = false
  }
}

function toggleProfileMenu() {
  isProfileMenuOpen.value = !isProfileMenuOpen.value
  if (isProfileMenuOpen.value) {
    isMobileMenuOpen.value = false
  }
}

function closeMobileMenu() {
  isMobileMenuOpen.value = false
}

function closeProfileMenu() {
  isProfileMenuOpen.value = false
}

// Закрытие меню при клике вне его области
function handleClickOutside(event) {
  if (mobileMenuRef.value && !mobileMenuRef.value.contains(event.target)) {
    isMobileMenuOpen.value = false
  }
  if (profileMenuRef.value && !profileMenuRef.value.contains(event.target)) {
    isProfileMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const confirmLogout = () => {
  showLogoutModal.value = false
  authStore.logout()
}
</script>
