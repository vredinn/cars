<template>
    <div class="container mx-auto p-4">
        
    <h1 class="text-2xl font-bold">Поиск объявлений</h1>
      <!-- Форма поиска с кнопкой toggle для мобильных -->
      <div class="bg-base-200 p-4 rounded-lg">
        <div class="flex justify-between items-center">
          <button class="btn btn-sm md:hidden mx-auto" @click="showFilters = !showFilters">
            {{ showFilters ? 'Скрыть фильтры' : 'Показать фильтры' }}
          </button>
        </div>
        
        <!-- Основной блок фильтров -->
        <div :class="{'hidden md:block': !showFilters}">
          <!-- Первая строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Марка</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.brand_id">
                <option :value="null">Любая</option>
                <option v-for="brand in brands" :value="brand.id">{{ brand.name }}</option>
              </select>
            </div>
            
            <div>
              <label class="label">
                <span class="label-text">Модель</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.model_id" :disabled="!tempFilters.brand_id">
                <option :value="null">Любая</option>
                <option v-for="model in filteredModels" :value="model.id">{{ model.name }}</option>
              </select>
            </div>
            
            <div>
              <label class="label">
                <span class="label-text">Состояние</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.car_condition">
                <option :value="null">Любое</option>
                <option v-for="car_condition in carConditions" :value="car_condition">{{ car_condition }}</option>
              </select>
            </div>
          </div>
  
          <!-- Вторая строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Год от</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_year" placeholder="Любой">
            </div>
            <div>
              <label class="label">
                <span class="label-text">Год до</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_year" placeholder="Любой">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">Руль</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.steering_side">
                <option :value="null">Любой</option>
                <option v-for="steering_side in steeringSides" :value="steering_side">{{ steering_side }}</option>
              </select>
            </div>
          </div>
          
          <!-- Третья строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Цена от</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_price" placeholder="Любая">
            </div>
            
            <div>
              <label class="label">
                <span class="label-text">Цена до</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_price" placeholder="Любая">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">Тип кузова</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.body_type">
                <option :value="null">Любой</option>
                <option v-for="body_type in bodyTypes" :value="body_type">{{ body_type }}</option>
              </select>
            </div>
          </div>
  
          <!-- Четвертая строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Объем двигателя от</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_capacity" placeholder="Любой">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">Объем двигателя до</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_capacity" placeholder="Любой">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">КПП</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.transmission">
                <option :value="null">Любая</option>
                <option v-for="transmission in transmissions" :value="transmission">{{ transmission }}</option>
              </select>
            </div>
          </div>
  
          <!-- Пятая строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Мощность от</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_power" placeholder="Любая">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">Мощность до</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_power" placeholder="Любая">
            </div>
            
            <div>
              <label class="label">
                <span class="label-text">Привод</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.drive_type">
                <option :value="null">Любой</option>
                <option v-for="drive_type in driveTypes" :value="drive_type">{{ drive_type }}</option>
              </select>
            </div>
          </div>
  
          <!-- Шестая строка фильтров -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label class="label">
                <span class="label-text">Пробег от</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_millage" placeholder="Любой">
            </div>
  
            <div>
              <label class="label">
                <span class="label-text">Пробег до</span>
              </label>
              <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_millage" placeholder="Любой">
            </div>
            
            <div>
              <label class="label">
                <span class="label-text">Топливо</span>
              </label>
              <select class="select select-bordered w-full" v-model="tempFilters.fuel_type">
                <option :value="null">Любое</option>
                <option v-for="fuel_type in fuelTypes" :value="fuel_type">{{ fuel_type }}</option>
              </select>
            </div>
          </div>
          
          <!-- Кнопки поиска и сброса -->
          <div class="flex justify-end">
            <button class="btn btn-primary mr-2" @click="searchCars">Поиск</button>
            <button class="btn btn-ghost" @click="resetFilters">Сбросить</button>
          </div>
        </div>
      </div>
      
      <div>
    <h2 class="text-xl font-bold mb-4">Подходящие предложения</h2>
    
    <div v-if="isLoading" class="flex justify-center my-8">
        <span class="loading loading-spinner loading-lg"></span>
      </div>
      
      <div v-else>
        <div class="grid grid-cols-1 gap-4" v-if="cars.length > 0">
          <CarCard 
            v-for="car in cars" 
            :key="car.id" 
            :car="car"
            @click="goToCarDetails(car.uuid)"
          />
        </div>
        
        <div v-else class="text-center py-8">
          <p class="text-lg">Ничего не найдено. Попробуйте изменить параметры поиска.</p>
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
</div>
  </template>

