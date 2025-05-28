<template>
  <div class="container mx-auto p-4">
    <div v-if="isUserLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <div class="mb-4">
        <div class="flex flex-col md:flex-row items-center gap-4">
          <div class="avatar">
            <div class="h-54 w-full rounded-box">
              <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar" />
            </div>
          </div>
          <div>
            <h1 class="text-2xl font-bold mb-4">{{ user.name }}</h1>
            <p>Email: {{ user.email }}</p>
            <p>Телефон: {{ user.phone }}</p>
            <p>Рейтинг: {{ user.rating.toFixed(2) }}</p>
            <p>Регистрация: {{ formatDate(user.registration_date) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Tabs only for own profile -->
    <div v-if="isOwnProfile" class="tabs tabs-border mb-4 justify-center">
      <a 
        class="tab" 
        :class="{ 'tab-active': activeTab === 'favorites' }"
        @click="setActiveTab('favorites')"
      >
        Избранное
      </a>
      <a 
        class="tab" 
        :class="{ 'tab-active': activeTab === 'ads' }"
        @click="setActiveTab('ads')"
      >
        Мои объявления
      </a>
    </div>
    <h3 v-else class="text-xl font-bold mb-4">Объявления пользователя</h3>

    <div v-if="isCarsLoading || isFavoritesLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <div v-if="displayedCars.length > 0" class="grid grid-cols-1 gap-4">
        <!-- Кнопка создания объявления в разделе "Мои объявления" -->
        <div v-if="isOwnProfile && activeTab === 'ads'" class="flex justify-center">
          <router-link to="/create_car" class="btn btn-primary">
            Создать объявление
          </router-link>
        </div>
        <CarCard v-for="car in displayedCars" :key="car.uuid" :car="car" />
      </div>
      <div v-else class="text-center py-8">
        <p class="text-lg">{{ noItemsMessage }}</p>
        <!-- Кнопка создания объявления, если нет объявлений -->
        <div v-if="isOwnProfile && activeTab === 'ads'" class="mt-4">
          <router-link to="/create_car" class="btn btn-primary">
            Создать объявление
          </router-link>
        </div>
      </div>

      <Pagination
        v-if="totalPages > 1"
        :currentPage="currentPage"
        :totalPages="totalPages"
        @page-changed="changePage"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
import api from '@/api'

// Маршрут и авторизация
const route = useRoute()
const authStore = useAuthStore()

// Состояния
const user = ref(null)
const isUserLoading = ref(true)

const cars = ref([])
const favorites = ref([])
const isCarsLoading = ref(true)
const isFavoritesLoading = ref(false)

// Отдельная пагинация для каждого типа
const carsPage = ref(1)
const carsTotalPages = ref(1)
const favoritesPage = ref(1)
const favoritesTotalPages = ref(1)

const activeTab = ref('favorites')

// Вычисляемые свойства
const isOwnProfile = computed(() => {
  return authStore.user && user.value && authStore.user.uuid === user.value.uuid
})

const displayedCars = computed(() => {
  if (!isOwnProfile.value) return cars.value
  // Extract car objects from favorites and ensure they have brand and model names
  if (activeTab.value === 'favorites') {
    return favorites.value.map(favorite => {
      const car = favorite.car
      return {
        ...car,
        brand_name: car.brand_name || 'Неизвестно',
        model_name: car.model_name || 'Неизвестно'
      }
    })
  }
  return cars.value
})

const noItemsMessage = computed(() => {
  if (!isOwnProfile.value) {
    return 'Пользователь пока не опубликовал ни одного объявления.'
  }
  return activeTab.value === 'favorites' 
    ? 'В избранном пока нет объявлений.' 
    : 'У вас пока нет опубликованных объявлений.'
})

// Вычисляемые свойства для пагинации
const currentPage = computed(() => {
  return activeTab.value === 'favorites' ? favoritesPage.value : carsPage.value
})

const totalPages = computed(() => {
  return activeTab.value === 'favorites' ? favoritesTotalPages.value : carsTotalPages.value
})

// Форматирование даты
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}

// Установка активной вкладки
function setActiveTab(tab) {
  activeTab.value = tab
  // При смене вкладки загружаем данные с первой страницы
  if (tab === 'favorites') {
    favoritesPage.value = 1
    fetchFavorites(1)
  } else {
    carsPage.value = 1
    fetchCars(1)
  }
}

// Получение профиля пользователя
async function fetchUserProfile() {
  isUserLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/users/${uuid}`)
    user.value = data
    
    // Если это собственный профиль, загружаем избранное
    if (isOwnProfile.value) {
      fetchFavorites()
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля пользователя:', error)
  } finally {
    isUserLoading.value = false
  }
}

// Получение избранных объявлений
async function fetchFavorites(page = 1) {
  if (!isOwnProfile.value) return
  
  isFavoritesLoading.value = true
  try {
    const { data } = await api.get(`/favorites/user_paginated/${user.value.uuid}?page=${page}`)
    favorites.value = data.items.map(favorite => {
      return {
        ...favorite,
        car: {
          ...favorite.car,
          brand_name: favorite.car.brand_name || 'Неизвестно',
          model_name: favorite.car.model_name || 'Неизвестно'
        }
      }
    })
    favoritesTotalPages.value = data.pages
    favoritesPage.value = data.page
  } catch (error) {
    console.error('Ошибка загрузки избранного:', error)
    favorites.value = []
  } finally {
    isFavoritesLoading.value = false
  }
}

// Получение автомобилей пользователя
async function fetchCars(page = 1) {
  isCarsLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/cars/user_cars/${uuid}?page=${page}`)
    cars.value = data.items
    carsTotalPages.value = data.pages
    carsPage.value = data.page
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
  } finally {
    isCarsLoading.value = false
  }
}

// Смена страницы
function changePage(page) {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return

  if (isOwnProfile.value && activeTab.value === 'favorites') {
    favoritesPage.value = page
    fetchFavorites(page)
  } else {
    carsPage.value = page
    fetchCars(page)
  }
}

// Загрузка данных при монтировании
onMounted(() => {
  fetchUserProfile()
  fetchCars()
})

// Отслеживание изменения маршрута
watch(() => route.params.uuid, () => {
  activeTab.value = 'favorites'
  fetchUserProfile()
  fetchCars()
})
</script>
