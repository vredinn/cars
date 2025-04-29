<template>
    <footer class="bg-neutral text-white py-10">
      <!-- Основное содержимое футера -->
      <div class="container mx-auto px-4">
        <!-- Верхняя часть с лого и формой -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-8 mb-8">
          <!-- Логотип -->
          <div class="flex-shrink-0">
            <img src="/src/assets/logo_White.svg" alt="CarPivot" class="h-10">
          </div>
          
          <!-- Форма подписки -->
          <div class="w-full md:w-auto">
            <div class="join">
              <input 
                type="email" 
                placeholder="Ваш Email адрес" 
                class="input input-bordered join-item w-full md:w-64 bg-neutral border-primary text-white"
              >
              <button class="btn btn-primary join-item">
                Отправить
              </button>
            </div>
          </div>
        </div>
        
        <!-- Разделительная линия -->
        <div class="border-t border-gray-700 my-6"></div>
        
        <!-- Нижняя часть с копирайтом и кнопкой -->
        <div class="flex flex-col md:flex-row justify-between items-center gap-4 ">
          <div class="text-gray-400">
            © 2025 CarPivot. Все права защищены.
          </div>
          <!-- Кнопка "Наверх" -->
        <button 
            @click="scrollToTop"
            class="btn btn-ghost btn-circle text-gray-400 hover:text-white "
            aria-label="Наверх">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 15l-6-6-6 6"/>
            </svg>
        </button>
        </div>
      </div>
      
    </footer>
  </template>
  
  <script>
  export default {
    name: 'Footer',
    methods: {
      scrollToTop() {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      }
    }
  }
  </script>
  
  <style scoped>
  /* Адаптация для мобильных */
  @media (max-width: 768px) {
    .join {
      flex-direction: column;
      width: 100%;
    }
    
    .join-item {
      width: 100% !important;
    }
    
    .join-item:first-child {
      margin-bottom: 0.5rem;
    }
  }
  </style>