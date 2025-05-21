<template>
    {{ address || 'Загрузка адреса...' }}
</template>

<script lang="ts" setup>
import { ref, watch, shallowRef } from 'vue'

const props = defineProps<{
  lat: number
  lng: number
}>()

const address = ref<string | null>(null)

const API_KEY = '249a7a27-d3cf-46ac-8920-d1f2c656a79b'

async function fetchAddress() {
  const url = `https://geocode-maps.yandex.ru/1.x/?format=json&apikey=${API_KEY}&geocode=${props.lng},${props.lat}&kind=locality&results=1`
  try {
    const response = await fetch(url)
    const data = await response.json()
    const components = data.response.GeoObjectCollection.featureMember
    const city = components?.[0]?.GeoObject?.name
    address.value = city || 'Город не найден'
  } catch (e) {
    console.error('Ошибка геокодирования:', e)
    address.value = 'Ошибка загрузки адреса'
  }
}

watch(() => [props.lat, props.lng], fetchAddress, { immediate: true })
</script>
