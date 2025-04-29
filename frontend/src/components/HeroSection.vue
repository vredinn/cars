<template>
  <section class="hero min-h-screen relative flex flex-col">
    <!-- Фоновое изображение -->
    <div class="hero-bg absolute inset-0 bg-cover bg-center" :style="{ backgroundImage: 'url(/src/assets/i.webp)' }">
    </div>
    



    <!-- Основной контент -->
    <div
      class="container mx-auto hero-content w-full flex-1 flex flex-col items-center justify-center text-center text-white">
      <div class="mb-8">
        <p class="text-xl">СагРivot – ваш поворот к идеальному автомобилю. С нами вы найдете автомобиль своей мечты
          быстро и удобно!</p>
        <h2 class="text-5xl font-bold ">Найдите свой идеальный автомобиль</h2>
      </div>
      

            <!-- Поисковая форма -->
      <div class="container mx-auto py-8 font-bold">
        <div class="w-full bg-white dark:bg-base-200 rounded-[20px] lg:rounded-full shadow-xl p-1">
          <div class="flex flex-col md:flex-row gap-3">
            <!-- Поле выбора марки -->
            <select class="select select-bordered font-bold flex-1 bg-white dark:bg-base-200 text-black dark:text-white border-gray-300 dark:border-base-300">
              <option disabled selected class="font-bold">Марка</option>
              <option class="font-bold">BMW</option>
              <option class="font-bold">Audi</option>
            </select>

            <!-- Поле выбора модели -->
            <select class="select select-bordered font-bold flex-1 bg-white dark:bg-base-200 text-black dark:text-white border-gray-300 dark:border-base-300">
              <option disabled selected class="font-bold">Модель</option>
              <option class="font-bold">X5</option>
              <option class="font-bold">A6</option>
            </select>

            <!-- Поле выбора года -->
            <select class="select select-bordered font-bold flex-1 bg-white dark:bg-base-200 text-black dark:text-white border-gray-300 dark:border-base-300">
              <option selected class="font-bold">Год выпуска: Все</option>
              <option class="font-bold">2023</option>
              <option class="font-bold">2022</option>
            </select>

            <!-- Поле выбора цены -->
            <select class="select select-bordered font-bold flex-1 bg-white dark:bg-base-200 text-black dark:text-white border-gray-300 dark:border-base-300">
              <option selected class="font-bold">Цена: Все цены</option>
              <option class="font-bold">До 500 000 ₽</option>
              <option class="font-bold">До 1 000 000 ₽</option>
            </select>

            <!-- Кнопка "Все фильтры" -->
            <button class="btn btn-outline font-bold text-black dark:text-white border-gray-300 dark:border-base-300 hover:bg-gray-100 dark:hover:bg-base-300">
              Все фильтры
            </button>

            <!-- Кнопка "Поиск" -->
            <button class="btn bg-blue-600 dark:bg-blue-700 text-white hover:bg-blue-700 dark:hover:bg-blue-800 flex items-center">
              <!-- Иконка для темной темы (белая) -->
              <img src="/src/assets/Icon_seartch_White.svg" 
                  alt="Поиск" 
                  class="h-3 w-3 mr-2 dark:block hidden">
              
              <!-- Иконка для светлой темы (черная) -->
              <img src="/src/assets/Icon_seartch_Black.svg" 
                  alt="Поиск" 
                  class="h-3 w-3 mr-2 block dark:hidden">
              Поиск
            </button>
          </div>
        </div>
      </div>

    </div>
    <div class="absolute bottom-0 left-0 w-full h-[200px] 
              bg-gradient-to-b from-transparent from-50% to-base-100 to-100%
              rounded-t-[50px] z-[1] pointer-events-none">
  </div>
  </section>
</template>