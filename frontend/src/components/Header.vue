<template>
     <!-- Прозрачный хедер -->
     <header class="navbar px-8 py-4 bg-transparent absolute top-0 w-full z-10">
        <div class="flex-1">
          <img src="/src/assets/logo_White.svg" alt="СагРivot" class="h-10">
          
        </div>
        <nav class="flex-none hidden lg:flex">
          <ul class="menu menu-horizontal space-x-2 text-white">
            <li><a class="hover:bg-white/10">Главная</a></li>
            <li><a class="hover:bg-white/10">Поиск</a></li>
            <li><a class="hover:bg-white/10">Контакты</a></li>
            <li><a class="hover:bg-white/10">О Нас</a></li>
          </ul>
        </nav>
        <div class="flex-none hidden lg:flex ">
          <button class="btn btn-ghost text-white hover:bg-white/10 flex items-center">
            <img src="/src/assets/avatar.png" alt="Добавить" class="h-3 w-3 mr-1">
            Вход</button>
          <button class="btn">Создать объявление</button>
        </div>
      </header>
  </template>
  
<!-- 
    <script>
  export default {
    name: 'AppHeader',
    data() {
      return {
        scrolled: false
      }
    },
    mounted() {
      window.addEventListener('scroll', this.handleScroll)
    },
    methods: {
      handleScroll() {
        this.scrolled = window.scrollY > 10
      }
    }
  }
  </script>
  
  <style scoped>
  .navbar {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }
  
  .router-link-active {
    background-color: rgba(59, 130, 246, 0.1); /* blue-500/10 */
    color: rgb(59, 130, 246); /* blue-500 */
  }
  </style>-->