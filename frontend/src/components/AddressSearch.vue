<template>
  <div class="relative w-full" ref="root">
    <div class="relative">
      <label :class="['input validator w-full', {'input-error': showError}]">
        <input
          v-model="search"
          autocomplete="off"
          placeholder="Название населенного пункта"
          type="text"
          class="w-full"
          @focus="handleFocus"
          @blur="handleBlur"
          @input="handleInput"
          :disabled="disabled"
          required
        />
      </label>

      <!-- Выпадающий список -->
      <div
        v-if="open"
        class="absolute left-0 right-0 z-20"
        style="top: 100%"
      >
        <ul class="bg-base-300 border border-base-100 rounded-box max-h-60 overflow-auto shadow-lg">
          <li
            v-if="suggestions.length === 0 && search.trim() !== ''"
            class="py-2 px-4 text-center text-base-content/50"
          >
            Ничего не найдено
          </li>

          <li
            v-for="(item, index) in suggestions"
            :key="index"
            @mousedown.prevent="selectOption(item)"
            :class="[
              'py-2 px-4 hover:bg-base-200 cursor-pointer',
              index !== 0 ? 'border-t border-base-100' : ''
            ]"
          >
            {{ item.name }}
          </li>
        </ul>
      </div>

      <!-- Сообщение об ошибке -->
      <div 
        v-if="showError" 
        class="validator-hint text-xs text-error mt-1"
      >
        {{ validationMessage }}
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted, computed } from 'vue'

const API_KEY = '249a7a27-d3cf-46ac-8920-d1f2c656a79b'

const emit = defineEmits<{
  (e: 'selected', payload: { latitude: number | null; longitude: number | null }): void
  (e: 'update:modelValue', value: boolean): void
}>()

const props = defineProps<{
  latitude?: number
  longitude?: number
  disabled?: boolean
  modelValue?: boolean
}>()

const root = ref<HTMLDivElement | null>(null)
const search = ref('')
const suggestions = ref<{ name: string; coords: [number, number] }[]>([])
const open = ref(false)
const isValidSelection = ref(false)
const isDirty = ref(false)

const hasError = computed(() => {
  if (!isDirty.value) return false
  return !isValidSelection.value
})

const validationMessage = computed(() => {
  if (!isDirty.value) return ''
  if (!isValidSelection.value) {
    return 'Выберите город из списка'
  }
  return ''
})

const showError = computed(() => {
  return hasError.value && !open.value && isDirty.value
})

// Debounce search
let searchTimeout: ReturnType<typeof setTimeout> | null = null

function handleInput() {
  // При любом изменении текста сбрасываем валидацию и координаты
  isValidSelection.value = false
  isDirty.value = false // Сбрасываем dirty state при вводе
  emit('update:modelValue', false)
  emit('selected', { latitude: null, longitude: null })

  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  searchTimeout = setTimeout(() => {
    performSearch(search.value)
  }, 300)
}

function handleFocus() {
  open.value = true
  if (search.value && !isValidSelection.value) {
    isDirty.value = true
    performSearch(search.value)
  }
}

function handleBlur() {
  setTimeout(() => {
    open.value = false
    if (search.value && !isValidSelection.value) {
      isDirty.value = true // Устанавливаем dirty state только при потере фокуса
      search.value = ''
      emit('update:modelValue', false)
      emit('selected', { latitude: null, longitude: null })
    }
  }, 200)
}

async function performSearch(query: string) {
  if (!query.trim()) {
    suggestions.value = []
    return
  }

  try {
    const url = `https://geocode-maps.yandex.ru/1.x/?format=json&apikey=${API_KEY}&geocode=${encodeURIComponent(
      query
    )}&kind=locality&results=5`

    const response = await fetch(url)
    const data = await response.json()
    const members = data.response.GeoObjectCollection.featureMember

    suggestions.value = members
      .filter((m: any) => {
        const kind =
          m.GeoObject?.metaDataProperty?.GeocoderMetaData?.kind || ''
        return kind === 'locality'
      })
      .map((m: any) => {
        const geo = m.GeoObject
        const name = geo.name
        const pos = geo.Point.pos.split(' ')
        return {
          name,
          coords: [parseFloat(pos[0]), parseFloat(pos[1])],
        }
      })
  } catch (e) {
    console.error('Ошибка геокодирования:', e)
    suggestions.value = []
  }
}

async function reverseGeocode(lat: number, lon: number): Promise<string> {
  const url = `https://geocode-maps.yandex.ru/1.x/?format=json&apikey=${API_KEY}&geocode=${lon},${lat}&kind=locality&results=1`
  try {
    const response = await fetch(url)
    const data = await response.json()
    const member = data.response.GeoObjectCollection.featureMember[0]
    if (member) return member.GeoObject.name || ''
  } catch (e) {
    console.error('Ошибка обратного геокодирования:', e)
  }
  return ''
}

onMounted(async () => {
  if (props.latitude && props.longitude) {
    const name = await reverseGeocode(props.latitude, props.longitude)
    if (name) {
      search.value = name
      isValidSelection.value = true
      emit('update:modelValue', true)
    }
  }
})

watch(
  () => [props.latitude, props.longitude],
  async ([lat, lon]) => {
    if (lat && lon) {
      const name = await reverseGeocode(lat, lon)
      if (name) {
        search.value = name
        isValidSelection.value = true
        emit('update:modelValue', true)
      }
    } else {
      search.value = ''
      isValidSelection.value = false
      emit('update:modelValue', false)
    }
  }
)

function selectOption(item: { name: string; coords: [number, number] }) {
  search.value = item.name
  suggestions.value = []
  open.value = false
  isValidSelection.value = true
  isDirty.value = true
  emit('update:modelValue', true)
  emit('selected', { latitude: item.coords[1], longitude: item.coords[0] })
}
</script>
