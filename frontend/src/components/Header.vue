<template>
  <!-- Прозрачный хедер -->
  <header class="navbar px-8 py-4 bg-transparent absolute top-0 w-full z-10">
    <div class="flex-1">
      <img src="/src/assets/logo_White.svg" alt="СагРivot" class="h-10">

    </div>
    <nav class="flex-none hidden lg:flex">
      <ul class="menu menu-horizontal space-x-2 text-white">
        <li><a class="btn btn-ghost text-white hover:bg-white/10">Главная</a></li>
        <li><a class="btn btn-ghost text-white hover:bg-white/10">Поиск</a></li>
        <li><a class="btn btn-ghost text-white hover:bg-white/10">Контакты</a></li>
        <li><a class="btn btn-ghost text-white hover:bg-white/10">О Нас</a></li>
      </ul>
    </nav>
    <div class="flex-none hidden lg:flex space-x-2">
      <button class="btn btn-ghost text-white hover:bg-white/10 flex items-center">
        <img src="/src/assets/avatar.png" alt="Добавить" class="h-3 w-3 mr-1">
        Вход
      </button>
      <button class="btn">Создать объявление</button>
    </div>
  </header>
</template>