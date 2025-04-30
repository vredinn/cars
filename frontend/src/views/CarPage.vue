<template>
    <div class="min-h-screen flex flex-col">
      
      <main class="flex-grow container mx-auto px-4 py-8">

        
        <!-- Основное содержимое страницы -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Галерея изображений -->
          <div>
            <!-- Основное изображение -->
            <div class="w-full mb-4 rounded-lg overflow-hidden">
              <img 
                :src="getImageUrl(currentImage)" 
                class="w-full h-96 object-cover cursor-pointer" 
                alt="Фото автомобиля"
                @click="openModal(currentImage)"
              >
            </div>
            
            <!-- Превью изображений -->
            <div class="flex overflow-x-auto pb-2 gap-2">
              <div 
                v-for="(img, index) in car.images" 
                :key="index"
                class="flex-none w-24 h-20"
              >
                <img 
                  :src="getImageUrl(img.image_url)" 
                  class="w-full h-full object-cover rounded cursor-pointer"
                  :class="{'ring-2 ring-primary': currentImage === img.image_url}"
                  @click="currentImage = img.image_url"
                  alt="Превью фото"
                >
              </div>
            </div>
          </div>
  
          <!-- Информация об автомобиле -->
          <div>
            <div class="bg-base-200 rounded-lg text-center  mb-4 py-2">
              <h1 class="text-3xl font-bold mb-4">{{ car.brand_name }} {{ car.model_name }}</h1>
              <div class="font-bold text-lg">{{ formatPrice(car.price) }}</div>
            </div>
  
            <!-- Характеристики -->
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Год</div>
                <div class="font-bold">{{ car.year }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Состояние автомобиля</div>
                <div class="font-bold">{{ car.car_condition }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Кузов</div>
                <div class="font-bold">{{ car.body_type }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Цвет</div>
                <div class="font-bold">{{ car.color }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Пробег</div>
                <div class="font-bold">{{ car.mileage.toLocaleString() }} км</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Мощность двигателя</div>
                <div class="font-bold">{{ car.engine_power }} л.с.</div>
              </div>              
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Объем двигателя</div>
                <div class="font-bold">{{ car.engine_capacity }} л</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Коробка</div>
                <div class="font-bold">{{ car.transmission }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Топливо</div>
                <div class="font-bold">{{ car.fuel_type }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Привод</div>
                <div class="font-bold">{{ car.drive_type }}</div>
              </div>
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Руль</div>
                <div class="font-bold">{{ car.steering_side }}</div>
              </div>
              
              <div class="bg-base-200 p-4 rounded-lg">
                <div class="text-gray-500">Дата объявления</div>
                <div class="font-bold">{{ formatListingDate(car.listing_date) }}</div>
              </div>
            </div>
  
            <!-- Описание -->
            <div class="prose bg-base-200 p-6 rounded-lg">
              <h3>Описание</h3>
              <p>{{ car.description }}</p>
            </div>
          </div>
        </div>
      </main>
  
      <Footer />

      <!-- Модальное окно для полноразмерного просмотра -->
      <dialog id="imageModal" class="modal" :open="isModalOpen" @click="closeModal">
        <div class="modal-box w-11/12 max-w-5xl p-0 overflow-hidden">
          <img 
            :src="getImageUrl(modalImage)" 
            class="w-full h-full object-contain" 
            alt="Фото автомобиля"
          >
        </div>
        <form method="dialog" class="modal-backdrop">
          <button @click="closeModal">close</button>
        </form>
      </dialog>
    </div>
</template>
  
<script>
import Footer from '@/components/Footer.vue'

export default {

  name: 'CarPage',
  components: {Footer },
  data() {
    return {
      car: {
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
      },
      currentImage: '',
      modalImage: '',
      isModalOpen: false
    }
  },
  async created() {
    const carId = this.$route.params.id
    await this.loadCarData(carId)
    if (this.car.images.length > 0) {
      this.currentImage = this.car.images[0].image_url
    }
  },
  methods: {
    async loadCarData(carId) {
      try {
        const response = await fetch(`http://192.168.0.101:8000/cars/${carId}`)
        const data = await response.json()
        this.car = data
        
        // Если нет изображений, добавляем превью
        if (data.images && data.images.length === 0 && data.preview_image_url) {
          this.car.images = [{ image_url: data.preview_image_url }]
        }
      } catch (error) {
        console.error('Ошибка загрузки данных автомобиля:', error)
      }
    },
    getImageUrl(url) {
      return `http://192.168.0.101:8000/${url}`
    },
    openModal(imageUrl) {
      this.modalImage = imageUrl
      this.isModalOpen = true
      document.getElementById('imageModal').showModal()
    },
    closeModal() {
      this.isModalOpen = false
      document.getElementById('imageModal').close()
    },
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU', { 
        style: 'currency', 
        currency: 'RUB',
        maximumFractionDigits: 0
      }).format(price)
    },
    formatListingDate(dateString) {
    if (!dateString) return 'Дата не указана';
    
    try {
      const date = new Date(dateString);
      
      // Проверяем, что дата валидна
      if (isNaN(date.getTime())) {
        return 'Некорректная дата';
      }
      
      // Форматируем дату с учетом локали пользователя
      return new Intl.DateTimeFormat('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
      
    } catch (e) {
      console.error('Ошибка форматирования даты:', e);
      return dateString; // Возвращаем оригинальную строку в случае ошибки
    }
  }
  }
}
</script>