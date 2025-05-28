import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  },
  {
    path: '/car/:uuid',
    name: 'car',
    component: () => import('@/views/CarPage.vue'),
    props: true
  },
  {
    path: '/cars/edit/:uuid',
    name: 'Edit',
    component: () => import('@/views/EditCarPage.vue'),
    props: true
  },
  {
    path: '/catalog',
    name: 'catalog',
    component: () => import('@/views/Catalog.vue')
  },
  {
    path: '/user/:uuid',
    name: 'user',
    component: () => import('@/views/UserProfile.vue'),
    props: true
  },
  {
    path: '/create_car',
    name: 'create_car',
    component: () => import('@/views/CreateCarPage.vue'),
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
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
    component: () => import('@/views/Chat.vue'),
    meta: { hideFooter: true },
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
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
    component: () => import('@/views/ChatList.vue'),
    meta: { hideFooter: true },
    beforeEnter: async (to, from) => {
      const auth = useAuthStore()

      try {
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