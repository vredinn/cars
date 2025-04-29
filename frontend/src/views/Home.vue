<template>
  <div>
    <HeroSection />

    <!-- Секция с брендами -->
    <section class="py-20 container mx-auto px-4 bg-white">
      <div class="flex justify-between items-center mb-10">
        <h2 class="text-3xl font-bold text-black">Бренды</h2>
        <button class="text-black text-black">Показать все бренды</button>
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
            <img :src="`http://192.168.0.101:8000/${brand.image_url}`" :alt="brand.name" class="w-1/2 h-auto mb-2">
            <span class="text-sm font-medium text-center text-black">{{ brand.name }}</span>
          </div>
        </div>
      </div>

    </section>

    <!-- Популярные объявления -->
    <section class="py-20 container mx-auto px-4 bg-white relative">
      <h2 class="text-3xl font-bold text-center mb-10 text-black">Популярные объявления</h2>

      <div ref="carousel" class="carousel bg-neutral w-full rounded-box space-x-4 p-4 scroll-p-4">
        <div v-for="(car, uuid) in popularCars" :key="uuid" class="flex-shrink-0">
          <div class="card carousel-item bg-base-100 border border-base-300 h-[400px] w-[306px]">
            <figure class="h-[200px]">
              <img :src="getImageUrl(car.preview_image_url)" :alt="car.title" class="object-cover w-full h-full">
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
                <span class="text-xl font-bold">{{ car.price }} руб.</span>
                <router-link 
  :to="`/car/${car.uuid}`" 
  class="btn btn-sm bg-black text-white hover:bg-gray-800"
>
  Подробнее
</router-link>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!isLoadingCars" class="btn carousel-item bg-base-100 border border-base-300 h-[400px] w-[306px] text-xl">
          Посмотреть все объявления
        </div>
      </div>

      <!-- Навигационные кнопки -->
      <div class="flex justify-center gap-6 mt-12 " :style="{ marginTop: '44px' }">
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
    <section class="py-20 container mx-auto px-4 bg-white">
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
    <section class="py-20 container mx-auto px-4 bg-white text-black">
    <h2 class="text-3xl font-bold text-center mb-10">Популярные продавцы</h2>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
      <!-- Карточка продавца 1 -->
      <div class="card bg-white shadow-md h-[400px] w-full mx-auto">
        <figure class="h-[306px] overflow-hidden">
          <img 
            src="/src/assets/sellers/Muhamed.png" 
            alt="Мухаммед"
            class="w-full h-full object-cover"
          >
        </figure>
        <div class="card-body p-4 text-center">
          <h3 class="card-title text-lg">Мухаммед</h3>
          <div class="rating rating-sm justify-center my-2">
            <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked disabled/>
            <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked disabled/>
            <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked disabled/>
            <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked disabled/>
          </div>
          <button class="btn btn-outline btn-sm mt-2">Подробнее</button>
        </div>
      </div>
      
      <!-- Карточка продавца 2 -->
      <div class="card bg-white shadow-md h-[400px] w-full mx-auto">
        <figure class="h-[306px] overflow-hidden">
          <img 
            src="/src/assets/sellers/Dmitry.jpg" 
            alt="Дмитрий"
            class="w-full h-full object-cover"
          >
        </figure>
        <div class="card-body p-4 text-center">
          <h3 class="card-title text-lg">Дмитрий</h3>
          <div class="rating rating-sm justify-center my-2">
            <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-2" class="mask mask-star-2 bg-orange-400" checked disabled/>
          </div>
          <button class="btn btn-outline btn-sm mt-2">Подробнее</button>
        </div>
      </div>
      
      <!-- Карточка продавца 3 -->
      <div class="card bg-white shadow-md h-[400px] w-full mx-auto">
        <figure class="h-[306px] overflow-hidden">
          <img 
            src="/src/assets/sellers/Kiril.jpg" 
            alt="Кирилл"
            class="w-full h-full object-cover"
          >
        </figure>
        <div class="card-body p-4 text-center">
          <h3 class="card-title text-lg">Кирилл</h3>
          <div class="rating rating-sm justify-center my-2">
            <input type="radio" name="rating-3" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-3" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-3" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-3" class="mask mask-star-2 bg-orange-400" checked disabled/>
            <input type="radio" name="rating-3" class="mask mask-star-2 bg-orange-400" checked disabled/>
          </div>
          <button class="btn btn-outline btn-sm mt-2">Подробнее</button>
        </div>
      </div>
      
      <!-- Карточка продавца 4 -->
      <div class="card bg-white shadow-md h-[400px] w-full mx-auto">
        <figure class="h-[306px] overflow-hidden">
          <img 
            src="/src/assets/sellers/Andrey.jpg" 
            alt="Андрей"
            class="w-full h-full object-cover"
          >
        </figure>
        <div class="card-body p-4 text-center">
          <h3 class="card-title text-lg">Андрей</h3>
          <div class="rating rating-sm justify-center my-2">
            <input type="radio" name="rating-4" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-4" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-4" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-4" class="mask mask-star-2 bg-orange-400" checked disabled />
            <input type="radio" name="rating-4" class="mask mask-star-2 bg-orange-400" checked disabled />
          </div>
          <button class="btn btn-outline btn-sm mt-2">Подробнее</button>
        </div>
      </div>
    </div>
  </section>
    <Footer />
  </div>
</template>

<script>
import HeroSection from '@/components/HeroSection.vue'
import footer from '../components/footer.vue'
import Footer from '../components/footer.vue'

export default {
  name: 'HomeView',
  components: { HeroSection, Footer},
  data() {
    return {
      brands: [],
      isLoadingBrands: true,
      popularCars: [],
      isLoadingCars: true,
      canScrollLeft: false,
      canScrollRight: true,
    }
  },
  mounted() {
    this.loadBrands()
    this.loadPopularCars()
    const carousel = this.$refs.carousel
    if (carousel) {
      carousel.addEventListener('scroll', this.updateScrollButtons)
    }
  },
  beforeUnmount() {
    const carousel = this.$refs.carousel;
    if (carousel) {
      carousel.removeEventListener('scroll', this.updateScrollButtons);
    }
  },
  methods: {
    async loadBrands() {
      this.isLoadingBrands = true
      try {
        const response = await fetch("http://192.168.0.101:8000/brands/");
        const data = await response.json();
        this.brands = data;
      } catch (error) {
        console.error("Ошибка загрузки брендов:", error);
      } finally {
        this.isLoadingBrands = false
      }
    },
    async loadPopularCars() {
      this.isLoadingCars = true
      try {
        const response = await fetch("http://192.168.0.101:8000/cars/popular");
        const data = await response.json();
        this.popularCars = data;
      } catch (error) {
        console.error("Ошибка загрузки популярных машин:", error);
      } finally {
        this.isLoadingCars = false
      }
    },
    updateScrollButtons() {
      const carousel = this.$refs.carousel;
      this.canScrollLeft = carousel.scrollLeft > 0;
      this.canScrollRight = Math.ceil(carousel.scrollLeft) < 
        Math.floor(carousel.scrollWidth - carousel.clientWidth);
    },
    nextSlide() {
      const carousel = this.$refs.carousel;
      const scrollAmount = 320;
      carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      this.updateScrollButtons // Обновляем состояние после прокрутки
    },
    prevSlide() {
      const carousel = this.$refs.carousel;
      const scrollAmount = -320;
      carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      setTimeout(this.updateScrollButtons, 500); // Обновляем состояние после прокрутки
    },
    getImageUrl(url) {
      return `http://192.168.0.101:8000/${url}`;
    }
  }
}
</script>
