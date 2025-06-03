<template>
  <div class="container mx-auto p-4">
    <div v-if="isUserLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <div class="mb-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="flex flex-col md:flex-row items-start gap-4">
            <div class="avatar">
              <div class="h-54 w-full rounded-box">
                <img 
                  :src="user.avatar_url || '/uploads/user_example.webp'" 
                  alt="avatar" 
                  class="w-full h-full object-cover"
                />
              </div>
            </div>
            <div class="flex-1">
              <h1 class="text-2xl font-bold mb-4">{{ user.name }}</h1>
              <p>Email: {{ user.email }}</p>
              <p>Телефон: {{ user.phone }}</p>
              <p>Регистрация: {{ formatDate(user.registration_date) }}</p>
              <div v-if="isOwnProfile" class="mt-4">
                <router-link :to="`/profile/edit/${user.uuid}`" class="btn btn-primary">
                  Редактировать профиль
                </router-link>
              </div>
            </div>
          </div>

          <div v-if="user?.uuid" class="bg-base-100 rounded-box">
            <UserReviews 
              :reviews="reviews"
              :isLoading="isReviewsLoading"
              :totalReviews="reviewsTotalCount"
            />

          </div>
        </div>
      </div>
    </div>

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

    <div v-if="isOwnProfile && activeTab === 'ads'" class="flex justify-center">
      <router-link to="/create_car" class="btn btn-primary">
        Создать объявление
      </router-link>
    </div>

    <div v-if="!isOwnProfile || (isOwnProfile && activeTab === 'ads')" class="mb-4">
      <h3 v-if="!isOwnProfile" class="text-xl font-bold">Объявления пользователя</h3>
      <div v-if="hasAnyCars" class="tabs tabs-border justify-center">
        <a 
          v-if="hasActiveCars"
          class="tab" 
          :class="{ 'tab-active': carsTab === 'active' }"
          @click="setCarsTab('active')"
        >
          Активные
        </a>
        <a 
          v-if="hasSoldCars"
          class="tab" 
          :class="{ 'tab-active': carsTab === 'sold' }"
          @click="setCarsTab('sold')"
        >
          Проданные
        </a>
      </div>
    </div>

    <div v-if="isCarsLoading || isFavoritesLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      <div v-if="displayedCars.length > 0" class="grid grid-cols-1 gap-4">
        <CarCard v-for="car in displayedCars" :key="car.uuid" :car="car" />
      </div>
      <div v-else class="text-center py-8">
        <p class="text-lg">{{ noItemsMessage }}</p>
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
import UserReviews from '@/components/UserReviews.vue'
import api from '@/api'

const route = useRoute()
const authStore = useAuthStore()

const user = ref(null)
const isUserLoading = ref(true)
const reviews = ref([])
const isReviewsLoading = ref(true)
const reviewsTotalCount = ref(0)

const cars = ref([])
const favorites = ref([])
const isCarsLoading = ref(true)
const isFavoritesLoading = ref(false)

const carsPage = ref(1)
const carsTotalPages = ref(1)
const favoritesPage = ref(1)
const favoritesTotalPages = ref(1)

const activeTab = ref('favorites')
const carsTab = ref('active')
const activeCars = ref([])
const soldCars = ref([])

const isOwnProfile = computed(() => {
  return authStore.user && user.value && authStore.user.uuid === user.value.uuid
})

const hasActiveCars = computed(() => {
  return activeCars.value.length > 0
})

const hasSoldCars = computed(() => {
  return soldCars.value.length > 0
})

const hasAnyCars = computed(() => {
  return hasActiveCars.value || hasSoldCars.value
})

const displayedCars = computed(() => {
  if (!isOwnProfile.value && carsTab.value === 'active') {
      return activeCars.value
  } else if (!isOwnProfile.value && carsTab.value === 'sold') {
    return soldCars.value
  }

  if (activeTab.value === 'favorites') {
    return favorites.value.map(favorite => favorite.car)
  } else {
    return carsTab.value === 'active' ? activeCars.value : soldCars.value
  }
})

const noItemsMessage = computed(() => {
  if (!isOwnProfile.value) {
    return carsTab.value === 'active'
      ? 'У пользователя нет активных объявлений.'
      : 'У пользователя нет проданных объявлений.'
  }
  if (activeTab.value === 'favorites') {
    return 'В избранном пока нет объявлений.'
  }
  return carsTab.value === 'active'
    ? 'У вас пока нет активных объявлений.'
    : 'У вас пока нет проданных объявлений.'
})

const currentPage = computed(() => {
  return activeTab.value === 'favorites' ? favoritesPage.value : carsPage.value
})

const totalPages = computed(() => {
  return activeTab.value === 'favorites' ? favoritesTotalPages.value : carsTotalPages.value
})

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('ru-RU', options)
}

function setActiveTab(tab) {
  activeTab.value = tab
  if (tab === 'favorites') {
    favoritesPage.value = 1
    fetchFavorites(1)
  } else {
    carsPage.value = 1
    fetchCars(1)
  }
}

async function fetchReviews() {
  isReviewsLoading.value = true
  try {
    const { data } = await api.get(`/reviews/seller/${user.value.uuid}`)
    reviews.value = data
    reviewsTotalCount.value = data.length
  } catch (error) {
    console.error('Ошибка загрузки отзывов:', error)
    reviews.value = []
    reviewsTotalCount.value = 0
  } finally {
    isReviewsLoading.value = false
  }
}

async function fetchUserProfile() {
  isUserLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/users/${uuid}`)
    user.value = data
    
    await fetchReviews()
    
    if (isOwnProfile.value) {
      fetchFavorites(1)
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля пользователя:', error)
  } finally {
    isUserLoading.value = false
  }
}

async function fetchCars(page = 1) {
  isCarsLoading.value = true
  try {
    const uuid = route.params.uuid
    const { data } = await api.get(`/cars/user_cars/${uuid}?page=${page}`)
    activeCars.value = data.items.filter(car => !car.is_sold)
    soldCars.value = data.items.filter(car => car.is_sold)
    
    if (carsTab.value === 'active' && !hasActiveCars.value && hasSoldCars.value) {
      carsTab.value = 'sold'
    } else if (carsTab.value === 'sold' && !hasSoldCars.value && hasActiveCars.value) {
      carsTab.value = 'active'
    }
    
    carsTotalPages.value = data.pages
    carsPage.value = data.page
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
  } finally {
    isCarsLoading.value = false
  }
}

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

function setCarsTab(tab) {
  carsTab.value = tab
  carsPage.value = 1
  fetchCars(1)
}

onMounted(() => {
  fetchUserProfile()
  fetchCars()
})

watch(() => route.params.uuid, () => {
  activeTab.value = 'favorites'
  fetchUserProfile()
  fetchCars()
})
</script>
