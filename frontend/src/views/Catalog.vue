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

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CarCard from '@/components/CarCard.vue'
import Pagination from '@/components/Pagination.vue'
import SearchableSelect from '@/components/SearchableSelect.vue'

import { useFiltersStore } from '@/stores/filters'

import api from '@/api'

// Роуты
const route = useRoute()
const router = useRouter()
const filtersStore = useFiltersStore()

// Состояния
const showDrawer = ref(false)

const brands = computed(() => filtersStore.brands)
const models = computed(() => filtersStore.models)

const carConditions = computed(() => filtersStore.carConditions)
const steeringSides = computed(() => filtersStore.steeringSides)
const bodyTypes = computed(() => filtersStore.bodyTypes)
const transmissions = computed(() => filtersStore.transmissions)
const fuelTypes = computed(() => filtersStore.fuelTypes)
const driveTypes = computed(() => filtersStore.driveTypes)

const activeFilters = reactive({
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
})

const tempFilters = reactive({
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
})

const currentPage = ref(1)
const totalPages = ref(1)
const cars = ref([])
const isLoading = ref(false)

// Вычисляемые свойства
const filteredModels = computed(() => {
  if (!tempFilters.brand_id) return []
  return models.value.filter(model => model.brand_id === tempFilters.brand_id)
})

// Watchers
watch(() => tempFilters.brand_id, (newVal) => {
  if (!newVal) {
    tempFilters.model_id = null
  }
})

watch(route, () => {
  parseQueryParams()
  fetchCars()
}, { immediate: true })

// Методы
function formatPrice(price) {
  return new Intl.NumberFormat('ru-RU', { 
    style: 'currency', 
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(price)
}
function parseQueryParams() {
  const query = route.query

  currentPage.value = query.page ? parseInt(query.page) : 1

  Object.keys(activeFilters).forEach(key => {
    if (query[key] !== undefined) {
      if (query[key] === 'null') {
        activeFilters[key] = null
        tempFilters[key] = null
      } else if (key.startsWith('min_') || key.startsWith('max_') || key.endsWith('_id')) {
        activeFilters[key] = query[key] ? parseInt(query[key]) : null
        tempFilters[key] = query[key] ? parseInt(query[key]) : null
      } else {
        activeFilters[key] = query[key] || null
        tempFilters[key] = query[key] || null
      }
    } else {
      activeFilters[key] = null
      tempFilters[key] = null
    }
  })
}

function buildQueryParams(filters) {
  const params = { ...filters }

  Object.keys(params).forEach(key => {
    if (params[key] === null || params[key] === undefined || params[key] === '') {
      delete params[key]
    }
  })

  if (currentPage.value > 1) {
    params.page = currentPage.value
  }

  return params
}

async function fetchCars() {
  isLoading.value = true

  try {
    const queryParams = buildQueryParams(activeFilters)
    const queryString = new URLSearchParams(queryParams).toString()

    const response = await api.get(`/cars/?${queryString}`)
    const data = await response.data

    cars.value = data.items
    totalPages.value = data.pages
    currentPage.value = data.page
  } catch (error) {
    console.error('Ошибка загрузки автомобилей:', error)
    cars.value = []
  } finally {
    isLoading.value = false
  }
}

function searchCars() {
  Object.assign(activeFilters, { ...tempFilters })
  currentPage.value = 1
  updateRoute()
  showDrawer.value = false
}

function resetFilters() {
  Object.keys(tempFilters).forEach(key => {
    tempFilters[key] = null
  })

  if (Object.values(activeFilters).some(val => val !== null)) {
    Object.keys(activeFilters).forEach(key => {
      activeFilters[key] = null
    })

    currentPage.value = 1
    updateRoute()
  }
}

function changePage(page) {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  currentPage.value = page
  updateRoute()
}

function updateRoute() {
  const query = buildQueryParams(activeFilters)

  router.push({ query }).catch(() => {})
}

// Lifecycle
onMounted(async () => {
  parseQueryParams()
  fetchCars()
})
</script>

