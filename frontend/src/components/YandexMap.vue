<template>
  <div>
    <div id="map" style="width: 100%; height: 400px;"></div>
    <p class="mt-2">Адрес: {{ address }}</p>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'

const emit = defineEmits(['update:location'])

const latitude = ref(55.751244)
const longitude = ref(37.618423)
const address = ref('')

onMounted(() => {
  ymaps.ready(init)
})

function init() {
  const map = new ymaps.Map('map', {
    center: [latitude.value, longitude.value],
    zoom: 10,
  })

  const placemark = new ymaps.Placemark(map.getCenter(), {}, {
    draggable: true
  })

  map.geoObjects.add(placemark)

  getAddressFromCoords(...map.getCenter())

  placemark.events.add('dragend', () => {
    const coords = placemark.geometry.getCoordinates()
    latitude.value = coords[0]
    longitude.value = coords[1]
    emit('update:location', { latitude: coords[0], longitude: coords[1] })
    getAddressFromCoords(...coords)
  })
}

function getAddressFromCoords(lat, lon) {
  ymaps.geocode([lat, lon]).then(res => {
    const firstGeoObject = res.geoObjects.get(0)
    address.value = firstGeoObject?.getAddressLine() || 'Адрес не найден'
  })
}
</script>
