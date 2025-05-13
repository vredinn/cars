<template>
  <div class="container mx-auto p-4">

    <div v-if="isUserLoading" class="flex justify-center my-8">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <div v-else>
      
      <h1 class="text-2xl font-bold mb-4">{{ user.name }}</h1>
      <div class="mb-4">
        <div class="flex flex-col md:flex-row items-center gap-4">
          <div class="avatar">
              <div class="h-54 w-full rounded-box">
                <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar"/>
              </div>
            </div>
          <div>
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
        <CarCard 
          v-for="car in cars" 
          :key="car.uuid" 
          :car="car"
        />
      </div>
      <div v-else class="text-center py-8">
        <p class="text-lg">Пользователь пока не опубликовал ни одного объявления.</p>
      </div>
      
              <!-- Пагинация -->
      <Pagination 
        v-if="totalPages > 1"
        :currentPage="currentPage"
        :totalPages="totalPages"
        @page-changed="changePage"
      />
    </div>
  </div>
</template>

<script>
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
import api from '@/api'
export default {
  name: 'UserProfile',
  components: {
    CarCard,
    Pagination
  },
  data() {
    return {
      user: null,
      user: null,
      isUserLoading: true,
      isCarsLoading: true,
      cars: [],
      currentPage: 1,
      totalPages: 1,
    }
  },
  methods: {
    async fetchUserProfile() {
      this.isUserLoading = true
      try {
        const uuid = this.$route.params.uuid
        const response = await api.get(`/users/${uuid}`)
        this.user = response.data
      } catch (error) {
        console.error('Ошибка загрузки профиля пользователя:', error)
      } finally {
        this.isUserLoading = false
      }
    },
    async fetchCars(page = 1) {
      this.isCarsLoading = true
      try {
        const uuid = this.$route.params.uuid
        const response = await api.get(`/cars/user_cars/${uuid}?page=${page}`)
        this.cars = response.data.items        
        this.totalPages = response.data.pages
        this.currentPage = response.data.page
      } catch (error) {
        console.error('Ошибка загрузки автомобилей:', error)
      }      
      this.isCarsLoading = false
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(dateString).toLocaleDateString('ru-RU', options)
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages || page === this.currentPage) return
      
      this.currentPage = page
      this.fetchCars(page)
    },
  },
  created() {
    this.fetchUserProfile()
    this.fetchCars()
  }
}
</script>