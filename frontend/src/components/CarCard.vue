<template>
  <div @click="goToCar(car.uuid)" class="card bg-base-300 cursor-pointer" :class="{ 'border-dashed border-2 border-error': car.is_sold }">
    <div class="card-body p-4">
      <div class="flex flex-col lg:flex-row gap-4">
        <div class="w-full lg:w-1/4">
          <img :src="car.preview_image_url || '/uploads/no_car_image.png'" class="w-full h-52 object-cover rounded-box"
            :alt="`${car.brand_name} ${car.model_name}`" />
        </div>

        <div class="w-full lg:w-3/4">
          <h3 class="card-title">
            <span :class="{ 'line-through': car.is_sold }">{{ car.brand_name }} {{ car.model_name }} - {{ car.year }} г.</span>
            <span v-if="car.is_sold" class="badge badge-error">Продано</span>
            <span 
              v-if="isOwner || user?.is_admin"
              class="badge"
              :class="{
                'badge-warning': car.moderation_status === 'pending' || car.moderation_status === 'На проверке',
                'badge-success': car.moderation_status === 'approved' || car.moderation_status === 'Одобрено',
                'badge-error': car.moderation_status === 'rejected' || car.moderation_status === 'Отклонено'
              }"
            >
              {{ getModerationStatusDisplay(car.moderation_status) }}
            </span>
          </h3>
          <p>
            {{ car.engine_power }} л.с. {{ car.fuel_type }}, {{ car.engine_capacity }} л,
            {{ car.steering_side }} руль, {{ car.drive_type }} привод
          </p>
          <div class="mt-2">
            <span class="text-xl font-bold" :class="{ 'line-through': car.is_sold }">{{ formatPrice(car.price) }}</span>
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
            <div v-if="isOwner" class="badge badge-lg h-10 badge-dash">
              Ваше объявление
            </div>
            <div v-else>
              <div v-if="!isFavorite" class="tooltip tooltip-left" data-tip="Добавить в избранное">
                <button @click.stop="toggleFavorite" v-if="user"
                  class="btn btn-outline p-2 w-10 h-10 md:w-full md:h-auto">
                  <svg class="w-4 h-4 fill-base-content">
                    <use href="#icon_favorite" />
                  </svg>
                  <template class="hidden md:block">В избранное</template>
                </button>
              </div>
              <div v-if="isFavorite" class="tooltip tooltip-left" data-tip="Удалить из избранного">
                <button @click.stop="toggleFavorite" v-if="user"
                  class="btn btn-secondary p-2 w-10 h-10 md:w-full md:h-auto">
                  <svg class="w-4 h-4 fill-secondary-content">
                    <use href="#icon_favorite" />
                  </svg>
                  <template class="hidden md:block">В избранном</template>
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

const props = defineProps({
  car: Object
})

const car = props.car 

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const isFavorite = ref(false)
const isOwner = ref(false)

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

function getModerationStatusDisplay(status) {
  switch (status) {
    case 'pending':
    case 'На проверке':
      return 'На проверке'
    case 'approved':
    case 'Одобрено':
      return 'Одобрено'
    case 'rejected':
    case 'Отклонено':
      return 'Отклонено'
    default:
      return status
  }
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
      await api.delete(`/favorites/${car.uuid}`)
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

onMounted(async () => {
  await checkFavorite()
})
</script>
