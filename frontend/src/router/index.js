import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
<<<<<<< HEAD
import AutoPage from '../views/AutoPage.vue'
import Catalog from '@/views/Catalog.vue'
=======
import CarPage from '../views/CarPage.vue'
>>>>>>> 1fe1d7b3ba9e8c678b5a6b4c7defa31d6aa48759

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