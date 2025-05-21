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

    <h3 class="text-xl font-bold mb-4">Объявления пользователя</h3>

    <div v-if="isCarsLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <div v-if="cars.length > 0" class="grid grid-cols-1 gap-4">
        <CarCard v-for="car in cars" :key="car.uuid" :car="car" />
      </div>
      <div v-else class="text-center py-8">
        <p class="text-lg">Пользователь пока не опубликовал ни одного объявления.</p>
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
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
import api from '@/api'

// Маршрут
const route = useRoute()

// Состояния
const user = ref(null)
const isUserLoading = ref(true)

const cars = ref([])
const isCarsLoading = ref(true)

const currentPage = ref(1)
const totalPages = ref(1)

// Форматирование даты
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}

// Получение профиля пользователя
async function fetchUserProfile() {
  isUserLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/users/${uuid}`)
    user.value = data
  } catch (error) {
    console.error('Ошибка загрузки профиля пользователя:', error)
  } finally {
    isUserLoading.value = false
  }
}

// Получение автомобилей пользователя
async function fetchCars(page = 1) {
  isCarsLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/cars/user_cars/${uuid}?page=${page}`)
    cars.value = data.items
    totalPages.value = data.pages
    currentPage.value = data.page
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
  } finally {
    isCarsLoading.value = false
  }
}

// Смена страницы
function changePage(page) {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  currentPage.value = page
  fetchCars(page)
}

// Загрузка данных при монтировании
onMounted(() => {
  fetchUserProfile()
  fetchCars()
})

// Отслеживание изменения маршрута
watch(() => route.params.uuid, () => {
  fetchUserProfile()
  fetchCars()
})
</script>
