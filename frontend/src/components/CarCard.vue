<template>
    <div @click="goToCar(car.uuid)" class="card bg-base-300 cursor-pointer">
      <div class="card-body">
        
        <div v-if="!is_favorite" class="tooltip absolute top-6 right-6 " data-tip="Добавить в избранное">
          <button @click.stop="toggleFavorite()" v-if="user" class="btn btn-primary p-2 h-auto">
            <svg class="w-4 h-4 fill-primary-content">
              <use href="#icon_favorite"></use>
            </svg>
          </button>
        </div>
        <div v-if="is_favorite" class="tooltip absolute top-6 right-6 " data-tip="Удалить из избранного">
          <button @click.stop="toggleFavorite()" v-if="user" class="btn btn-secondary p-2 h-auto">
            <svg class="w-4 h-4 fill-secondary-content">
              <use href="#icon_favorite"></use>
            </svg>
          </button>
        </div>
        <div class="flex flex-col lg:flex-row gap-4">
          <div class="w-full lg:w-1/4">
            <img :src="car.preview_image_url" 
                 class="w-full h-48 object-cover rounded-box"
                 :alt="`${car.brand_name} ${car.model_name}`">
          </div>
          
          <div class="w-full lg:w-3/4">
            <h3 class="card-title">{{ car.brand_name }} {{ car.model_name }} - {{ car.year }} г.</h3>
            <p>{{ car.engine_power }} л.с. {{ car.fuel_type }}, {{ car.engine_capacity }} л, {{ car.steering_side }} руль, {{ car.drive_type }} привод</p>
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
              <router-link :to="`/car/${car.uuid}`" class="btn btn-primary" @click.stop>Подробнее</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script>
  import { useAuthStore } from '@/stores/auth'
  import api from '@/api'
  export default {
    props: {
      car: Object
    },
    data() {
      return {
        is_favorite: false
      }
    },
    computed: {
      user() {
        return useAuthStore().user
      }
    },
    methods: {
      goToCar(uuid) {
        this.$router.push(`/car/${uuid}`);
      },
      formatPrice(price) {
        return new Intl.NumberFormat('ru-RU', { 
          style: 'currency', 
          currency: 'RUB',
          maximumFractionDigits: 0
        }).format(price)
      },
      async checkFavorite() {
        if (!this.user) {
          return
        }
        try {
          const response = await api.get(`/favorites/check/${this.user.uuid}/${this.car.uuid}`)
          this.is_favorite = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async toggleFavorite() {
        if (!this.user) {
          return
        }
        if (this.is_favorite) {
          try {
            await api.delete(`/favorites/${this.user.uuid}/${this.car.uuid}`)
            this.is_favorite = false
          } catch (error) {
            console.error(error)
          }          
        }
        else {
          try {
            await api.post('/favorites', {
                user_uuid: this.user.uuid,
                car_uuid: this.car.uuid
            })
            this.is_favorite = true
          } catch (error) {
            console.error(error)
          }          
        }
      }
    },
    created() {
      this.checkFavorite()
    }
  }
</script>