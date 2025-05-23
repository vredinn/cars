<template>
  <div>
    <HeroSection />

    <!-- Секция с брендами -->
    <section class="py-12 container mx-auto px-4 bg-base-100">
      <div class="flex justify-between items-center mb-10">
        <h2 class="text-3xl font-bold">Бренды</h2>
        <button class="font-bold">Показать все бренды</button>
      </div>

      <!-- Пока грузится -->
      <div v-if="isLoadingBrands" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-6">
        <div v-for="n in 6" :key="n" class="flex flex-col items-center animate-pulse">
          <div class="w-full aspect-square rounded-full bg-gray-300"></div>
        </div>
      </div>

      <!-- Когда загрузилось -->
      <div v-else class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-6">
        <div v-for="brand in brands" :key="brand.id" class="flex flex-col items-center">
          <div
            class="w-full aspect-square rounded-full bg-white flex flex-col items-center justify-center p-4 hover:shadow-lg transition-all shadow-md">
            <img :src="`${brand.image_url}`" :alt="brand.name" class="w-1/2 h-auto mb-2">
            <span class="text-sm font-medium text-center text-black">{{ brand.name }}</span>
          </div>
        </div>
      </div>

    </section>

    <!-- Популярные объявления -->
    <section class="container mx-auto px-4 bg-base-100 relative">
      <h2 class="text-3xl font-bold text-center mb-10">Популярные объявления</h2>

      <div ref="carousel" class="carousel w-full rounded-box space-x-4 p-4 scroll-p-4 bg-base-200">

        <router-link v-for="(car, uuid) in popularCars" :key="uuid" :to="`/car/${car.uuid}`"
          class="card carousel-item btn btn-soft p-0 h-100 w-70 transition-all duration-250">
          <figure class="w-full max-h-[200px] ">
            <img :src="car.preview_image_url" :alt="car.title" class="object-cover w-full h-full">
          </figure>
          <div class="card-body p-4 text-base-content">
            <h3 class="card-title text-lg">{{ car.brand_name }} {{ car.model_name }}</h3>
            <p class="text-sm">{{ car.specs }}</p>
            <div class="flex flex-wrap gap-2 my-2">
              
              <div class="badge badge-outline border-gray-300 ">{{ car.car_condition }}</div>
              <div class="badge badge-outline border-gray-300 ">{{ car.mileage }}</div>
              <div class="badge badge-outline border-gray-300 ">{{ car.fuel_type }}</div>
              <div class="badge badge-outline border-gray-300 ">{{ car.transmission }}</div>
              <div class="badge badge-outline border-gray-300 ">{{ car.engine_power }} л.с.</div>
            </div>
            <div class="card-actions justify-between items-center mt-auto">
              <span class="text-xl font-bold">{{ formatPrice(car.price) }}</span>
              <router-link 
                :to="`/car/${car.uuid}`" 
                class="btn btn-sm btn-primary"
                v-if="!isLoadingCars"
              >
                Подробнее
              </router-link>
            </div>
          </div>
        </router-link>
        <router-link to="/catalog" class="btn btn-soft carousel-item h-100 w-70 p-0 text-xl">
          Посмотреть все объявления
        </router-link>
      </div>

      <!-- Навигационные кнопки -->
      <div class="flex justify-center gap-6 mt-4">
        <button @click="prevSlide" :class="{ 'btn-disabled': !canScrollLeft}"
          class="btn btn-neutral btn-circle w-[60px] h-[40px] min-h-[40px]">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M15 18l-6-6 6-6" />
          </svg>
        </button>
        <button @click="nextSlide" :class="{ 'btn-disabled': !canScrollRight}"
          class="btn btn-neutral btn-circle w-[60px] h-[40px] min-h-[40px]">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18l6-6-6-6" />
          </svg>
        </button>
      </div>
    </section>

    <!-- Новая секция "Получите справедливую цену" -->
    <section class="py-20 container mx-auto px-4 bg-base-100">
      <!-- Верхняя часть: изображение и текст -->
      <div class="flex flex-col lg:flex-row mb-16  ">
        <!-- Изображение машины (левая часть) -->
        <div class="lg:w-1/2 shadow-md rounded-none">
          <img src="/src/assets/cars/Background.jpg" alt="Продажа автомобиля"
            class="w-full h-full rounded-t-[24px] lg:rounded-none lg:rounded-l-[24px]">
        </div>

        <!-- Текст (правая часть) -->
        <div class="lg:w-1/2 flex flex-col justify-center bg-base-300 rounded-b-[24px] lg:rounded-none lg:rounded-r-[24px] p-4">
          <h2 class="text-3xl font-bold mb-4">ПОЛУЧИТЕ СПРАВЕДЛИВУЮ ЦЕНУ ЗА СВОЙ АВТОМОБИЛЬ</h2>
          <h3 class="text-2xl mb-6 font-semibold">Продайте его сегодня</h3>

          <p class="mb-8">Мы стремимся предоставлять нашим клиентам исключительный сервис,
            конкурентоспособные цены и широкий ассортимент</p>

          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="">Бесплатная оценка автомобиля онлайн за 5 минут</span>
            </li>
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="">Продажа авто в любом состоянии — даже после аварии</span>
            </li>
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="">Удобное общение с покупателями</span>
            </li>
          </ul>

          <button class="btn btn-primary px-8 py-3 text-lg w-fit mx-auto">Начать</button>
        </div>
      </div>

      <!-- Нижняя часть: статистика -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 bg-base-100">
        <!-- Блоки статистики -->
        <div class=" p-6 rounded-lg text-center font-bold">
          <div class="text-4xl font-bold mb-2">836M</div>
          <div class=" uppercase text-sm">Автомобилей в продаже</div>
        </div>
        <div class=" p-6 rounded-lg text-center">
          <div class="text-4xl font-bold mb-2 ">738M</div>
          <div class=" uppercase text-sm">Отзывов о дилерах</div>
        </div>
        <div class=" p-6 rounded-lg text-center">
          <div class="text-4xl font-bold mb-2 ">238M</div>
          <div class=" uppercase text-sm">Проверенных дилеров</div>
        </div>
        <div class=" p-6 rounded-lg text-center ">
          <div class="text-4xl font-bold mb-2 ">100M</div>
          <div class=" uppercase text-sm">Посетителей в день</div>
        </div>
      </div>
    </section>
    <section class="py-20 container mx-auto px-4">
    <h2 class="text-3xl font-bold text-center mb-10">Популярные продавцы</h2>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <!-- Карточки продавца -->
      <div v-for="(user, uuid) in popularUsers" :key="uuid" class="card bg-base-300 shadow-md h-[400px] w-full mx-auto">
        <figure class="h-[306px] overflow-hidden">
          <img :src="user.avatar_url || '/uploads/user_example.webp'" :alt="user.name"
            class="w-full h-full object-cover"
          >
        </figure>
        <div class="card-body p-4">
          <h3 class="card-title text-lg">{{ user.name }}</h3>
          <p class="text-sm">На сайте с {{ formatDate(user.registration_date) }}</p>
          
          <div class="text-sm text-center">Рейтинг: {{ user.rating.toFixed(2) }}</div>
          <div class="rating rating-sm rating-half justify-center mb-2">
            <template v-for="i in 10" :key="i">
              <input
                type="radio"
                :name="'rating-' + user.uuid"
                class="mask mask-star-2"
                :class="i % 2 === 1 ? 'mask-half-1 bg-orange-400' : 'mask-half-2 bg-orange-400'"
                :checked="i === Math.round(user.rating * 2)"
                disabled
              />
            </template>
          </div>
          <router-link :to="'/user/' + user.uuid" class="btn btn-outline btn-sm mt-2">Подробнее</router-link>
        </div>
      </div>
    </div>
  </section>
  </div>
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import HeroSection from '@/components/HeroSection.vue'
import api from '@/api'

