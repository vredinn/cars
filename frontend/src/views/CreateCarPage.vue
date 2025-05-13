<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-6">Создание объявления</h1>

    <form @submit.prevent="handleSubmit">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div
          class="bg-base-200 border-2 border-dashed rounded-box p-4 text-center transition"
          @dragover.prevent
          @drop.prevent="handleDrop"
        >
          <label class="label mb-2 block text-balance">Перетащите фото сюда или выберите файл</label>
          <input type="file" class="hidden" ref="fileInput" multiple @change="handleFiles">
          <button class="btn btn-primary" type="button" @click="$refs.fileInput.click()">Выбрать фото</button>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4" v-if="previews.length">
            <div v-for="(src, index) in previews" :key="index" class="flex flex-col">
              <img :src="src" class="rounded w-full h-32 object-cover border mb-2" />
              <button
                type="button"
                class="btn btn-error text-error-content rounded-full flex items-center justify-center"
                @click="removeImage(index)"
              >
                Удалить
              </button>
            </div>
          </div>
        </div>
        <div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label mb-2">Марка</label>
              <SearchableSelect
                v-model="form.brand_id"
                :options="brands"
                labelKey="name"
                valueKey="id"
                placeholder="Выберите марку"
              />
            </div>

            <div>
              <label class="label mb-2">Модель</label>
              <SearchableSelect
                v-model="form.model_id"
                :options="filteredModels"
                labelKey="name"
                valueKey="id"
                placeholder="Выберите модель"
                :disabled="!form.brand_id"
              />
            </div>

            <div>
              <label class="label mb-2">Год выпуска</label>
              <input type="number" min="1900" :max="currentYear" class="input input-bordered w-full" v-model="form.year" required>
            </div>

            <div>
              <label class="label mb-2">Цена</label>
              <input type="number" class="input input-bordered w-full" v-model="form.price" required>
            </div>
          </div>

          <!-- Характеристики -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label mb-2">Тип кузова</label>
              <SearchableSelect
                v-model="form.body_type"
                :options="bodyTypes"
                placeholder="Тип кузова"
              />
            </div>

            <div>
              <label class="label mb-2">Привод</label>
              <SearchableSelect
                v-model="form.drive_type"
                :options="driveTypes"
                placeholder="Тип привода"
              />
            </div>

            <div>
              <label class="label mb-2">КПП</label>
              <SearchableSelect
                v-model="form.transmission"
                :options="transmissions"
                placeholder="Коробка передач"
              />
            </div>

            <div>
              <label class="label mb-2">Тип топлива</label>
              <SearchableSelect
                v-model="form.fuel_type"
                :options="fuelTypes"
                placeholder="Тип топлива"
              />
            </div>

            <div>
              <label class="label mb-2">Сторона руля</label>
              <SearchableSelect
                v-model="form.steering_side"
                :options="steeringSides"
                placeholder="Сторона руля"
              />
            </div>

            <div>
              <label class="label mb-2">Состояние</label>
              <SearchableSelect
                v-model="form.car_condition"
                :options="carConditions"
                placeholder="Состояние автомобиля"
              />
            </div>
          </div>

          <!-- Двигатель и прочее -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label mb-2">Объем двигателя (л)</label>
              <input type="number" step="0.1" class="input input-bordered w-full" v-model="form.engine_capacity">
            </div>

            <div>
              <label class="label mb-2">Мощность (л.с.)</label>
              <input type="number" class="input input-bordered w-full" v-model="form.engine_power">
            </div>

            <div>
              <label class="label mb-2">Пробег (км)</label>
              <input type="number" class="input input-bordered w-full" v-model="form.mileage">
            </div>

            <div>
              <label class="label mb-2">Цвет</label>
              <input type="text" class="input input-bordered w-full" v-model="form.color">
            </div>
          </div>

          <!-- Геолокация -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="label mb-2">Широта</label>
              <input type="number" class="input input-bordered w-full" v-model="form.latitude">
            </div>
            <div>
              <label class="label mb-2">Долгота</label>
              <input type="number" class="input input-bordered w-full" v-model="form.longitude">
            </div>
          </div>

          <div>
            <label class="label mb-2">Описание</label>
            <textarea class="textarea textarea-bordered w-full p-4" rows="4" v-model="form.description"></textarea>
          </div>
        </div>
      </div>

      <!-- Кнопка -->
      <div class="pt-4">
        <button class="btn btn-primary w-full" type="submit" :disabled="loading">
          {{ loading ? 'Сохранение...' : 'Создать объявление' }}
        </button>
      </div>
    </form>
  </div>
    <div v-if="errorMessage" role="alert" class="alert alert-error alert-soft">
      <span>{{ errorMessage }}</span>
      <button @click="errorMessage=''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
    </div>
