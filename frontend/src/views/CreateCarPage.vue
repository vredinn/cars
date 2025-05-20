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
          <input type="file" class="hidden" ref="fileInput" multiple @change="handleFiles" accept="image/*">
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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
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
          <!-- Карта -->
          <div class="mt-6">
            <h2 class="text-lg font-semibold mb-2">Укажите местоположение</h2>

            <yandex-map
      v-model="map"
      :settings="{
        location: {
          center: [37.617644, 55.755819],
          zoom: 9,
        },
      }"
  >
    <yandex-map-default-scheme-layer/>
    <yandex-map-default-features-layer/>
    <yandex-map-default-marker :settings="{ coordinates: [37.617644, 55.755819] }"/>
  </yandex-map>
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

<script setup>
import { ref, reactive, computed, onMounted, nextTick  } from 'vue'
import { useRouter } from 'vue-router'
import SearchableSelect from '@/components/SearchableSelect.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useFiltersStore } from '@/stores/filters'

import {
  YandexMap,
  YandexMapDefaultSchemeLayer,
  YandexMapDefaultFeaturesLayer,
  YandexMapDefaultMarker,
} from 'vue-yandex-maps';

const router = useRouter()
const authStore = useAuthStore()
const filtersStore = useFiltersStore()

const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  brand_id: null, model_id: null, year: null, price: null, description: null,
  body_type: null, drive_type: null, transmission: null, fuel_type: null,
  steering_side: null, car_condition: null, engine_capacity: null,
  engine_power: null, mileage: null, color: null,
  latitude: null, longitude: null
})

const files = ref([])
const previews = ref([])

const brands        = computed(() => filtersStore.brands)
const models        = computed(() => filtersStore.models)
const carConditions = computed(() => filtersStore.carConditions)
const steeringSides = computed(() => filtersStore.steeringSides)
const bodyTypes     = computed(() => filtersStore.bodyTypes)
const transmissions = computed(() => filtersStore.transmissions)
const fuelTypes     = computed(() => filtersStore.fuelTypes)
const driveTypes    = computed(() => filtersStore.driveTypes)

const currentYear = computed(() => new Date().getFullYear())
const filteredModels = computed(() =>
  models.value.filter(m => m.brand_id === form.brand_id)
)

// --- карта
const map = ref(null)
const initialCenter = [55.7558, 37.6176]  // Москва
const markerCoords = ref(null)

// по клику на карту ставим маркер
function onMapClick(event) {
  const coords = event.get('coords')      // [lat, lon]
  markerCoords.value = coords
  form.latitude  = coords[0]
  form.longitude = coords[1]
}

// по выбору из поиска тоже ставим маркер
function onSearchResult(event) {
  const feature = event.get('idx')          // индекс объекта
  map.value.getGeoObjects().getAll()[feature]
    .getGeometry()
    .getCoordinates()
    .then(([lon, lat]) => {
      // v3 search control возвращает [lon, lat]
      markerCoords.value = [lat, lon]
      form.latitude  = lat
      form.longitude = lon
      // смещаем центр карты
      map.value.setCenter(markerCoords.value)
    })
}


function handleFiles(event) {
  const selectedFiles = Array.from(event.target.files)
  if (!selectedFiles.length) {
    errorMessage.value = 'Не удалось выбрать файл. Попробуйте снова.'
    return
  }
  addFiles(selectedFiles)
}

function handleDrop(event) {
  event.preventDefault()
  const droppedFiles = Array.from(event.dataTransfer.files)
  addFiles(droppedFiles)
}

function addFiles(fileList) {
  for (const file of fileList) {
    if (!file.type.startsWith('image/')) continue
    files.value.push(file)
    previews.value.push(URL.createObjectURL(file))
  }
}

function removeImage(index) {
  files.value.splice(index, 1)
  URL.revokeObjectURL(previews.value[index])
  previews.value.splice(index, 1)
}

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''

  try {
    const payload = { ...form }
    const { data } = await api.post('/cars/', payload)

    const carId = data.id
    const carUuid = data.uuid

    for (const file of files.value) {
      const formData = new FormData()
      formData.append('file', file)
      await api.post(`/car-images/?car_id=${carId}`, formData)
    }

    router.push(`/car/${carUuid}`)
  } catch (error) {
    console.error('Ошибка создания:', error)
    errorMessage.value = 'Не удалось создать объявление'
  } finally {
    loading.value = false
  }
}

</script>

