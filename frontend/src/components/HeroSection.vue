<template>
  <section class="hero min-h-screen relative flex flex-col">
    <!-- Фоновое изображение -->
    <div
      class="hero-bg absolute inset-0 bg-cover bg-center"
      :style="{ backgroundImage: 'url(/src/assets/i.webp)' }"
    ></div>

    <!-- Основной контент -->
    <div
      class="container mx-auto hero-content w-full flex-1 flex flex-col items-center justify-center text-center"
    >
      <div class="md:mb-8">
        <p class="text-xl text-white">
          СагРivot – ваш поворот к идеальному автомобилю. С нами вы найдете
          автомобиль своей мечты быстро и удобно!
        </p>
        <h2 class="text-5xl font-bold text-white">Найдите свой идеальный автомобиль</h2>
      </div>

      <!-- Поисковая форма -->
      <div class="container mx-auto">
        <div class="w-full rounded-[20px] lg:rounded-full p-1 bg-base-100">
          <div class="flex flex-col md:flex-row gap-3">
            <SearchableSelect
              class="flex-1"
              :options="brands"
              v-model="filters.brand_id"
              placeholder="Марка"
              label-key="name"
              value-key="id"
            />

            <SearchableSelect
              class="flex-1"
              :options="filteredModels"
              v-model="filters.model_id"
              placeholder="Модель"
              label-key="name"
              value-key="id"
              :disabled="!filters.brand_id"
            />

            <SearchableSelect
              class="flex-1"
              :options="carConditions"
              v-model="filters.car_condition"
              placeholder="Состояние"
            />

            <div>
              <input
                type="number"
                class="input input-bordered w-full"
                v-model="filters.max_price"
                placeholder="Цена"
                min="50000"
              />
            </div>

            <button class="btn btn-primary flex items-center" @click="searchCars">
              <svg class="w-3 h-3 fill-primary-content">
                <use href="#icon_search"></use>
              </svg>
              Поиск
            </button>
          </div>
        </div>
      </div>
    </div>

    <div
      class="absolute bottom-0 left-0 w-full h-[200px] bg-gradient-to-b from-transparent from-50% to-base-100 to-100% rounded-t-[50px] pointer-events-none"
    ></div>
  </section>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFiltersStore } from '@/stores/filters'

import SearchableSelect from '@/components/SearchableSelect.vue'

const filtersStore = useFiltersStore()

const router = useRouter()

const brands = computed(() => filtersStore.brands)
const models = computed(() => filtersStore.models)
const carConditions = computed(() => filtersStore.carConditions)

const filters = reactive({
  brand_id: null,
  model_id: null,
  car_condition: null,
  max_price: null,
})

// Фильтрация моделей по выбранной марке
const filteredModels = computed(() => {
  if (!filters.brand_id) return []
  return models.value.filter(model => model.brand_id === filters.brand_id)
})

// Если бренд сброшен, сбрасываем модель
watch(() => filters.brand_id, (newVal) => {
  if (!newVal) {
    filters.model_id = null
  }
})

// Формируем параметры запроса без null и пустых значений
const buildQueryParams = (filters) => {
  const params = { ...filters }
  Object.keys(params).forEach(key => {
    if (params[key] === null || params[key] === undefined || params[key] === '') {
      delete params[key]
    }
  })
  return params
}

// Поиск — переход на /catalog с параметрами
const searchCars = () => {
  const query = buildQueryParams(filters)
  router.push({ path: '/catalog', query }).catch(() => {})
}
</script>
