<template>
  <div class="min-h-screen flex flex-col">
    <div class="flex-grow container mx-auto px-4 py-8">
      <!-- Основное содержимое страницы -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <!-- Галерея изображений -->
        <div>
          <!-- Основное изображение -->
          <div class="w-full rounded-xl overflow-hidden">
            <img 
              :src="currentImage" 
              class="w-full h-96 object-contain cursor-pointer bg-black rounded" 
              alt="Фото автомобиля"
              @click="openModal(currentImage)"
            >
          </div>
          
          <!-- Превью изображений -->
          <div class="flex overflow-x-auto py-2 gap-2">
            <div 
              v-for="(img, index) in car.images" 
              :key="index"
              class="flex-none w-24 h-20"
            >
              <img 
                :src="img.image_url" 
                class="w-full h-full object-cover rounded-xl cursor-pointer transition-all duration-75"
                :class="{'border-2': currentImage === img.image_url}"
                @click="currentImage = img.image_url"
                alt="Превью фото"
              >
            </div>
          </div>
        </div>

        <!-- Информация об автомобиле -->
        <div class="row-span-3">
          <div class="bg-base-200 rounded-xl text-center mb-4 py-4 flex justify-around flex-wrap">
            <h1 class="text-3xl font-bold mb-0">{{ car.brand_name }} {{ car.model_name }}</h1>
            <div class="font-bold text-3xl">{{ formatPrice(car.price) }}</div>
          </div>
          <!-- Характеристики -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Год</div>
              <div class="font-bold">{{ car.year }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Состояние автомобиля</div>
              <div class="font-bold">{{ car.car_condition }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Кузов</div>
              <div class="font-bold">{{ car.body_type }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Цвет</div>
              <div class="font-bold">{{ car.color }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Пробег</div>
              <div class="font-bold">{{ car.mileage.toLocaleString() }} км</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Мощность двигателя</div>
              <div class="font-bold">{{ car.engine_power }} л.с.</div>
            </div>              
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Объем двигателя</div>
              <div class="font-bold">{{ car.engine_capacity }} л</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Коробка</div>
              <div class="font-bold">{{ car.transmission }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Топливо</div>
              <div class="font-bold">{{ car.fuel_type }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Привод</div>
              <div class="font-bold">{{ car.drive_type }}</div>
            </div>
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Руль</div>
              <div class="font-bold">{{ car.steering_side }}</div>
            </div>
            
            <div class="bg-base-200 p-4 rounded-xl">
              <div class="text-gray-500">Дата объявления</div>
              <div class="font-bold">{{ formatListingDate(car.listing_date) }}</div>
            </div>
          </div>
          
          <div class="prose bg-base-200 p-4 rounded-xl mt-4">
            <div class="text-gray-500">Местоположение</div>
            <div class="font-bold">
              <AddressDisplay v-if="car.latitude && car.longitude" :lat="car.latitude" :lng="car.longitude" />
            </div>
          </div>
          <!-- Описание -->
          <div class="prose bg-base-200 p-4 rounded-xl mt-4">
            <div class="text-gray-500">Описание</div>
            <div class="font-bold">{{ car.description }}</div>
          </div>
        </div>
        <!-- Связь с продавцом -->
        <div>          
          <p class="text-lg font-bold mb-4">Продавец:</p>
          <div @click="goToUser(user.uuid)" class="flex flex-col sm:flex-row bg-base-200 rounded-2xl items-center justify-between p-4 cursor-pointer">
            <div class="flex flex-col text-center sm:text-left sm:flex-row items-center gap-4">
              <figure class="w-32 sm:w-16 h-32 sm:h-16">
                <img :src="user.avatar_url || '/uploads/user_example.webp'" :alt="user.name" class="rounded-2xl"/>
              </figure>
              <div>
                <h3 class="font-bold">{{ user.name }}</h3>
                <p>На сайте с {{ formatTraderDate(user.registration_date) }}</p>
              </div> 
            </div>         
            <div class="grid grid-cols-2 w-full sm:w-auto sm:flex items-center gap-2 mt-4 sm:mt-0">
              <div class="flex flex-col justify-center items-center bg-base-300 rounded-xl sm:w-16 h-16">
                <div class="rating rating-sm">
                    <input
                      type="radio"
                      :name="'rating-' + user.uuid"
                      class="mask mask-star-2 bg-orange-400"
                      checked
                      disabled
                    />
                </div>
                <div class="text-sm">{{ user.rating }}</div>
              </div>
              <button @click.stop class="btn btn-primary w-full sm:w-16 h-16 rounded-xl flex flex-col justify-center items-center gap-0">
                <svg class="w-5 h-5 fill-primary-content">
                  <use href="#icon_chat"></use>
                </svg>
                <div class="text-sm">Чат</div>
              </button>   
            </div>     
          </div>
        </div>
    </div>
  </div>

    <!-- Модальное окно для полноразмерного просмотра -->
<dialog id="imageModal" class="modal" :open="isModalOpen" @click.self="closeModal">
  <!-- Модальное окно с адаптивными размерами -->
  <div class="modal-box p-0 relative w-auto max-w-none rounded-none md:rounded-box flex flex-col bg-base-300 backdrop-blur-sm h-[100dvh] md:h-[90vh]">
    <button 
      @click="closeModal" 
      class="absolute top-2 right-2 btn btn-circle btn-sm z-20"
      aria-label="Закрыть"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

    <!-- Контейнер изображения с возможностью прокрутки -->
    <div class="flex-1 overflow-hidden flex justify-center items-center relative">
      <img 
        :src="modalImage" 
        class="max-w-full max-h-full object-contain select-none"
        :style="{
          transform: `scale(${zoomLevel}) translate(${offsetX}px, ${offsetY}px)`
        }"
        alt="Фото автомобиля"
        draggable="false"
        @touchstart="startTouch"
        @touchmove="moveTouch"
        @touchend="endTouch"
        @mousedown="handleMouseDown"
        @mousemove="handleMouseMove"
        @mouseup="handleMouseUp"
      />
    </div>
    
    <!-- Панель управления с кнопками -->
    <div class="sticky bottom-0 bg-base-100 bg-opacity-90 p-2 flex justify-center gap-4 z-10">
      <button 
        @click.stop="prevImage" 
        :disabled="currentIndex === 0"
        class="btn btn-circle"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <button @click="zoomOut" class="btn btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
        </svg>
      </button>
      
      <button @click="zoomIn" class="btn btn-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
      
      <button 
        @click.stop="nextImage" 
        :disabled="currentIndex === car.images.length - 1"
        class="btn btn-circle"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
  
  <!-- Фон модального окна -->
  <form method="dialog" class="modal-backdrop">
    <button @click="closeModal">close</button>
  </form>
</dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import AddressDisplay from '@/components/AddressDisplay.vue'


const route = useRoute()
const router = useRouter()

const car = reactive({
  id: null,
  brand_id: null,
  brand_name: '',
  model_name: '',
  price: '',
  year: '',
  mileage: '',
  engine_power: '',
  transmission: '',
  drive_type: '',
  fuel_type: '',
  description: '',
  images: []
})

const user = reactive({
  uuid: '',
  name: '',
  avatar_url: '',
  registration_date: '',
  rating: 0
})

const currentImage = ref('')
const modalImage = ref('')
const isModalOpen = ref(false)
const currentIndex = ref(0)

const zoomLevel = ref(1)
const offsetX = ref(0)
const offsetY = ref(0)
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)

const imageWidth = ref(0)
const imageHeight = ref(0)

const initialDistance = ref(null)
const initialZoom = ref(1)

async function loadCarData(carUUID) {
  try {
    const response = await api.get(`/cars/${carUUID}`)
    const data = response.data
    Object.assign(car, data)
    if (data.user) {
      Object.assign(user, data.user)
      user.rating = parseFloat(user.rating).toFixed(2)
    }
    // Если нет изображений, добавляем превью
    if (data.images && data.images.length === 0 && data.preview_image_url) {
      car.images = [{ image_url: data.preview_image_url }]
    }
  } catch (error) {
    console.error('Ошибка загрузки данных автомобиля:', error)
  }
}

onMounted(async () => {
  const carUUID = route.params.uuid
  await loadCarData(carUUID)
  if (Array.isArray(car.images) && car.images.length > 0) {
    currentImage.value = car.images[0].image_url
    currentIndex.value = 0
  }
})

function goToUser(uuid) {
  router.push(`/user/${uuid}`)
}

function formatPrice(price) {
  if (!price) return ''
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(price)
}

function formatListingDate(dateString) {
  if (!dateString) return 'Дата не указана'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return 'Некорректная дата'
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

function formatTraderDate(dateString) {
  if (!dateString) return 'Дата не указана'
  const date = new Date(dateString)
  if (isNaN(date.getTime())) return 'Некорректная дата'
  return new Intl.DateTimeFormat('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date)
}

function openModal(imageUrl) {
  modalImage.value = imageUrl
  isModalOpen.value = true
  currentIndex.value = car.images.findIndex(img => img.image_url === imageUrl)

  const img = new Image()
  img.src = imageUrl
  img.onload = () => {
    imageWidth.value = img.naturalWidth
    imageHeight.value = img.naturalHeight
  }
  resetZoom()
}

function closeModal() {
  isModalOpen.value = false
  const modalEl = document.getElementById('imageModal')
  if (modalEl && modalEl.close) {
    modalEl.close()
  }
}

function prevImage() {
  if (currentIndex.value > 0) {
    resetZoom()
    currentIndex.value--
    currentImage.value = car.images[currentIndex.value].image_url
    if (isModalOpen.value) {
      modalImage.value = currentImage.value
    }
  }
}

function nextImage() {
  if (currentIndex.value < car.images.length - 1) {
    resetZoom()
    currentIndex.value++
    currentImage.value = car.images[currentIndex.value].image_url
    if (isModalOpen.value) {
      modalImage.value = currentImage.value
    }
  }
}

function resetZoom() {
  zoomLevel.value = 1
  offsetX.value = 0
  offsetY.value = 0
}

function applyMovementConstraints() {
  const container = document.querySelector('.modal-box')
  const imgEl = document.querySelector('.modal-box img')
  if (!container || !imgEl || !imageWidth.value || !imageHeight.value) return

  const containerRect = container.getBoundingClientRect()
  const scaledWidth = imageWidth.value * zoomLevel.value
  const scaledHeight = imageHeight.value * zoomLevel.value

  const maxOffsetX = Math.max(0, (scaledWidth - containerRect.width) / 2)
  const maxOffsetY = Math.max(0, (scaledHeight - containerRect.height) / 2)

  offsetX.value = Math.max(-maxOffsetX, Math.min(offsetX.value, maxOffsetX)) * 0.95
  offsetY.value = Math.max(-maxOffsetY, Math.min(offsetY.value, maxOffsetY)) * 0.95
}

function handleMouseDown(event) {
  if (event.button !== 0 || zoomLevel.value <= 1) return
  event.preventDefault()
  isDragging.value = true
  dragStartX.value = event.clientX - offsetX.value
  dragStartY.value = event.clientY - offsetY.value
}

function handleMouseMove(event) {
  if (!isDragging.value || zoomLevel.value <= 1) return
  event.preventDefault()

  offsetX.value = event.clientX - dragStartX.value
  offsetY.value = event.clientY - dragStartY.value

  applyMovementConstraints()
}

function handleMouseUp() {
  isDragging.value = false
}

function zoomIn() {
  const prevZoom = zoomLevel.value
  zoomLevel.value = Math.min(zoomLevel.value * 1.2, 3)
  adjustOffsetAfterZoom(prevZoom)
}

function zoomOut() {
  const prevZoom = zoomLevel.value
  const container = document.querySelector('.modal-box')
  if (!container) return

  const minScale = Math.min(
    1,
    Math.min(
      container.offsetWidth / imageWidth.value,
      container.offsetHeight / imageHeight.value
    )
  )
  zoomLevel.value = Math.max(zoomLevel.value / 1.2, minScale)
  adjustOffsetAfterZoom(prevZoom)
}

function adjustOffsetAfterZoom(prevZoom) {
  const ratio = zoomLevel.value / prevZoom
  offsetX.value *= ratio
  offsetY.value *= ratio
  applyMovementConstraints()
}

function handleZoom(event) {
  event.preventDefault()
  const delta = event.deltaY > 0 ? -0.1 : 0.1
  const prevZoom = zoomLevel.value
  zoomLevel.value = Math.min(Math.max(0.2, zoomLevel.value + delta), 3)

  if (zoomLevel.value !== prevZoom) {
    const rect = event.target.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top

    offsetX.value += (x - rect.width / 2) * (zoomLevel.value / prevZoom - 1)
    offsetY.value += (y - rect.height / 2) * (zoomLevel.value / prevZoom - 1)

    applyMovementConstraints()
  }
}

function startTouch(event) {
  if (event.touches.length === 2) {
    initialDistance.value = Math.hypot(
      event.touches[0].clientX - event.touches[1].clientX,
      event.touches[0].clientY - event.touches[1].clientY
    )
    initialZoom.value = zoomLevel.value
  } else if (zoomLevel.value > 1 && event.touches.length === 1) {
    const touch = event.touches[0]
    isDragging.value = true
    dragStartX.value = touch.clientX - offsetX.value
    dragStartY.value = touch.clientY - offsetY.value
  }
}

function moveTouch(event) {
  if (event.touches.length === 2) {
    event.preventDefault()
    const distance = Math.hypot(
      event.touches[0].clientX - event.touches[1].clientX,
      event.touches[0].clientY - event.touches[1].clientY
    )
    if (initialDistance.value) {
      zoomLevel.value = Math.min(
        Math.max(0.2, initialZoom.value * (distance / initialDistance.value)),
        3
      )
    }
  } else if (isDragging.value && zoomLevel.value > 1 && event.touches.length === 1) {
    event.preventDefault()
    const touch = event.touches[0]
    offsetX.value = touch.clientX - dragStartX.value
    offsetY.value = touch.clientY - dragStartY.value
    applyMovementConstraints()
  }
}

function endTouch() {
  isDragging.value = false
  initialDistance.value = null
}
</script>
