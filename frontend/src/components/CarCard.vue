<template>
  <div @click="goToCar(car.uuid)" class="card bg-base-300 cursor-pointer">
    <div class="card-body p-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <div class="w-full lg:w-1/4">
          <img 
            :src="car.preview_image_url" 
            class="w-full h-52 object-cover rounded-box"
            :alt="`${car.brand_name} ${car.model_name}`"
          />
        </div>

        <div class="w-full lg:w-3/4">
          <h3 class="card-title">{{ car.brand_name }} {{ car.model_name }} - {{ car.year }} г.</h3>
          <p>
            {{ car.engine_power }} л.с. {{ car.fuel_type }}, {{ car.engine_capacity }} л, 
            {{ car.steering_side }} руль, {{ car.drive_type }} привод
          </p>
          <div class="mt-2">
            <span class="text-xl font-bold">{{ formatPrice(car.price) }}</span>
          </div>

          <div class="flex flex-wrap gap-2 mt-2">
            <span class="badge badge-outline">{{ car.transmission }}</span>
            <span class="badge badge-outline">{{ car.body_type }}</span>
            <span class="badge badge-outline">{{ car.car_condition }}</span>
            <span class="badge badge-outline">{{ car.mileage }} км</span>
            <span class="badge badge-outline">{{ car.color }} цвет</span>
            <span class="badge badge-outline">{{ car.drive_type }} привод</span>
          </div>

          <div class="card-actions justify-end mt-4">
            <div v-if="isOwner" class="badge badge-lg h-10 badge-outline">
              Ваше объявление
            </div>
            <div v-else>
              <div v-if="!isFavorite" class="tooltip tooltip-left" data-tip="Добавить в избранное">
                <button @click.stop="toggleFavorite" v-if="user" class="btn btn-accent p-2">
                  <svg class="w-4 h-4 fill-accent-content">
                    <use href="#icon_favorite" />
                  </svg>
                  В избранное
                </button>
              </div>
              <div v-if="isFavorite" class="tooltip tooltip-left" data-tip="Удалить из избранного">
                <button @click.stop="toggleFavorite" v-if="user" class="btn btn-secondary p-2">
                  <svg class="w-4 h-4 fill-secondary-content">
                    <use href="#icon_favorite" />
                  </svg>
                  Уже в избранном
                </button>
              </div>
            </div>
            <router-link :to="`/car/${car.uuid}`" class="btn btn-primary" @click.stop>Подробнее</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

// Получаем пропсы
const props = defineProps({
  car: Object
})

const car = props.car // добавляем эту строку, чтобы обращаться к car напрямую

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const isFavorite = ref(false)
const isOwner = ref(false)

// Методы
function goToCar(uuid) {
  router.push(`/car/${uuid}`)
}

function formatPrice(price) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0
  }).format(price)
}

async function checkFavorite() {
  if (!user.value) return

  try {
    const favRes = await api.get(`/favorites/check/${user.value.uuid}/${car.uuid}`)
    isFavorite.value = favRes.data
  } catch (error) {
    console.error(error)
  }

  try {
    const ownRes = await api.get(`/cars/check_ownership/${car.uuid}/${user.value.uuid}`)
    isOwner.value = ownRes.data
  } catch (error) {
    console.error(error)
  }
}

async function toggleFavorite() {
  if (!user.value) return

  if (isFavorite.value) {
    try {
      await api.delete(`/favorites/${user.value.uuid}/${car.uuid}`)
      isFavorite.value = false
    } catch (error) {
      console.error(error)
    }
  } else {
    try {
      await api.post('/favorites/', {
        car_uuid: car.uuid
      })
      isFavorite.value = true
    } catch (error) {
      console.error(error)
    }
  }
}

onMounted(() => {
  checkFavorite()
})
</script>
