<template>
  <div class="container mx-auto p-4">
    <div v-if="isLoadingFilters" class="flex justify-center items-center h-64">
      <div class="loading loading-spinner loading-lg"></div>
    </div>
    <div v-else>
      <h1 class="text-2xl font-bold mb-6">Редактирование объявления</h1>

      <form @submit.prevent="showSaveConfirmation">
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
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите марку автомобиля</div>
              </div>

              <div>
                <label class="label mb-2">Модель</label>
                <SearchableSelect
                  v-model="form.model_id"
                  :options="filteredModels"
                  labelKey="name"
                  valueKey="id"
                  placeholder="Выберите модель"
                  :disabled="!form.brand_id || loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите модель автомобиля</div>
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
                  className="validator"
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
                  className="validator"
                />
              </div>

              <div>
                <label class="label mb-2">Тип кузова</label>
                <SearchableSelect
                  v-model="form.body_type"
                  :options="bodyTypes"
                  placeholder="Тип кузова"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите тип кузова</div>
              </div>

              <div>
                <label class="label mb-2">Привод</label>
                <SearchableSelect
                  v-model="form.drive_type"
                  :options="driveTypes"
                  placeholder="Тип привода"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите тип привода</div>
              </div>

              <div>
                <label class="label mb-2">КПП</label>
                <SearchableSelect
                  v-model="form.transmission"
                  :options="transmissions"
                  placeholder="Коробка передач"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите тип коробки передач</div>
              </div>

              <div>
                <label class="label mb-2">Тип топлива</label>
                <SearchableSelect
                  v-model="form.fuel_type"
                  :options="fuelTypes"
                  placeholder="Тип топлива"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите тип топлива</div>
              </div>

              <div>
                <label class="label mb-2">Сторона руля</label>
                <SearchableSelect
                  v-model="form.steering_side"
                  :options="steeringSides"
                  placeholder="Сторона руля"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите сторону руля</div>
              </div>

              <div>
                <label class="label mb-2">Состояние</label>
                <SearchableSelect
                  v-model="form.car_condition"
                  :options="carConditions"
                  placeholder="Состояние автомобиля"
                  :disabled="loading"
                  required
                />
                <div class="validator-hint hidden mt-0">Выберите состояние автомобиля</div>
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
                  className="validator"
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
                  className="validator"
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
                  className="validator"
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
            <!-- Карта -->
            <div class="mb-2">
              <label class="label mb-2">Местоположение</label>
              <div>
                <AddressSearch
                  @selected="onAddressSelected"
                  :latitude="form.latitude"
                  :longitude="form.longitude"
                  :disabled="loading"
                  v-model="isAddressValid"
                />
              </div>
            </div>
            <div>
              <label class="label mb-2">Описание</label>
              <textarea
                class="textarea textarea-bordered validator w-full p-4"
                rows="4"
                v-model="form.description"
                :disabled="loading"
                minlength="10"
                maxlength="2000"
                required
              ></textarea>
              <div class="validator-hint hidden mt-0">Описание должно содержать от 10 до 2000 символов</div>
            </div>
          </div>
        </div>

        <div class="pt-4">
          <div v-if="errorMessage" role="alert" class="alert alert-error alert-soft mb-2">
            <span>{{ errorMessage }}</span>
            <button @click="errorMessage = ''" class="btn btn-sm btn-circle btn-ghost ml-auto">✕</button>
          </div>
          <div class="flex flex-row gap-4">
            <button class="btn btn-primary flex-1 leading-4" type="submit" :disabled="loading || !isFormValid">
              {{ loading ? 'Сохранение...' : 'Сохранить изменения' }}
            </button>
            <button class="btn btn-error flex-1 leading-4" type="button" @click="showDeleteConfirmation" :disabled="loading">
              {{ loading ? 'Удаление...' : 'Удалить объявление' }}
            </button>
          </div>
        </div>
      </form>
    </div>

    <dialog id="save-modal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box">
        <h3 class="font-bold text-lg mb-4">Сохранение изменений</h3>
        <p>Вы уверены, что хотите сохранить изменения в объявлении?</p>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn" @click="closeSaveModal">Отмена</button>
            <button class="btn btn-primary" @click="handleSubmit">Сохранить</button>
          </form>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>закрыть</button>
      </form>
    </dialog>

    <dialog id="delete-modal" class="modal modal-bottom sm:modal-middle">
      <div class="modal-box">
        <h3 class="font-bold text-lg text-error mb-4">Удаление объявления</h3>
        <p>Вы уверены, что хотите удалить это объявление? Это действие нельзя отменить.</p>
        <div class="modal-action">
          <form method="dialog" class="flex gap-2">
            <button class="btn" @click="closeDeleteModal">Отмена</button>
            <button class="btn btn-error" @click="handleDelete">Удалить</button>
          </form>
        </div>
      </div>
      <form method="dialog" class="modal-backdrop">
        <button>закрыть</button>
      </form>
    </dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SearchableSelect from '@/components/SearchableSelect.vue'
