<template>
  <div>
    <HeroSection />
    
    <!-- Секция с брендами -->
    <section class="py-20 container mx-auto px-4 bg-white">
      <div class="flex justify-between items-center mb-10">
        <h2 class="text-3xl font-bold text-black">Бренды</h2>
        <button class="text-black text-black">Показать все бренды</button>
      </div>
      
      <!-- Сетка (6 на десктопе, 3 на мобилке) -->
      <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6 gap-6">
        <div 
          v-for="brand in brands" 
          :key="brand.id"
          class="flex flex-col items-center"
        >
          <!-- Круглый контейнер с логотипом и названием внутри -->
          <div class="w-full aspect-square rounded-full bg-white flex flex-col items-center justify-center p-4 hover:shadow-lg transition-all shadow-md">
            <!-- Логотип -->
            <img 
              :src="`/src/assets/brands/${brand.image}`" 
              :alt="brand.name" 
              class="w-1/2 h-auto mb-2"
            >
            <!-- Название бренда -->
            <span class="text-sm font-medium text-center text-black">{{ brand.name }}</span>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Популярные объявления -->
    <section class="py-20 container mx-auto px-4 bg-white relative">
      <h2 class="text-3xl font-bold text-center mb-10 ">Популярные объявления</h2>
      
      <!-- Обертка слайдера -->
      <div class="relative overflow-hidden">
        <!-- Контейнер карточек -->
        <div 
          class="flex transition-transform duration-500 ease-in-out"
          :style="{ transform: `translateX(-${currentSlide * (100 / visibleCards)}%)` }"
          ref="slider"
        >
          <!-- Карточки автомобилей -->
          <div 
  v-for="(car, index) in popularCars" 
  :key="index"
  class="flex-shrink-0 px-3"
  :style="{ width: `${100 / visibleCards}%` }"
>
  <div class="card bg-white border border-gray-300 h-[400px] w-[306px] mx-auto">
    <figure class="h-[200px]">
      <img :src="car.image" :alt="car.title" class="object-cover w-full h-full">
    </figure>
    <div class="card-body p-4 text-black">
      <h3 class="card-title text-lg">{{ car.title }}</h3>
      <p class="text-sm">{{ car.specs }}</p>
      <div class="flex flex-wrap gap-2 my-2">
        <div class="badge badge-outline border-gray-300 text-gray-800">{{ car.mileage }}</div>
        <div class="badge badge-outline border-gray-300 text-gray-800">{{ car.fuel }}</div>
        <div class="badge badge-outline border-gray-300 text-gray-800">{{ car.transmission }}</div>
      </div>
      <div class="card-actions justify-between items-center mt-auto">
        <span class="text-xl font-bold">{{ car.price }}</span>
        <button class="btn btn-sm bg-black text-white hover:bg-gray-800">Подробнее</button>
      </div>
    </div>
  </div>
</div>
        </div>
      </div>

      <!-- Навигационные кнопки -->
      <div class="flex justify-center gap-6 mt-12 " :style="{ marginTop: '44px' }">
  <button 
    @click="prevSlide"
    class="btn btn-circle btn-outline border-gray-300 text-black hover:bg-black hover:text-white w-[60px] h-[40px] min-h-[40px]"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M15 18l-6-6 6-6"/>
    </svg>
  </button>
  <button 
    @click="nextSlide"
    class="btn btn-circle btn-outline border-gray-300 text-black hover:bg-black hover:text-white w-[60px] h-[40px] min-h-[40px]"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M9 18l6-6-6-6"/>
    </svg>
  </button>
</div>
    </section>
    <!-- Новая секция "Получите справедливую цену" -->
    <section class="py-20 container mx-auto px-4 bg-white ">
      <!-- Верхняя часть: изображение и текст -->
      <div class="flex flex-col lg:flex-row gap-10 mb-16  ">
        <!-- Изображение машины (левая часть) -->
        <div class="lg:w-1/2 ">
          <img 
            src="/src/assets/cars/Background.png" 
            alt="Продажа автомобиля" 
            class="w-full h-full  shadow-md rounded-l-[24px]"
          >
        </div>
        
        <!-- Текст (правая часть) -->
        <div class="lg:w-1/2 flex flex-col justify-center bg-[#EDEDED] rounded-r-[24px]">
          <h2 class="text-3xl font-bold mb-4 text-black">ПОЛУЧИТЕ СПРАВЕДЛИВУЮ ЦЕНУ ЗА СВОЙ АВТОМОБИЛЬ</h2>
          <h3 class="text-2xl mb-6 font-semibold text-black">Продайте его сегодня</h3>
          
          <p class="mb-8 text-gray-700 text-black">Мы стремимся предоставлять нашим клиентам исключительный сервис, конкурентоспособные цены и широкий ассортимент</p>
          
          <ul class="space-y-4 mb-8">
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="text-gray-700 text-black">Бесплатная оценка автомобиля онлайн за 5 минут</span>
            </li>
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="text-gray-700 text-black">Продажа авто в любом состоянии — даже после аварии</span>
            </li>
            <li class="flex items-center">
              <input type="checkbox" checked class="checkbox checkbox-black mr-3" disabled />
              <span class="text-gray-700 text-black">Удобное общение с покупателями</span>
            </li>
          </ul>
          
          <button class="btn btn-black px-8 py-3 text-lg w-fit">Начать</button>
        </div>
      </div>
      
      <!-- Нижняя часть: статистика -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 ">
        <!-- Блоки статистики -->
        <div class="bg-gray-50 p-6 rounded-lg text-center bg-white">
          <div class="text-4xl font-bold mb-2 text-black">836M</div>
          <div class="text-gray-600 uppercase text-sm">Автомобилей в продаже</div>
        </div>
        <div class="bg-gray-50 p-6 rounded-lg text-center bg-white">
          <div class="text-4xl font-bold mb-2 text-black">738M</div>
          <div class="text-gray-600 uppercase text-sm">Отзывов о дилерах</div>
        </div>
        <div class="bg-gray-50 p-6 rounded-lg text-center bg-white">
          <div class="text-4xl font-bold mb-2 text-black">238M</div>
          <div class="text-gray-600 uppercase text-sm">Проверенных дилеров</div>
        </div>
        <div class="bg-gray-50 p-6 rounded-lg text-center bg-white">
          <div class="text-4xl font-bold mb-2 text-black">100M</div>
          <div class="text-gray-600 uppercase text-sm">Посетителей в день</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import HeroSection from '@/components/HeroSection.vue'

