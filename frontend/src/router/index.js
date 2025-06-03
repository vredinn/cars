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
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Moderations.vue')
      },
      {
        path: 'moderations',
        name: 'AdminModerations',
        component: () => import('@/views/admin/Moderations.vue')
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue')
      },
      {
        path: 'brands',
        name: 'AdminBrands',
        component: () => import('@/views/admin/Brands.vue')
      },
      {
        path: 'models',
        name: 'AdminModels',
        component: () => import('@/views/admin/Models.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  const hasAccessToken = !!getCookie('csrf_access_token')

  if (!hasAccessToken && !auth.isAuthenticated) {
    if (to.meta.requiresAuth) {
      next({ name: 'Auth', query: { redirect: to.fullPath } })
      return
    }
  }
  else if (hasAccessToken && !auth.isAuthenticated) {
    try {
      await auth.fetchUser()
    } catch (error) {
      console.error('Ошибка загрузки пользователя:', error)
      if (to.meta.requiresAuth) {
        next({ name: 'Auth', query: { redirect: to.fullPath } })
        return
      }
    }
  }

  if (to.meta.hideForAuth && auth.isAuthenticated) {
    next({ name: 'Home' })
    return
  }

  if (to.meta.requiresAdmin && !auth.user?.is_admin) {
    next({ name: 'Home' })
    return
  }

  next()
})

export default router