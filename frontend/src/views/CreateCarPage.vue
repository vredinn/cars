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
                required
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
                required
              />
            </div>

            <div>
              <label class="label mb-2">Год выпуска</label>
              <NumberInput
                v-model="form.year"
                :min="1900"
                :max="currentYear"
                :step="1"
                required
                :validator-hint="`Год должен быть между 1900 и ${currentYear}`"
              />
            </div>

            <div>
              <label class="label mb-2">Цена</label>
              <NumberInput
                v-model="form.price"
                :min="1"
                :step="1"
                required
                validator-hint="Цена должна быть положительным числом"
              />
            </div>

            <div>
              <label class="label mb-2">Тип кузова</label>
              <SearchableSelect
                v-model="form.body_type"
                :options="bodyTypes"
                placeholder="Тип кузова"
                required
              />
            </div>

            <div>
              <label class="label mb-2">Привод</label>
              <SearchableSelect
                v-model="form.drive_type"
                :options="driveTypes"
                placeholder="Тип привода"
                required
              />
            </div>

            <div>
              <label class="label mb-2">КПП</label>
              <SearchableSelect
                v-model="form.transmission"
                :options="transmissions"
                placeholder="Коробка передач"
                required
              />
            </div>

            <div>
              <label class="label mb-2">Тип топлива</label>
              <SearchableSelect
                v-model="form.fuel_type"
                :options="fuelTypes"
                placeholder="Тип топлива"
                required
              />
            </div>

            <div>
              <label class="label mb-2">Сторона руля</label>
              <SearchableSelect
                v-model="form.steering_side"
                :options="steeringSides"
                placeholder="Сторона руля"
                required
              />
            </div>

            <div>
              <label class="label mb-2">Состояние</label>
              <SearchableSelect
                v-model="form.car_condition"
                :options="carConditions"
                placeholder="Состояние автомобиля"
                required
              />
            </div>

            <div>
              <label class="label mb-2">Объем двигателя (л)</label>
              <NumberInput
                v-model="form.engine_capacity"
                :min="0.1"
                :max="10.0"
                :step="0.1"
                required
                validator-hint="Объем двигателя должен быть от 0.1 до 10.0 литров"
              />
            </div>

            <div>
              <label class="label mb-2">Мощность (л.с.)</label>
              <NumberInput
                v-model="form.engine_power"
                :min="1"
                :max="2000"
                :step="1"
                required
                validator-hint="Мощность должна быть от 1 до 2000 л.с."
              />
            </div>

            <div>
              <label class="label mb-2">Пробег (км)</label>
              <NumberInput
                v-model="form.mileage"
                :min="0"
                :step="1"
                required
                validator-hint="Пробег не может быть отрицательным"
              />
            </div>

            <div>
              <label class="label mb-2">Цвет</label>
              <label class="input validator w-full">
                <input 
                  type="text" 
                  class="w-full" 
                  v-model="form.color"
                  required
                  minlength="2"
                  maxlength="50"
                  pattern="[A-Za-zА-Яа-яЁё\- ]+"
                >
              </label>
              <div class="validator-hint hidden mt-0">Цвет должен содержать от 2 до 50 символов, только буквы, пробелы и дефис</div>
            </div>
          </div>
          <div class="mb-2">
            <label class="label mb-2">Местоположение</label>
            <div>                
              <AddressSearch 
                @selected="onAddressSelected" 
                v-model="isAddressValid"
              />
            </div>         
          </div>
          <div>
            <label class="label mb-2">Описание</label>
              <textarea 
                class="textarea validator textarea-bordered w-full p-4" 
                rows="4" 
                v-model="form.description"
                minlength="10"
                maxlength="2000"
                required
              ></textarea>
            <div class="validator-hint hidden mt-0">Описание должно содержать от 10 до 2000 символов</div>
          </div>
        </div>
      </div>

      <div class="pt-4">        
        <div v-if="errorMessage" role="alert" class="alert alert-error alert-soft">
          <span>{{ errorMessage }}</span>
          <button @click="errorMessage=''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
        </div>
        <button class="btn btn-primary w-full" type="submit" :disabled="loading || !isFormValid">
          {{ loading ? 'Сохранение...' : 'Создать объявление' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import SearchableSelect from '@/components/SearchableSelect.vue'
import AddressSearch from '@/components/AddressSearch.vue'
import NumberInput from '@/components/NumberInput.vue'

import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useFiltersStore } from '@/stores/filters'

const router = useRouter()
const authStore = useAuthStore()
const filtersStore = useFiltersStore()

const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
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
})

const files = ref([])
const previews = ref([])
const isAddressValid = ref(false)

const brands = computed(() => filtersStore.brands)
const models = computed(() => filtersStore.models)
const carConditions = computed(() => filtersStore.carConditions)
const steeringSides = computed(() => filtersStore.steeringSides)
const bodyTypes = computed(() => filtersStore.bodyTypes)
const transmissions = computed(() => filtersStore.transmissions)
const fuelTypes = computed(() => filtersStore.fuelTypes)
const driveTypes = computed(() => filtersStore.driveTypes)

const currentYear = computed(() => new Date().getFullYear())
const filteredModels = computed(() =>
  models.value.filter(m => m.brand_id === form.brand_id)
)

const isFormValid = computed(() => {
  return (
    form.brand_id &&
    form.model_id &&
    form.year >= 1900 && form.year <= currentYear.value + 1 &&
    form.price > 0 &&
    form.body_type &&
    form.drive_type &&
    form.transmission &&
    form.fuel_type &&
    form.steering_side &&
    form.car_condition &&
    form.engine_capacity >= 0.1 && form.engine_capacity <= 10.0 &&
    form.engine_power >= 1 && form.engine_power <= 2000 &&
    form.mileage >= 0 &&
    form.color?.length >= 2 && form.color?.length <= 50 &&
    (!form.description || (form.description.length >= 10 && form.description.length <= 2000)) &&
    isAddressValid.value
  )
})

function onAddressSelected({ latitude, longitude }) {
  form.latitude = latitude;
  form.longitude = longitude;
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
  if (!isFormValid.value) {
    errorMessage.value = 'Пожалуйста, заполните все обязательные поля корректно'
    return
  }

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
      await api.post(`/car-images/?car_uuid=${carUuid}`, formData)
    }

    router.push(`/car/${carUuid}`)
  } catch (error) {
    console.error('Ошибка создания:', error)
    errorMessage.value = error.response?.data?.detail || 'Не удалось создать объявление'
  } finally {
    loading.value = false
  }
}
</script>


