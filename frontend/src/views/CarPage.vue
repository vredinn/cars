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
              :src="currentImage" 
              class="w-full h-96 object-contain cursor-pointer bg-black rounded" 
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
                :src="img.image_url" 
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

    <!-- Модальное окно для полноразмерного просмотра -->
<dialog id="imageModal" class="modal" :open="isModalOpen" @click.self="closeModal">
  <!-- Модальное окно с адаптивными размерами -->
  <div class="modal-box p-0 relative w-auto max-w-none bg-black flex flex-col h-[90vh]">
    <button 
      @click="closeModal" 
      class="absolute top-2 right-2 btn btn-circle btn-sm btn-ghost z-20"
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
    
    <!-- Панель управления с кнопками DaisyUI -->
    <div class="sticky bottom-0 bg-base-100 bg-opacity-90 p-2 flex justify-center gap-2 z-10">
      <button 
        @click.stop="prevImage" 
        :disabled="currentIndex === 0"
        class="btn btn-circle btn-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      
      <button @click="zoomOut" class="btn btn-circle btn-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
        </svg>
      </button>
      
      <button @click="zoomIn" class="btn btn-circle btn-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
      </button>
      
      <button 
        @click.stop="nextImage" 
        :disabled="currentIndex === car.images.length - 1"
        class="btn btn-circle btn-sm"
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

<script>
import api from '@/api'

