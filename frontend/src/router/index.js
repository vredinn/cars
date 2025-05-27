import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

import Catalog from '@/views/Catalog.vue'
import CarPage from '@/views/CarPage.vue'
import UserProfile from '@/views/UserProfile.vue'
import CreateCarPage from '@/views/CreateCarPage.vue'
import EditCarPage from '@/views/EditCarPage.vue'
import { useAuthStore } from '@/stores/auth'
import Chat from '@/views/Chat.vue';
import ChatList from '@/views/ChatList.vue'

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
    path: '/cars/edit/:uuid',
    name: 'Edit',
    component: EditCarPage,
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
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
        // Если пользователь уже загружен — ничего не делаем
        if (!auth.user) {
          await auth.fetchUser()
        }

        if (auth.user) {
          return true
        }

        return { name: 'Home' }
      } catch (e) {
        return { name: 'Home' }
      }
    }
  },
  {
    path: '/chat/:carUuid/:otherUserUuid',
    name: 'Chat',
    component: Chat,
    meta: { hideFooter: true },
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
        // Если пользователь уже загружен — ничего не делаем
        if (!auth.user) {
          await auth.fetchUser()
        }

        if (auth.user) {
          return true
        }

        return { name: 'Home' }
      } catch (e) {
        return { name: 'Home' }
      }
    }
  },
  {
    path: '/chats',
    name: 'ChatList',
    component: ChatList,

    meta: { hideFooter: true },
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
        // Если пользователь уже загружен — ничего не делаем
        if (!auth.user) {
          await auth.fetchUser()
        }

        if (auth.user) {
          return true
        }

        return { name: 'Home' }
      } catch (e) {
        return { name: 'Home' }
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router