// Состояния
const brands = ref([])
const isLoadingBrands = ref(true)

const popularCars = ref([])
const popularUsers = ref([])

const isLoadingCars = ref(true)
const isLoadingUsers = ref(true)

const canScrollLeft = ref(false)
const canScrollRight = ref(true)

const carousel = ref(null)

// Методы

async function loadBrands() {
  isLoadingBrands.value = true
  try {
    const { data } = await api.get('/brands/')
    brands.value = data
  } catch (error) {
    console.error('Ошибка загрузки брендов:', error)
  } finally {
    isLoadingBrands.value = false
  }
}

async function loadPopularUsers() {
  isLoadingUsers.value = true
  try {
    const { data } = await api.get('/users_popular')
    popularUsers.value = data
  } catch (error) {
    console.error('Ошибка загрузки популярных пользователей:', error)
  } finally {
    isLoadingUsers.value = false
  }
}

async function loadPopularCars() {
  isLoadingCars.value = true
  try {
    const { data } = await api.get('/cars/popular')
    popularCars.value = data
  } catch (error) {
    console.error('Ошибка загрузки популярных машин:', error)
  } finally {
    isLoadingCars.value = false
    await nextTick()
    if (carousel.value) {
      carousel.value.scrollLeft = 0
      updateScrollButtons()
    }
  }
}

function updateScrollButtons() {
  if (!carousel.value) return
  const el = carousel.value
  canScrollLeft.value = el.scrollLeft > 0
  canScrollRight.value = Math.ceil(el.scrollLeft) <
    Math.floor(el.scrollWidth - el.clientWidth)
}

function nextSlide() {
  if (!carousel.value) return
  carousel.value.scrollBy({ left: 320, behavior: 'smooth' })
  setTimeout(updateScrollButtons, 500)
}

function prevSlide() {
  if (!carousel.value) return
  carousel.value.scrollBy({ left: -320, behavior: 'smooth' })
  setTimeout(updateScrollButtons, 500)
}

function formatPrice(price) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(price)
}

function formatDate(dateString) {
  if (!dateString) return 'Дата не указана'

  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'Некорректная дата'

    return new Intl.DateTimeFormat('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    }).format(date)
  } catch (e) {
    console.error('Ошибка форматирования даты:', e)
    return dateString
  }
}

// Хуки
onMounted(() => {
  loadBrands()
  loadPopularCars()
  loadPopularUsers()

  if (carousel.value) {
    carousel.value.scrollLeft = 0
    carousel.value.addEventListener('scroll', updateScrollButtons)
  }
})

onBeforeUnmount(() => {
  if (carousel.value) {
    carousel.value.removeEventListener('scroll', updateScrollButtons)
  }
})
</script>