</template>

<script>
import SearchableSelect from '@/components/SearchableSelect.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
export default {
  name: 'CreateCarPage',
  components: { SearchableSelect },
  data() {
    return {
      loading: false,
      form: {
        brand_id: null,
        model_id: null,
        year: null,
        price: null,
        description: null,
        body_type: null,
        drive_type: null,
        transmission: null,
        fuel_type: null,
        steering_side: null,
        car_condition: null,
        engine_capacity: null,
        engine_power: null,
        mileage: null,
        color: null,
        latitude: null,
        longitude: null
      },
      files: [],
      brands: [],
      models: [],
      carConditions: [],
      steeringSides: [],
      bodyTypes: [],
      transmissions: [],
      fuelTypes: [],
      driveTypes: [],
      previews: [],
      errorMessage: ''
    }
  },
  computed: {
    filteredModels() {
      return this.models.filter(m => m.brand_id === this.form.brand_id)
    },
    user() {
      return useAuthStore().user
    },      
    currentYear() {
      return new Date().getFullYear()
    }
  },
  methods: {
    async loadData() {
      const [brandsRes, modelsRes] = await Promise.all([
        api.get('/brands/'),
        api.get('/models/')
      ])
      this.brands = brandsRes.data
      this.models = modelsRes.data

      const [c1, c2, c3, c4, c5, c6] = await Promise.all([
        api.get('/enums/car-conditions'),
        api.get('/enums/steering-sides'),
        api.get('/enums/body-types'),
        api.get('/enums/transmissions'),
        api.get('/enums/fuel-types'),
        api.get('/enums/drive-types')
      ])
      this.carConditions = c1.data
      this.steeringSides = c2.data
      this.bodyTypes = c3.data
      this.transmissions = c4.data
      this.fuelTypes = c5.data
      this.driveTypes = c6.data
    },
handleFiles(event) {
  const selectedFiles = Array.from(event.target.files)
  this.addFiles(selectedFiles)
},

handleDrop(event) {
  const droppedFiles = Array.from(event.dataTransfer.files)
  this.addFiles(droppedFiles)
},

addFiles(fileList) {
  for (const file of fileList) {
    if (!file.type.startsWith('image/')) continue
    this.files.push(file)
    this.previews.push(URL.createObjectURL(file))
  }
},

removeImage(index) {
  this.files.splice(index, 1)
  URL.revokeObjectURL(this.previews[index])
  this.previews.splice(index, 1)
},
    async handleSubmit() {
      this.loading = true
      try {
        const payload = {
          ...this.form,
          user_id: this.user.id
        }

        const { data } = await api.post('/cars/', payload)

        const carId = data.id
        const carUuid = data.uuid

        for (const file of this.files) {
          const formData = new FormData()
          formData.append('file', file)
          await api.post(`/car-images/?car_id=${carId}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
        }

        this.$router.push(`/car/${carUuid}`) // редирект на страницу авто
      } catch (error) {
        console.error('Ошибка создания:', error)
        this.errorMessage ='Не удалось создать объявление'
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    this.loadData()
  }
}
</script>
