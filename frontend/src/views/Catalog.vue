<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Поиск объявлений</h1>
    <!-- Кнопка для открытия drawer на мобильных -->
    <button class="btn btn-primary md:hidden mb-4" @click="showDrawer = true">
      Показать фильтры
    </button>
    
    <!-- Основной контент -->
    <div class="flex gap-4">

      <div class="drawer md:drawer-open md:gap-2">
        <input id="my-drawer" type="checkbox" class="drawer-toggle" v-model="showDrawer">
        <div class="drawer-content">
          <!-- Контент страницы -->
            <h2 class="text-xl font-bold mb-4">Подходящие предложения</h2>
            
            <div v-if="isLoading" class="flex justify-center my-8">
              <span class="loading loading-spinner loading-lg"></span>
            </div>
            
            <div v-else>
              <div class="flex flex-col gap-4" v-if="cars.length > 0">
                <CarCard 
                  v-for="car in cars" 
                  :key="car.id" 
                  :car="car"
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
        <div class="drawer-side md:pr-2">  
          <label for="my-drawer" class="drawer-overlay"></label>
          <div class="bg-base-300 md:rounded-box p-4 md:w-75 flex flex-col min-h-[100dvh] md:min-h-0 max-h-[100dvh]">
            <!-- Шапка -->
            <div class="flex justify-between items-center mb-4 md:mb-0">
              <h2 class="text-xl font-bold mb-2 md:hidden">Фильтры</h2>
              <label for="my-drawer" class="btn btn-sm btn-circle md:hidden">✕</label>
            </div>
            
            <!-- Фильтры -->
            <div class="flex-1 overflow-y-auto pb-4">
              <div class="grid gap-4">
                <div class="collapse collapse-plus bg-base-200">
                  <input type="checkbox" checked>
                  <div class="collapse-title font-medium">
                    Основные параметры
                  </div>
                  <div class="collapse-content grid gap-4">
                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Марка</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.brand_id"
                        :options="brands"
                        labelKey="name"
                        valueKey="id"
                        placeholder="Любая"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Модель</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.model_id"
                        :options="filteredModels"
                        labelKey="name"
                        valueKey="id"
                        placeholder="Любая"
                        :disabled="!tempFilters.brand_id"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Состояние</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.car_condition"
                        :options="carConditions"
                        placeholder="Любое"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Цена от</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_price" placeholder="Любая">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Цена до</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_price" placeholder="Любая">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Год от</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_year" placeholder="Любой">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Год до</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_year" placeholder="Любой">
                    </div>
                  </div>
                </div>

                <div class="collapse collapse-plus bg-base-200">
                  <input type="checkbox">
                  <div class="collapse-title font-medium">
                    Параметры автомобиля
                  </div>
                  <div class="collapse-content grid gap-4">
                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Тип кузова</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.body_type"
                        :options="bodyTypes"
                        placeholder="Любой"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">КПП</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.transmission"
                        :options="transmissions"
                        placeholder="Любая"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Привод</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.drive_type"
                        :options="driveTypes"
                        placeholder="Любой"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Руль</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.steering_side"
                        :options="steeringSides"
                        placeholder="Любой"
                      />
                    </div>
                  </div>
                </div>

                <div class="collapse collapse-plus bg-base-200">
                  <input type="checkbox">
                  <div class="collapse-title font-medium">
                    Параметры двигателя
                  </div>
                  <div class="collapse-content grid gap-4">
                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Топливо</span>
                      </label>
                      <SearchableSelect
                        v-model="tempFilters.fuel_type"
                        :options="fuelTypes"
                        placeholder="Любое"
                      />
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Мощность от</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_power" placeholder="Любая">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Мощность до</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_power" placeholder="Любая">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Объем двигателя от</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_capacity" placeholder="Любой">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Объем двигателя до</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_capacity" placeholder="Любой">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Пробег от</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_millage" placeholder="Любой">
                    </div>

                    <div>
                      <label class="label mb-1">
                        <span class="label-text">Пробег до</span>
                      </label>
                      <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_millage" placeholder="Любой">
                    </div>
                  </div>
                </div>
              </div>

            </div>
            
              <!-- Кнопки поиска и сброса -->
              <div class="flex gap-2 pt-4">
                <button class="btn btn-primary flex-1" @click="searchCars">Поиск</button>
                <button class="btn btn-ghost" @click="resetFilters">Сбросить</button>
              </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
import SearchableSelect from '@/components/SearchableSelect.vue'
import api from '@/api'
export default {
  name: 'CarSearchPage',
  components: {
    CarCard,
    Pagination,
    SearchableSelect
  },
  data() {
    return {
      showDrawer: false,
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
    async loadBrandsAndModels() {
      try {
        const [brandsRes, modelsRes] = await Promise.all([
          api.get('/brands/'),
          api.get('/models/')
        ])
        
        this.brands = brandsRes.data
        this.models = modelsRes.data
      } catch (error) {
        console.error('Ошибка загрузки брендов и моделей:', error)
      }
    },
    async loadEnums() {
      try {
        const enumsPromises = {
          carConditions: api.get('/enums/car-conditions').then(r => r.data),
          steeringSides: api.get('/enums/steering-sides').then(r => r.data),
          bodyTypes: api.get('/enums/body-types').then(r => r.data),
          transmissions: api.get('/enums/transmissions').then(r => r.data),
          fuelTypes: api.get('/enums/fuel-types').then(r => r.data),
          driveTypes: api.get('/enums/drive-types').then(r => r.data)
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
        
        const response = await api.get(`/cars/?${queryString}`)
        const data = await response.data
        
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
      this.showDrawer = false
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
  created() {
    Promise.all([
      this.loadBrandsAndModels(),
      this.loadEnums()
    ]).then(() => {
      this.parseQueryParams()
      this.fetchCars()
    })
  }
}
</script>
