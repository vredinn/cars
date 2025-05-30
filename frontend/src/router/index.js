import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCookie } from '@/api'

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
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/catalog',
    name: 'Catalog',
    component: () => import('@/views/Catalog.vue')
  },
  {
    path: '/create_car',
    name: 'CreateCar',
    component: () => import('@/views/CreateCarPage.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/user/:uuid',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    props: true
  },
  {
    path: '/profile/edit/:uuid',
    name: 'EditProfile',
    component: () => import('@/views/EditProfile.vue'),
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/chats',
    name: 'ChatList',
    component: () => import('@/views/ChatList.vue'),
    meta: { requiresAuth: true, hideFooter: true }
  },
  {
    path: '/chat/:carUuid/:otherUserUuid',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true, hideFooter: true }

  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/Auth.vue'),
    meta: { hideForAuth: true, hideFooter: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  const hasAccessToken = !!getCookie('csrf_access_token')

  // Если нет токена и нет пользователя, значит точно не авторизован
  if (!hasAccessToken && !auth.isAuthenticated) {
    if (to.meta.requiresAuth) {
      next({ name: 'Auth', query: { redirect: to.fullPath } })
      return
    }
  }
  // Если есть токен, но нет пользователя - пробуем получить пользователя
  else if (hasAccessToken && !auth.isAuthenticated) {
    try {
      await auth.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
      if (to.meta.requiresAuth) {
        next({ name: 'Auth', query: { redirect: to.fullPath } })
        return
      }
    }
  }

  // Если страница скрыта для авторизованных и пользователь авторизован
  if (to.meta.hideForAuth && auth.isAuthenticated) {
    next({ name: 'Home' })
    return
  }

  next()
})

export default router