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
import { ref, watch } from 'vue'

const emit = defineEmits<{
  (e: 'select-coords', payload: { lat: number; lng: number }): void
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

    suggestions.value = members.map((m: any) => {
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

function selectOption(item: { name: string; coords: [number, number] }) {
  search.value = item.name
  suggestions.value = []
  open.value = false

  emit('select-coords', { lng: item.coords[0], lat: item.coords[1] })
}
</script>