export default {
  name: 'CarPage',
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
      isModalOpen: false,
      currentIndex: 0,
      zoomLevel: 1,
      offsetX: 0,
      offsetY: 0,
      startX: 0,
      startY: 0,
      isDragging: false,
      dragStartX: 0,
      dragStartY: 0,
      imageWidth: 0,
      imageHeight: 0,
      initialDistance: null,
      initialZoom: 1
    }
  },
  async created() {
    const carUUID = this.$route.params.uuid
    await this.loadCarData(carUUID)
    if (Array.isArray(this.car.images) && this.car.images.length > 0) {
      this.currentImage = this.car.images[0].image_url
      this.currentIndex = 0
    }
  },
  methods: {
      handleMobileMove(event) {
    if (this.isDragging && this.zoomLevel > 1) {
      event.preventDefault();
      const touch = event.type.includes('touch') ? event.touches[0] : event;
      this.offsetX = touch.clientX - this.dragStartX;
      this.offsetY = touch.clientY - this.dragStartY;
      this.applyMovementConstraints();
    }
  },
    async loadCarData(carUUID) {
      try {
        const response = await api.get(`/cars/${carUUID}`)
        const data = await response.data
        this.car = data
        // Если нет изображений, добавляем превью
        if (data.images && data.images.length === 0 && data.preview_image_url) {
          this.car.images = [{ image_url: data.preview_image_url }]
        }
      } catch (error) {
        console.error('Ошибка загрузки данных автомобиля:', error)
      }
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
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'Некорректная дата';
      return new Intl.DateTimeFormat('ru-RU', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    },
    prevImage() {
      if (this.currentIndex > 0) {
        this.zoomLevel = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.currentIndex--;
        this.currentImage = this.car.images[this.currentIndex].image_url;
        if (this.isModalOpen) {
          this.modalImage = this.currentImage;
        }
      }
    },
    nextImage() {
      if (this.currentIndex < this.car.images.length - 1) {
        this.zoomLevel = 1;
        this.offsetX = 0;
        this.offsetY = 0;
        this.currentIndex++;
        this.currentImage = this.car.images[this.currentIndex].image_url;
        if (this.isModalOpen) {
          this.modalImage = this.currentImage;
        }
      }
    },
  openModal(imageUrl) {
    this.modalImage = imageUrl;
    this.isModalOpen = true;
    this.currentIndex = this.car.images.findIndex(img => img.image_url === imageUrl);
    
    const img = new Image();
    img.src = imageUrl;
    img.onload = () => {
      this.imageWidth = img.naturalWidth;
      this.imageHeight = img.naturalHeight;
      document.getElementById('imageModal').showModal();
    };
  },
  handleMouseDown(event) {
    if (event.button !== 0 || this.zoomLevel <= 1) return;
    event.preventDefault();
    this.isDragging = true;
    this.dragStartX = event.clientX - this.offsetX;
    this.dragStartY = event.clientY - this.offsetY;
  },
    
  handleMouseMove(event) {
    if (!this.isDragging || this.zoomLevel <= 1) return;
    event.preventDefault();
    
    // Плавное перемещение без коэффициента
    this.offsetX = event.clientX - this.dragStartX;
    this.offsetY = event.clientY - this.dragStartY;
    
    this.applyMovementConstraints();
  },
    handleMouseUp() {
      this.isDragging = false;
    },
  zoomIn() {
    const prevZoom = this.zoomLevel;
    // Увеличиваем масштаб с учетом текущей позиции
    this.zoomLevel = Math.min(this.zoomLevel * 1.2, 3);
    this.adjustOffsetAfterZoom(prevZoom);
  },
  zoomOut() {
    const prevZoom = this.zoomLevel;
    // Уменьшаем масштаб, но не меньше чем нужно для заполнения контейнера
    const minScale = Math.min(
      1,
      Math.min(
        this.$el.querySelector('.modal-box').offsetWidth / this.imageWidth,
        this.$el.querySelector('.modal-box').offsetHeight / this.imageHeight
      )
    );
    this.zoomLevel = Math.max(this.zoomLevel / 1.2, minScale);
    this.adjustOffsetAfterZoom(prevZoom);
  },
  adjustOffsetAfterZoom(prevZoom) {
    const container = this.$el.querySelector('.modal-box');
    if (!container || !this.imageWidth || !this.imageHeight) return;
    
    const ratio = this.zoomLevel / prevZoom;
    this.offsetX *= ratio;
    this.offsetY *= ratio;
    
    this.applyMovementConstraints();
  },
  handleZoom(event) {
    event.preventDefault();
    const delta = event.deltaY > 0 ? -0.1 : 0.1;
    const prevZoom = this.zoomLevel;
    this.zoomLevel = Math.min(Math.max(0.2, this.zoomLevel + delta), 3);
    
    // Позиционируем курсор в точке масштабирования
    if (this.zoomLevel !== prevZoom) {
      const rect = event.target.getBoundingClientRect();
      const x = event.clientX - rect.left;
      const y = event.clientY - rect.top;
      
      this.offsetX += (x - rect.width/2) * (this.zoomLevel/prevZoom - 1);
      this.offsetY += (y - rect.height/2) * (this.zoomLevel/prevZoom - 1);
      
      this.applyMovementConstraints();
    }
  },
  startTouch(event) {
    if (event.touches.length === 2) {
      // Жест двумя пальцами
      this.initialDistance = Math.hypot(
        event.touches[0].clientX - event.touches[1].clientX,
        event.touches[0].clientY - event.touches[1].clientY
      );
      this.initialZoom = this.zoomLevel;
    } else if (this.zoomLevel > 1) {
      // Перемещение одним пальцем
      const touch = event.touches[0];
      this.isDragging = true;
      this.dragStartX = touch.clientX - this.offsetX;
      this.dragStartY = touch.clientY - this.offsetY;
    }
  },
  moveTouch(event) {
    if (event.touches.length === 2) {
      // Обработка масштабирования
      event.preventDefault();
      const distance = Math.hypot(
        event.touches[0].clientX - event.touches[1].clientX,
        event.touches[0].clientY - event.touches[1].clientY
      );
      if (this.initialDistance) {
        this.zoomLevel = Math.min(
          Math.max(0.2, this.initialZoom * (distance / this.initialDistance)),
          3
        );
      }
    } else if (this.isDragging && this.zoomLevel > 1) {
      // Обработка перемещения
      event.preventDefault();
      const touch = event.touches[0];
      this.offsetX = touch.clientX - this.dragStartX;
      this.offsetY = touch.clientY - this.dragStartY;
      this.applyMovementConstraints();
    }
  },
  applyMovementConstraints() {
    const container = this.$el.querySelector('.modal-box');
    if (!container || !this.imageWidth || !this.imageHeight) return;
    
    const containerRect = container.getBoundingClientRect();
    const imgRect = this.$el.querySelector('img').getBoundingClientRect();
    
    const scaledWidth = this.imageWidth * this.zoomLevel;
    const scaledHeight = this.imageHeight * this.zoomLevel;
    
    const maxOffsetX = Math.max(0, (scaledWidth - containerRect.width) / 2);
    const maxOffsetY = Math.max(0, (scaledHeight - containerRect.height) / 2);
    
    // Мягкие границы с "эффектом пружины"
    this.offsetX = Math.max(-maxOffsetX, Math.min(this.offsetX, maxOffsetX)) * 0.95;
    this.offsetY = Math.max(-maxOffsetY, Math.min(this.offsetY, maxOffsetY)) * 0.95;
  }
},
    // startDrag(event) {
    //   if (this.zoomLevel <= 1) return;
    //   this.isDragging = true;
    //   this.dragStartX = event.clientX;
    //   this.dragStartY = event.clientY;
    // },
    
    // dragMove(event) {
    //     if (!this.isDragging || this.zoomLevel <= 1) return;

    //     const deltaX = event.clientX - this.dragStartX;
    //     const deltaY = event.clientY - this.dragStartY;
    //     this.offsetX += deltaX;
    //     this.offsetY += deltaY;

    //     this.dragStartX = event.clientX;
    //     this.dragStartY = event.clientY;
    //     const container = this.$el.querySelector('.modal-box .w-full.h-[80vh]');
    //     if (!container) return;

    //     const containerWidth = container.offsetWidth;
    //     const containerHeight = container.offsetHeight;

    //     const scaledWidth = this.imageWidth * this.zoomLevel;
    //     const scaledHeight = this.imageHeight * this.zoomLevel;

    //     const maxOffsetX = Math.max(0, (scaledWidth - containerWidth) / 2);
    //     const maxOffsetY = Math.max(0, (scaledHeight - containerHeight) / 2);

    //     this.offsetX = Math.max(-maxOffsetX, Math.min(this.offsetX + deltaX, maxOffsetX));
    //     this.offsetY = Math.max(-maxOffsetY, Math.min(this.offsetY + deltaY, maxOffsetY));

    //     this.dragStartX = event.clientX;
    //     this.dragStartY = event.clientY;
    //   },
    // endDrag() {
    //   this.isDragging = false;
    // },
      handleMouseUp() {
    this.isDragging = false;
  },
        endTouch() {
      this.isDragging = false;
      this.initialDistance = null;
    }
  }
</script>
<style>
/* Для лучшего отображения на мобильных */
@media (max-width: 768px) {
  .modal-box {
    width: 100vw !important;
    height: 100vh !important;
    max-height: none !important;
    border-radius: 0 !important;
  }
    .modal-box .btn-ghost {
    width: 44px;
    height: 44px;
  }
  
  /* Увеличиваем кнопки для мобильных */
  .btn-circle {
    width: 44px;
    height: 44px;
  }
    .modal-box .btn-ghost svg {
    width: 24px;
    height: 24px;
  }
}
</style>