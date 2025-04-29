import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

import Catalog from '@/views/Catalog.vue'
import CarPage from '@/views/CarPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/car/:id',
    name: 'car',
    component: CarPage,
    props: true
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: Catalog

  }
  // Добавьте другие маршруты
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router