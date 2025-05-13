<template>
  <section class="hero min-h-screen relative flex flex-col">
    <!-- Фоновое изображение -->
    <div class="hero-bg absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: 'url(/src/assets/i.webp)' }">
    </div>
    



    <!-- Основной контент -->
    <div
      class="container mx-auto hero-content w-full flex-1 flex flex-col items-center justify-center text-center">
      <div class="md:mb-8">
        <p class="text-xl text-white">СагРivot – ваш поворот к идеальному автомобилю. С нами вы найдете автомобиль своей мечты
          быстро и удобно!</p>
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

            <!-- Поле выбора состояния машины -->
        <SearchableSelect
                class="flex-1"
                :options="carConditions"
                v-model="filters.car_condition"
                placeholder="Состояние"
              />

            <!-- Поле выбора цены -->
            <div>
              <input type="number" class="input input-bordered w-full" v-model="filters.max_price" placeholder="Цена" min="50000">
            </div>

            <!-- Кнопка "Поиск" -->
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
    <div class="absolute bottom-0 left-0 w-full h-[200px] 
              bg-gradient-to-b from-transparent from-50% to-base-100 to-100%
              rounded-t-[50px] z-[1] pointer-events-none">
  </div>
  </section>
</template>

<script>
import SearchableSelect from '@/components/SearchableSelect.vue'
import api from '@/api'
export default {
  name: 'HeroSection',
  components: {SearchableSelect},
  data() {
    return {
      brands: [],
      models: [],
      carConditions: [],
      carPrice: null,
      filters: {
        brand_id: null,
        model_id: null,
        car_condition: null,
        max_price: null
      }
    }
  },
  computed: {
    filteredModels() {
      if (!this.filters.brand_id) return []
      return this.models.filter(model => model.brand_id === this.filters.brand_id)
    },
  },
  watch: {
    'filters.brand_id'(newVal) {
      if (!newVal) {
        this.filters.model_id = null
      }
    }
  },
  methods: {
    async loadBrandsAndModels() {
      try {
        const [brandsRes, modelsRes] = await Promise.all([
          api.get('/brands/'),
          api.get('/models/')
        ])
        
        this.brands = await brandsRes.data
        this.models = await modelsRes.data
      } catch (error) {
        console.error('Ошибка загрузки брендов и моделей:', error)
      }
    },
    async loadCarConditions() {
      try {
        this.carConditions = await api.get('/enums/car-conditions').then(r => r.data)
      } catch (error) {
        console.error('Ошибка загрузки состояний автомобиля:', error)
      }
    },
    buildQueryParams(filters) {
      const params = { ...filters }
      
      // Удаляем null/undefined значения
      Object.keys(params).forEach(key => {
        if (params[key] === null || params[key] === undefined || params[key] === '') {
          delete params[key]
        }
      })
      
      return params
    },
    searchCars() {
      // Копируем временные фильтры в активные
      const query = this.buildQueryParams(this.filters)
            
      this.$router.push({
        path: '/catalog',
        query: query
      }).catch(() => {})
    }
  },
  created() {
    this.loadBrandsAndModels()
    this.loadCarConditions()
  }
}
</script>