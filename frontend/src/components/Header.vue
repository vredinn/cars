<template>
  <!-- Фиксированный хедер с прозрачностью -->
  <header class="container mx-auto navbar w-full px-4 py-0">
    <nav class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost mr-2 lg:hidden">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /> </svg>
      </div>
      <ul
        tabindex="0"
        class="menu menu-sm dropdown-content bg-base-200 rounded-box z-1 mt-3 w-64 p-2 shadow gap-2">
        <li><router-link 
            to="/" 
            class="btn btn-ghost"
            active-class="btn btn-outline">Главная
          </router-link></li>
          <li><router-link to="/catalog" class="btn btn-ghost"
          active-class="btn btn-outline">Поиск</router-link></li>
        <!-- <li><a class="btn btn-ghost">Контакты</a></li>
        <li><a class="btn btn-ghost">О Нас</a></li> -->
      </ul>
    </nav>
    <router-link to="/" class="flex-1">
      <div class="h-8">
        <img src="/src/assets/logo_White.svg" 
            alt="Logo"
            class="h-full dark:block hidden">
        <img src="/src/assets/logo_Black.svg" 
            alt="Logo"
            class="h-full block dark:hidden">
      </div>
    </router-link>
    <nav class="flex-none hidden lg:flex">
      <ul class="menu menu-horizontal space-x-2 ">
        <li><router-link 
            to="/" 
            class="btn btn-ghost"
            active-class="btn btn-outline">Главная
          </router-link>
        </li>
        <li><router-link to="/catalog" class="btn btn-ghost"
          active-class="btn btn-outline">Поиск</router-link></li>
        <!-- <li><a class="btn btn-ghost">Контакты</a></li>
        <li><a class="btn btn-ghost">О Нас</a></li> -->
      </ul>
    </nav>
    <div class="flex space-x-2">    
    <template v-if="!user">
      <LoginForm />
    </template>
    <template v-if="user">
      <!-- <router-link to="/" class="btn btn-primary">
        Сообщения
      </router-link> -->
      <router-link to="/create_car" class="btn btn-primary hidden md:flex">Создать объявление</router-link>
      <router-link to="/" class="btn btn-primary hidden md:inline-flex">
        Мои объявления
      </router-link>

      <div class="dropdown dropdown-end">
        <div tabindex="0" role="button" class="btn btn-ghost btn-circle avatar">
          <div class="w-10 rounded-full">
            <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar"/>
          </div>
        </div>
        <ul
          tabindex="0"
          class="menu dropdown-content z-[1] mt-3 w-64 rounded-box bg-base-200 p-2 shadow gap-2">
          <div class="flex flex-col gap-2">
            <div class="avatar">
              <div class="h-36 w-full rounded-box">
                <img :src="user.avatar_url || '/uploads/user_example.webp'" alt="avatar"/>
              </div>
            </div>
            <div class="text-center text-pretty">{{ user.name }} <br> {{ user.email }}</div>
          </div>
          <li><router-link to="/create_car" class="btn btn-primary md:hidden">Создать объявление</router-link></li>
          <li>
            <router-link to="/" class="btn btn-primary md:hidden">
              Мои объявления
            </router-link>
          </li>
          <li><router-link :to="'/user/' + user.uuid" class="btn btn-outline">Профиль</router-link></li>
          <li><label for="logout-modal" class="btn btn-soft btn-error">Выйти</label></li>
        </ul>
        <!-- Модалка подтверждения -->
        <input type="checkbox" id="logout-modal" class="modal-toggle" v-model="showLogoutModal" />
        <div class="modal modal-bottom sm:modal-middle">
          <div class="modal-box">
            <h3 class="font-bold text-lg">Выход</h3>
            <p class="py-4">Вы уверены, что хотите выйти?</p>
            <div class="modal-action">
              <label for="logout-modal" class="btn btn-primary">Отмена</label>
              <button @click="confirmLogout" class="btn btn-soft btn-error">Выйти</button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
  </header>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Header',
  components: {
    LoginForm
  },
  data() {
    return {      
      showLogoutModal: false, 
    }
  },
  computed: {
    user() {
      return useAuthStore().user
    }
  },
  methods: {
    confirmLogout() {
      this.showLogoutModal = false
      useAuthStore().logout()
    }
  }
}
</script>