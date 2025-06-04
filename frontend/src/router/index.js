import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getCookie } from '@/api'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: 'Главная' }
  },
  {
    path: '/car/:uuid',
    name: 'car',
    component: () => import('@/views/CarPage.vue'),
    props: true,
    meta: { title: 'Просмотр автомобиля' }
  },
  {
    path: '/cars/edit/:uuid',
    name: 'Edit',
    component: () => import('@/views/EditCarPage.vue'),
    props: true,
    meta: { requiresAuth: true, title: 'Редактирование объявления' }
  },
  {
    path: '/catalog',
    name: 'Catalog',
    component: () => import('@/views/Catalog.vue'),
    meta: { title: 'Поиск' }
  },
  {
    path: '/create_car',
    name: 'CreateCar',
    component: () => import('@/views/CreateCarPage.vue'),
    meta: { requiresAuth: true, title: 'Создать объявление' }
  },
  {
    path: '/user/:uuid',
    name: 'UserProfile',
    component: () => import('@/views/UserProfile.vue'),
    props: true,
    meta: { title: 'Профиль пользователя' }
  },
  {
    path: '/profile/edit/:uuid',
    name: 'EditProfile',
    component: () => import('@/views/EditProfile.vue'),
    props: true,
    meta: { requiresAuth: true, title: 'Редактирование профиля' }
  },
  {
    path: '/chats',
    name: 'ChatList',
    component: () => import('@/views/ChatList.vue'),
    meta: { requiresAuth: true, hideFooter: true, title: 'Список чатов' }
  },
  {
    path: '/chat/:carUuid/:otherUserUuid',
    name: 'Chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: true, hideFooter: true, title: 'Чат' },
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/Auth.vue'),
    meta: { hideForAuth: true, hideFooter: true, title: 'Авторизация' }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, title: 'Админ-панель' },
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

  // Update page title
  const pageTitle = to.meta.title ? `CarPivot - ${to.meta.title}` : 'CarPivot'
  document.title = pageTitle

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