import AddressSearch from '@/components/AddressSearch.vue'
import NumberInput from '@/components/NumberInput.vue'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import { useFiltersStore } from '@/stores/filters'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const filtersStore = useFiltersStore()

const loading = ref(false)
const isLoadingFilters = ref(true)
const errorMessage = ref('')
const isAddressValid = ref(false)

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
const existingImages = ref([]) 

const brands = computed(() => filtersStore.brands)
const models = computed(() => filtersStore.models)
const carConditions = computed(() => filtersStore.carConditions)
const steeringSides = computed(() => filtersStore.steeringSides)
const bodyTypes = computed(() => filtersStore.bodyTypes)
const transmissions = computed(() => filtersStore.transmissions)
const fuelTypes = computed(() => filtersStore.fuelTypes)
const driveTypes = computed(() => filtersStore.driveTypes)

const currentYear = computed(() => new Date().getFullYear())
const filteredModels = computed(() => models.value.filter(m => m.brand_id === form.brand_id))

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

async function loadFilters() {
  try {
    await filtersStore.loadAll()
    isLoadingFilters.value = false
  } catch (error) {
    console.error('Ошибка загрузки фильтров:', error)
    errorMessage.value = 'Не удалось загрузить фильтры'
    isLoadingFilters.value = false
  }
}

async function loadCarData(carUUID) {
  try {
    const response = await api.get(`/cars/${carUUID}`)
    const data = response.data
    Object.assign(form, {
      brand_id: data.brand_id,
      model_id: data.model_id,
      year: data.year,
      price: typeof data.price === 'string' ? parseInt(data.price) : data.price,
      description: data.description || '',
      body_type: data.body_type,
      drive_type: data.drive_type,
      transmission: data.transmission,
      fuel_type: data.fuel_type,
      steering_side: data.steering_side,
      car_condition: data.car_condition,
      engine_capacity: data.engine_capacity,
      engine_power: data.engine_power,
      mileage: data.mileage,
      color: data.color,
      latitude: data.latitude,
      longitude: data.longitude
    })
    if (data.latitude && data.longitude) {
      isAddressValid.value = true
    }
    if (data.images && data.images.length > 0) {
      existingImages.value = data.images.map(img => ({
        id: img.id,
        url: img.image_url
      }))
      previews.value = data.images.map(img => img.image_url)
    }
    if (authStore.user && authStore.user.uuid) {
      const ownRes = await api.get(`/cars/check_ownership/${carUUID}/${authStore.user.uuid}`)
      if (!ownRes.data && !authStore.user.is_admin) {
        errorMessage.value = 'У вас нет прав для редактирования этого объявления'
        router.push(`/car/${carUUID}`)
      }
    } else {
      errorMessage.value = 'Войдите в систему для редактирования'
      router.push('/login')
    }
  } catch (error) {
    console.error('Ошибка загрузки данных автомобиля:', error)
    errorMessage.value = 'Не удалось загрузить данные автомобиля'
  }
}

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
    if (!file.type.startsWith('image/')) {
      errorMessage.value = 'Поддерживаются только изображения'
      continue
    }
    if (previews.value.length >= 30) {
      errorMessage.value = 'Максимум 30 изображений'
      return
    }
    files.value.push(file)
    previews.value.push(URL.createObjectURL(file))
  }
}

function removeImage(index) {
  if (index < existingImages.value.length) {
    existingImages.value.splice(index, 1)
  } else {
    const fileIndex = index - existingImages.value.length
    files.value.splice(fileIndex, 1)
    URL.revokeObjectURL(previews.value[index])
  }
  previews.value.splice(index, 1)
}

