<template>
  <div class="container mx-auto p-4 max-w-3xl">
    <h1 class="text-2xl font-bold mb-6">Создание объявления</h1>

    <form @submit.prevent="handleSubmit" class="grid gap-4">

      <!-- Базовая информация -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="label">Марка</label>
          <select class="select select-bordered w-full" v-model="form.brand_id" required>
            <option :value="null" disabled>Выберите марку</option>
            <option v-for="brand in brands" :value="brand.id" :key="brand.id">{{ brand.name }}</option>
          </select>
        </div>

        <div>
          <label class="label">Модель</label>
          <select class="select select-bordered w-full" v-model="form.model_id" required :disabled="!form.brand_id">
            <option :value="null" disabled>Выберите модель</option>
            <option v-for="model in filteredModels" :value="model.id" :key="model.id">{{ model.name }}</option>
          </select>
        </div>

        <div>
          <label class="label">Год выпуска</label>
          <input type="number" class="input input-bordered w-full" v-model="form.year" required>
        </div>

        <div>
          <label class="label">Цена</label>
          <input type="number" class="input input-bordered w-full" v-model="form.price" required>
        </div>
      </div>

      <!-- Характеристики -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="label">Тип кузова</label>
          <select class="select select-bordered w-full" v-model="form.body_type">
            <option v-for="val in bodyTypes" :value="val">{{ val }}</option>
          </select>
        </div>

        <div>
          <label class="label">Привод</label>
          <select class="select select-bordered w-full" v-model="form.drive_type">
            <option v-for="val in driveTypes" :value="val">{{ val }}</option>
          </select>
        </div>

        <div>
          <label class="label">КПП</label>
          <select class="select select-bordered w-full" v-model="form.transmission">
            <option v-for="val in transmissions" :value="val">{{ val }}</option>
          </select>
        </div>

        <div>
          <label class="label">Тип топлива</label>
          <select class="select select-bordered w-full" v-model="form.fuel_type">
            <option v-for="val in fuelTypes" :value="val">{{ val }}</option>
          </select>
        </div>

        <div>
          <label class="label">Сторона руля</label>
          <select class="select select-bordered w-full" v-model="form.steering_side">
            <option v-for="val in steeringSides" :value="val">{{ val }}</option>
          </select>
        </div>

        <div>
          <label class="label">Состояние</label>
          <select class="select select-bordered w-full" v-model="form.car_condition">
            <option v-for="val in carConditions" :value="val">{{ val }}</option>
          </select>
        </div>
      </div>

      <!-- Двигатель и прочее -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="label">Объем двигателя (л)</label>
          <input type="number" step="0.1" class="input input-bordered w-full" v-model="form.engine_capacity">
        </div>

        <div>
          <label class="label">Мощность (л.с.)</label>
          <input type="number" class="input input-bordered w-full" v-model="form.engine_power">
        </div>

        <div>
          <label class="label">Пробег (км)</label>
          <input type="number" class="input input-bordered w-full" v-model="form.mileage">
        </div>

        <div>
          <label class="label">Цвет</label>
          <input type="text" class="input input-bordered w-full" v-model="form.color">
        </div>
      </div>

      <!-- Геолокация -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="label">Широта</label>
          <input type="number" class="input input-bordered w-full" v-model="form.latitude">
        </div>
        <div>
          <label class="label">Долгота</label>
          <input type="number" class="input input-bordered w-full" v-model="form.longitude">
        </div>
      </div>

      <div>
        <label class="label">Описание</label>
        <textarea class="textarea textarea-bordered w-full" rows="4" v-model="form.description"></textarea>
      </div>

<!-- Drag & Drop фото -->
<div
  class="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:bg-gray-50 transition"
  @dragover.prevent
  @drop.prevent="handleDrop"
>
  <label class="label mb-2 block">Перетащите фото сюда или выберите файл</label>
  <input type="file" class="hidden" ref="fileInput" multiple @change="handleFiles">
  <button class="btn btn-sm" type="button" @click="$refs.fileInput.click()">Выбрать фото</button>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4" v-if="previews.length">
    <div v-for="(src, index) in previews" :key="index" class="relative">
      <img :src="src" class="rounded w-full h-32 object-cover border" />
      <button
        type="button"
        class="absolute top-0 right-0 bg-red-500 text-white rounded-full w-6 h-6 text-xs flex items-center justify-center"
        @click="removeImage(index)"
      >
        ✕
      </button>
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
</template>

<script>
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
export default {
  name: 'CreateCarPage',
  data() {
    return {
      loading: false,
      form: {
        brand_id: null,
        model_id: null,
        year: null,
        price: null,
        description: '',
        body_type: '',
        drive_type: '',
        transmission: '',
        fuel_type: '',
        steering_side: '',
        car_condition: '',
        engine_capacity: null,
        engine_power: null,
        mileage: null,
        color: '',
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
      previews: []
    }
  },
  computed: {
    filteredModels() {
      return this.models.filter(m => m.brand_id === this.form.brand_id)
    },
    user() {
      return useAuthStore().user
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
        alert('Не удалось создать объявление')
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
