<template>
  <div class="relative w-full">
    <input
      v-model="search"
      autocomplete="off"
      placeholder="Название населенного пункта"
      type="text"
      class="input input-bordered w-full"
      @focus="open = true"
      @blur="handleBlur"
    />

    <ul
      v-if="open"
      class="absolute z-10 w-full bg-base-300 border-1 border-base-100 rounded-box max-h-60 overflow-auto mt-1"
    >
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
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'

const emit = defineEmits<{
  (e: 'selected', payload: { latitude: number; longitude: number }): void
}>()

const props = defineProps<{
  latitude?: number
  longitude?: number
}>()

const search = ref('')
const suggestions = ref<{ name: string; coords: [number, number] }[]>([])
const open = ref(false)

const API_KEY = '249a7a27-d3cf-46ac-8920-d1f2c656a79b'

function handleBlur() {
  setTimeout(() => (open.value = false), 200)
}

watch(search, async val => {
  if (!val.trim()) {
    suggestions.value = []
    return
  }

  const url = `https://geocode-maps.yandex.ru/1.x/?format=json&apikey=${API_KEY}&geocode=${encodeURIComponent(
    val
  )}&kind=locality&results=5`

  try {
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
})

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

// при старте
onMounted(async () => {
  if (props.latitude && props.longitude) {
    const name = await reverseGeocode(props.latitude, props.longitude)
    if (name) search.value = name
  }
})

// и при изменении координат (если нужно)
watch(
  () => [props.latitude, props.longitude],
  async ([lat, lon]) => {
    if (lat && lon) {
      const name = await reverseGeocode(lat, lon)
      if (name) search.value = name
    }
  }
)

function selectOption(item: { name: string; coords: [number, number] }) {
  search.value = item.name
  suggestions.value = []
  open.value = false

  emit('selected', { latitude: item.coords[1], longitude: item.coords[0] })
}
</script>
