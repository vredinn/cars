<template>
    <div class="card bg-base-300 cursor-pointer" @click="$emit('click')">
      <div class="card-body">
        <div class="flex flex-col lg:flex-row gap-4">
          <div class="w-full lg:w-1/4">
            <img :src="getImageUrl(car.preview_image_url)" 
                 class="w-full h-48 object-cover rounded-lg"
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
  export default {
    props: {
      car: Object
    },
    methods: {
      formatPrice(price) {
        return new Intl.NumberFormat('ru-RU', { 
          style: 'currency', 
          currency: 'RUB',
          maximumFractionDigits: 0
        }).format(price)
      },
      getImageUrl(url) {
        return `http://192.168.0.101:8000/${url}`
      }
    }
  }
  </script>