<script>
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
export default {
  name: 'CarSearchPage',
  components: {
    CarCard,
    Pagination
  },
  data() {
    return {
      showFilters: false,
      brands: [],
      models: [],
      carConditions: [],
      steeringSides: [],
      bodyTypes: [],
      transmissions: [],
      fuelTypes: [],
      driveTypes: [],
      // Активные фильтры (которые применяются)
      activeFilters: {
        brand_id: null,
        model_id: null,
        car_condition: null,
        transmission: null,
        drive_type: null,
        fuel_type: null,
        min_year: null,
        max_year: null,
        min_price: null,
        max_price: null,
        min_engine_power: null,
        max_engine_power: null,
        min_engine_capacity: null,
        max_engine_capacity: null,
        min_millage: null,
        max_millage: null,
        steering_side: null,
        body_type: null
      },
      // Временные фильтры (которые выбираются в форме)
      tempFilters: {
        brand_id: null,
        model_id: null,
        car_condition: null,
        transmission: null,
        drive_type: null,
        fuel_type: null,
        min_year: null,
        max_year: null,
        min_price: null,
        max_price: null,
        min_engine_power: null,
        max_engine_power: null,
        min_engine_capacity: null,
        max_engine_capacity: null,
        min_millage: null,
        max_millage: null,
        steering_side: null,
        body_type: null
      },
      currentPage: 1,
      totalPages: 1,
      cars: [],
      isLoading: false
    }
  },
  computed: {
    filteredModels() {
      if (!this.tempFilters.brand_id) return []
      return this.models.filter(model => model.brand_id === this.tempFilters.brand_id)
    },
    pagesToShow() {
      const pages = []
      const maxVisiblePages = 5
      
      let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2))
      let endPage = startPage + maxVisiblePages - 1
      
      if (endPage > this.totalPages) {
        endPage = this.totalPages
        startPage = Math.max(1, endPage - maxVisiblePages + 1)
      }
      
      for (let i = startPage; i <= endPage; i++) {
        pages.push(i)
      }
      
      return pages
    }
  },
  watch: {
    'tempFilters.brand_id'(newVal) {
      if (!newVal) {
        this.tempFilters.model_id = null
      }
    },
    $route() {
      this.parseQueryParams()
      this.fetchCars()
    }
  },
  methods: {
    formatPrice(price) {
      return new Intl.NumberFormat('ru-RU', { 
        style: 'currency', 
        currency: 'RUB',
        maximumFractionDigits: 0
      }).format(price)
    },
    getImageUrl(url) {
      return `http://192.168.0.101:8000/${url}`
    },
    async loadBrandsAndModels() {
      try {
        const [brandsRes, modelsRes] = await Promise.all([
          fetch('http://192.168.0.101:8000/brands/'),
          fetch('http://192.168.0.101:8000/models/')
        ])
        
        this.brands = await brandsRes.json()
        this.models = await modelsRes.json()
      } catch (error) {
        console.error('Ошибка загрузки брендов и моделей:', error)
      }
    },
    async loadEnums() {
      try {
        const enumsPromises = {
          carConditions: fetch('http://192.168.0.101:8000/enums/car-conditions/').then(r => r.json()),
          steeringSides: fetch('http://192.168.0.101:8000/enums/steering-sides/').then(r => r.json()),
          bodyTypes: fetch('http://192.168.0.101:8000/enums/body-types/').then(r => r.json()),
          transmissions: fetch('http://192.168.0.101:8000/enums/transmissions/').then(r => r.json()),
          fuelTypes: fetch('http://192.168.0.101:8000/enums/fuel-types/').then(r => r.json()),
          driveTypes: fetch('http://192.168.0.101:8000/enums/drive-types/').then(r => r.json())
        }

        const results = await Promise.all(Object.values(enumsPromises))
        ;[
          this.carConditions,
          this.steeringSides,
          this.bodyTypes,
          this.transmissions,
          this.fuelTypes,
          this.driveTypes
        ] = results
      } catch (error) {
        console.error('Ошибка загрузки enum списков:', error)
      }
    },
    parseQueryParams() {
      const query = this.$route.query
      
      // Преобразуем строковые значения в нужные типы
      this.currentPage = query.page ? parseInt(query.page) : 1
      
      // Заполняем активные фильтры из query параметров
      Object.keys(this.activeFilters).forEach(key => {
        if (query[key] !== undefined) {
          // Для числовых значений преобразуем в Number
          if (query[key] === 'null') {
            this.activeFilters[key] = null
            this.tempFilters[key] = null
          } else if (key.startsWith('min_') || key.startsWith('max_') || key.endsWith('_id')) {
            this.activeFilters[key] = query[key] ? parseInt(query[key]) : null
            this.tempFilters[key] = query[key] ? parseInt(query[key]) : null
          } else {
            this.activeFilters[key] = query[key] || null
            this.tempFilters[key] = query[key] || null
          }
        } else {
          this.activeFilters[key] = null
          this.tempFilters[key] = null
        }
      })
    },
    buildQueryParams(filters) {
      const params = { ...filters }
      
      // Удаляем null/undefined значения
      Object.keys(params).forEach(key => {
        if (params[key] === null || params[key] === undefined || params[key] === '') {
          delete params[key]
        }
      })
      
      // Добавляем текущую страницу
      if (this.currentPage > 1) {
        params.page = this.currentPage
      }
      
      return params
    },
    async fetchCars() {
      this.isLoading = true
      
      try {
        const queryParams = this.buildQueryParams(this.activeFilters)
        const queryString = new URLSearchParams(queryParams).toString()
        
        const response = await fetch(`http://192.168.0.101:8000/cars/?${queryString}`)
        const data = await response.json()
        
        this.cars = data.items
        this.totalPages = data.pages
        this.currentPage = data.page
      } catch (error) {
        console.error('Ошибка загрузки автомобилей:', error)
        this.cars = []
      } finally {
        this.isLoading = false
      }
    },
    searchCars() {
      // Копируем временные фильтры в активные
      this.activeFilters = { ...this.tempFilters }
      
      // Сбрасываем на первую страницу при новом поиске
      this.currentPage = 1
      this.updateRoute()
    },
    resetFilters() {
      // Сбрасываем все фильтры
      Object.keys(this.tempFilters).forEach(key => {
        this.tempFilters[key] = null
      })
      
      // Если были активные фильтры - сбрасываем и их
      if (Object.values(this.activeFilters).some(val => val !== null)) {
        Object.keys(this.activeFilters).forEach(key => {
          this.activeFilters[key] = null
        })
        
        this.currentPage = 1
        this.updateRoute()
      }
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages || page === this.currentPage) return
      
      this.currentPage = page
      this.updateRoute()
    },
    updateRoute() {
      const query = this.buildQueryParams(this.activeFilters)
            
      this.$router.push({
        query: query
      }).catch(() => {})
    }
  },
  mounted() {
    this.loadBrandsAndModels()
    this.loadEnums()
    this.parseQueryParams()
    this.fetchCars()
  }
}
</script>