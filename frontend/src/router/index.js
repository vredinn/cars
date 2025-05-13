import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

import Catalog from '@/views/Catalog.vue'
import CarPage from '@/views/CarPage.vue'
import UserProfile from '@/views/UserProfile.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router