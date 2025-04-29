<template>
    <div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-2 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Марка</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.brand_id">
            <option :value="null">Любая</option>
            <option v-for="brand in brands" :value="brand.id">{{ brand.name }}</option>
          </select>
        </div>
        
        <div>
          <label class="label">
            <span class="label-text">Модель</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.model_id" :disabled="!tempFilters.brand_id">
            <option :value="null">Любая</option>
            <option v-for="model in filteredModels" :value="model.id">{{ model.name }}</option>
          </select>
        </div>
        
        <div>
          <label class="label">
            <span class="label-text">Состояние</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.car_condition">
            <option :value="null">Любое</option>
            <option v-for="car_condition in carConditions" :value="car_condition">{{ car_condition }}</option>
          </select>
        </div>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Год от</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_year" placeholder="Любой">
        </div>
        <div>
          <label class="label">
            <span class="label-text">Год до</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_year" placeholder="Любой">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">Руль</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.steering_side">
            <option :value="null">Любой</option>
            <option v-for="steering_side in steeringSides" :value="steering_side">{{ steering_side }}</option>
          </select>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Цена от</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_price" placeholder="Любая">
        </div>
        
        <div>
          <label class="label">
            <span class="label-text">Цена до</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_price" placeholder="Любая">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">Тип кузова</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.body_type">
            <option :value="null">Любой</option>
            <option v-for="body_type in bodyTypes" :value="body_type">{{ body_type }}</option>
          </select>
        </div>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Объем двигателя от</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_capacity" placeholder="Любой">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">Объем двигателя до</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_capacity" placeholder="Любой">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">КПП</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.transmission">
            <option :value="null">Любая</option>
            <option v-for="transmission in transmissions" :value="transmission">{{ transmission }}</option>
          </select>
        </div>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Мощность от</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_engine_power" placeholder="Любая">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">Мощность до</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_engine_power" placeholder="Любая">
        </div>
        
        <div>
          <label class="label">
            <span class="label-text">Привод</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.drive_type">
            <option :value="null">Любой</option>
            <option v-for="drive_type in driveTypes" :value="drive_type">{{ drive_type }}</option>
          </select>
        </div>
      </div>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="label">
            <span class="label-text">Пробег от</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.min_millage" placeholder="Любой">
        </div>
  
        <div>
          <label class="label">
            <span class="label-text">Пробег до</span>
          </label>
          <input type="number" class="input input-bordered w-full" v-model="tempFilters.max_millage" placeholder="Любой">
        </div>
        
        <div>
          <label class="label">
            <span class="label-text">Топливо</span>
          </label>
          <select class="select select-bordered w-full" v-model="tempFilters.fuel_type">
            <option :value="null">Любое</option>
            <option v-for="fuel_type in fuelTypes" :value="fuel_type">{{ fuel_type }}</option>
          </select>
        </div>
      </div>
      
      <div class="flex justify-end">
        <button class="btn btn-ghost mr-2" @click="$emit('reset')">Сбросить</button>
        <button class="btn btn-primary" @click="$emit('search')">Поиск</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      brands: Array,
      models: Array,
      filteredModels: Array,
      tempFilters: Object,
      carConditions: Array,
      steeringSides: Array,
      bodyTypes: Array,
      transmissions: Array,
      fuelTypes: Array,
      driveTypes: Array
    },
    watch: {
      tempFilters: {
        handler(newVal) {
          this.$emit('update:tempFilters', newVal)
        },
        deep: true
      }
    }
  }
  </script>