import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

import Catalog from '@/views/Catalog.vue'
import CarPage from '@/views/CarPage.vue'
import UserProfile from '@/views/UserProfile.vue'
import CreateCarPage from '@/views/CreateCarPage.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/car/:uuid',
    name: 'car',
    component: CarPage,
    props: true
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: Catalog

  },
  {
    path: '/user/:uuid',
    name: 'user',
    component: UserProfile,
    props: true
  },
  {
    path: '/create_car',
    name: 'create_car',
    component: CreateCarPage,
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router