function showSaveConfirmation(e) {
  e.preventDefault()
  if (!isFormValid.value) {
    errorMessage.value = 'Пожалуйста, заполните все обязательные поля корректно'
    return
  }
  
  const modal = document.getElementById('save-modal')
  modal?.showModal()
}

function closeSaveModal() {
  const modal = document.getElementById('save-modal')
  modal?.close()
}

function showDeleteConfirmation() {
  const modal = document.getElementById('delete-modal')
  modal?.showModal()
}

function closeDeleteModal() {
  const modal = document.getElementById('delete-modal')
  modal?.close()
}

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''
  closeSaveModal()

  try {
    const carUUID = route.params.uuid
    const payload = { ...form }
    await api.put(`/cars/${carUUID}`, payload)

    const existingImageIds = existingImages.value.map(img => img.id)
    const originalImageIds = (await api.get(`/cars/${carUUID}`)).data.images.map(img => img.id)
    const imagesToDelete = originalImageIds.filter(id => !existingImageIds.includes(id))
    for (const imageId of imagesToDelete) {
      await api.delete(`/car-images/${imageId}`)
    }

    for (const file of files.value) {
      const formData = new FormData()
      formData.append('file', file)
      await api.post(`/car-images/?car_uuid=${carUUID}`, formData)
    }

    router.push(`/car/${carUUID}`)
  } catch (error) {
    console.error('Ошибка обновления:', error)
    errorMessage.value = error.response?.data?.detail || 'Не удалось обновить объявление'
  } finally {
    loading.value = false
  }
}

function validateForm() {
  if (!isFormValid.value) {
    if (!form.brand_id || !form.model_id) {
      errorMessage.value = 'Выберите марку и модель автомобиля'
    } else if (!form.year || form.year < 1900 || form.year > currentYear.value) {
      errorMessage.value = `Год выпуска должен быть между 1900 и ${currentYear.value}`
    } else if (!form.price || form.price <= 0) {
      errorMessage.value = 'Укажите корректную цену'
    } else if (!form.body_type) {
      errorMessage.value = 'Выберите тип кузова'
    } else if (!form.drive_type) {
      errorMessage.value = 'Выберите тип привода'
    } else if (!form.transmission) {
      errorMessage.value = 'Выберите тип коробки передач'
    } else if (!form.fuel_type) {
      errorMessage.value = 'Выберите тип топлива'
    } else if (!form.steering_side) {
      errorMessage.value = 'Выберите сторону руля'
    } else if (!form.car_condition) {
      errorMessage.value = 'Выберите состояние автомобиля'
    } else if (!form.engine_capacity || form.engine_capacity < 0.1 || form.engine_capacity > 10.0) {
      errorMessage.value = 'Объем двигателя должен быть от 0.1 до 10.0 литров'
    } else if (!form.engine_power || form.engine_power < 1 || form.engine_power > 2000) {
      errorMessage.value = 'Мощность должна быть от 1 до 2000 л.с.'
    } else if (!form.mileage || form.mileage < 0) {
      errorMessage.value = 'Пробег не может быть отрицательным'
    } else if (!form.color || form.color.length < 2 || form.color.length > 50) {
      errorMessage.value = 'Цвет должен содержать от 2 до 50 символов'
    } else if (form.description && (form.description.length < 10 || form.description.length > 2000)) {
      errorMessage.value = 'Описание должно содержать от 10 до 2000 символов'
    } else if (!isAddressValid.value) {
      errorMessage.value = 'Выберите местоположение из списка'
    }
    return false
  }
  return true
}

async function handleDelete() {
  loading.value = true
  errorMessage.value = ''
  closeDeleteModal()

  try {
    const carUUID = route.params.uuid
    await api.delete(`/cars/${carUUID}`)
    router.push('/')
  } catch (error) {
    console.error('Ошибка удаления:', error)
    errorMessage.value = error.response?.data?.detail || 'Не удалось удалить объявление'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  isLoadingFilters.value = true
  await loadFilters()
  if (!isLoadingFilters.value) {
    const carUUID = route.params.uuid
    await loadCarData(carUUID)
  }
})
</script>