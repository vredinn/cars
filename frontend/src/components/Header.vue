<template>
  <!-- Фиксированный хедер с прозрачностью -->
  <header class="navbar px-8 py-4 w-full z-50 border-b border-base-200/10 bg-transparent">
    <div class="flex-1">
      <div class="h-10">
        <img src="/src/assets/logo_White.svg" 
            alt="Logo"
            class="h-full dark:block hidden">
        <img src="/src/assets/logo_Black.svg" 
            alt="Logo"
            class="h-full block dark:hidden">
      </div>
    </div>
    <nav class="flex-none hidden lg:flex">
      <ul class="menu menu-horizontal space-x-2 ">
        <li><router-link 
            to="/" 
            class="btn btn-ghost hover:bg-white/10"
            active-class="btn btn-ghost  hover:bg-white/10">Главная
          </router-link>
        </li>
        <li><a class="btn btn-ghost  hover:bg-white/10">Поиск</a></li>
        <li><a class="btn btn-ghost  hover:bg-white/10">Контакты</a></li>
        <li><a class="btn btn-ghost  hover:bg-white/10">О Нас</a></li>
      </ul>
    </nav>
    <div class="flex-none hidden lg:flex space-x-2">
      <button class="btn btn-ghost hover:bg-white/10 flex items-center">
  <!-- Для темной темы - белая иконка -->
        <img src="/src/assets/avatar.png" 
            class="h-3 w-3 mr-1 dark:block hidden" 
            alt="Вход">    
        <!-- Для светлой темы - черная иконка -->
        <img src="/src/assets/Avatar_Black.svg" 
            class="h-3 w-3 mr-1 block dark:hidden" 
            alt="Вход"> Вход
      </button>
      <button class="btn">Создать объявление</button>
    </div>
  </header>
</template>