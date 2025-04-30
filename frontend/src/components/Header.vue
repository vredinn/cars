<template>
  <!-- Фиксированный хедер с прозрачностью -->
  <header class="container mx-auto navbar w-full p-0">
    <nav class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost mr-2 lg:hidden">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"> <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" /> </svg>
      </div>
      <ul
        tabindex="0"
        class="menu menu-sm dropdown-content bg-base-200 rounded-box z-1 mt-3 w-52 p-2 shadow">
        <li><router-link 
            to="/" 
            class="btn btn-ghost"
            active-class="btn btn-outline">Главная
          </router-link></li>
          <li><router-link to="/catalog" class="btn btn-ghost"
          active-class="btn btn-outline">Поиск</router-link></li>
        <li><a class="btn btn-ghost">Контакты</a></li>
        <li><a class="btn btn-ghost">О Нас</a></li>
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
        <li><a class="btn btn-ghost">Контакты</a></li>
        <li><a class="btn btn-ghost">О Нас</a></li>
      </ul>
    </nav>
    <div class="flex space-x-2">
      <button class="btn btn-ghost flex items-center">
  <!-- Для темной темы - белая иконка -->
        <img src="/src/assets/avatar.svg" 
            class="h-3 w-3 mr-1 dark:block hidden" 
            alt="Вход">    
        <!-- Для светлой темы - черная иконка -->
        <img src="/src/assets/Avatar_Black.svg" 
            class="h-3 w-3 mr-1 block dark:hidden" 
            alt="Вход"> Вход
      </button>
      <button class="btn btn-primary hidden md:block">Создать объявление</button>
    </div>
  </header>
</template>