export default {
  name: 'HomeView',
  components: { HeroSection },
  data() {
    return {
      brands: [
        { id: 1, name: 'Mercedes-Benz', image: 'mercedes.png' },
        { id: 2, name: 'BMW', image: 'bmw.png' },
        { id: 3, name: 'Audi', image: 'audi.png' },
        { id: 4, name: 'Volkswagen', image: 'volkswagen.png' },
        { id: 5, name: 'Ford', image: 'ford.png' },
        { id: 6, name: 'Peugeot', image: 'peugeot.png' },
      ],
      popularCars: [
        {
          title: 'ВАЗ 2112',
          specs: '1,6 л (16 клапанов), 5–МКПП, Привод ...',
          mileage: '50000 Км',
          fuel: 'Бензин',
          transmission: 'Вариатор',
          price: 'Р35,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'Kia Rio',
          specs: '1,6 л, 4–МКПП, Передний привод',
          mileage: '75000 Км',
          fuel: 'Бензин',
          transmission: 'Механика',
          price: 'Р45,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'ВАЗ 2112',
          specs: '1,6 л (16 клапанов), 5–МКПП, Привод ...',
          mileage: '50000 Км',
          fuel: 'Бензин',
          transmission: 'Вариатор',
          price: 'Р35,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'Kia Rio',
          specs: '1,6 л, 4–МКПП, Передний привод',
          mileage: '75000 Км',
          fuel: 'Бензин',
          transmission: 'Механика',
          price: 'Р45,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'ВАЗ 2112',
          specs: '1,6 л (16 клапанов), 5–МКПП, Привод ...',
          mileage: '50000 Км',
          fuel: 'Бензин',
          transmission: 'Вариатор',
          price: 'Р35,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'Kia Rio',
          specs: '1,6 л, 4–МКПП, Передний привод',
          mileage: '75000 Км',
          fuel: 'Бензин',
          transmission: 'Механика',
          price: 'Р45,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'ВАЗ 2112',
          specs: '1,6 л (16 клапанов), 5–МКПП, Привод ...',
          mileage: '50000 Км',
          fuel: 'Бензин',
          transmission: 'Вариатор',
          price: 'Р35,000',
          image: '/src/assets/cars/lada12.jpg'
        },
        {
          title: 'Kia Rio',
          specs: '1,6 л, 4–МКПП, Передний привод',
          mileage: '75000 Км',
          fuel: 'Бензин',
          transmission: 'Механика',
          price: 'Р45,000',
          image: '/src/assets/cars/lada12.jpg'
        },  
      ],
      currentSlide: 0,
      autoSlideInterval: null,
      visibleCards: 4
    }
  },
  mounted() {
    this.updateVisibleCards()
    window.addEventListener('resize', this.updateVisibleCards)
    this.startAutoSlide()
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateVisibleCards)
    this.stopAutoSlide()
  },
  methods: {
    updateVisibleCards() {
      if (window.innerWidth < 640) {
        this.visibleCards = 2 // 2 карточки на мобильных
      } else if (window.innerWidth < 768) {
        this.visibleCards = 3 // 3 карточки на планшетах
      } else {
        this.visibleCards = 4 // 4 карточки на десктопе
      }
    },
    startAutoSlide() {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide()
      }, 4000) // 4 секунды
    },
    stopAutoSlide() {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval)
      }
    },
    nextSlide() {
      if (this.currentSlide >= this.popularCars.length - this.visibleCards) {
        this.currentSlide = 0
      } else {
        this.currentSlide++
      }
    },
    prevSlide() {
      if (this.currentSlide <= 0) {
        this.currentSlide = Math.max(0, this.popularCars.length - this.visibleCards)
      } else {
        this.currentSlide--
      }
    }
  }
}
</script>

<style scoped>
/* Адаптация для мобилок */
@media (max-width: 640px) {
  .aspect-square {
    width: 80px;
    height: 80px;
  }
  .text-sm {
    font-size: 0.7rem; /* Уменьшаем текст на мобилках */
  }
  /* карточки автомобилей */
  .card {
    width: 136px !important;
    height: 245.75px !important;
  }
  .card figure {
    height: 120px !important;
  }
  .card-body {
    padding: 0.5rem !important;
  }
  .card-title {
    font-size: 0.875rem !important;
  }
  .text-sm {
    font-size: 0.75rem !important;
  }
  .badge {
    font-size: 0.65rem !important;
    padding: 0.25rem 0.5rem !important;
  }
  /* блок с ифной */
  .grid-cols-2 {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .text-4xl {
    font-size: 1.75rem;
    line-height: 2.25rem;
  }
  
  .text-3xl {
    font-size: 1.5rem;
    line-height: 2rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
    line-height: 1.75rem;
  }
  
  .px-4 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .gap-10 {
    gap: 1.5rem;
  }
  
  .p-6 {
    padding: 1rem;
  }
  
  .mb-16 {
    margin-bottom: 2rem;
  }
}
/* Плавные переходы */
.transition-transform {
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 500ms;
}
</style>