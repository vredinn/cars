<template>
  <div class="admin-dashboard">
    <nav class="admin-nav bg-base-100">
      <div class="container mx-auto">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-2xl font-bold">Панель администратора</h1>
        </div>
        <div role="tablist" class="tabs tabs-border justify-center">
          <router-link 
            role="tab"
            to="/admin/moderations" 
            class="tab"
            :class="{ 'tab-active': $route.name === 'AdminModerations' || $route.name === 'AdminDashboard' }"
          >
            Модерация
          </router-link>
          <router-link 
            role="tab"
            to="/admin/users" 
            class="tab"
            :class="{ 'tab-active': $route.name === 'AdminUsers' }"
          >
            Пользователи
          </router-link>
          <router-link role="tab" to="/admin/brands" class="tab" :class="{ 'tab-active': $route.name === 'AdminBrands' } || $route.name === 'AdminDashboard'">Марки</router-link>
          <router-link role="tab" to="/admin/models" class="tab" :class="{ 'tab-active': $route.name === 'AdminModels' } || $route.name === 'AdminDashboard'">Модели</router-link>
        </div>
      </div>
    </nav>

    <div class="container mx-auto pb-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
</script>
