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
      <div class="container mx-auto py-8">
        <div class="w-full bg-white/100 backdrop-blur-sm rounded-[20px] lg:rounded-full shadow-xl p-1">
          <div class="flex flex-col md:flex-row gap-3">
            <select class="select select-bordered bg-white flex-1 text-black">
              <option disabled selected>Марка</option>
              <option>BMW</option>
              <option>Audi</option>
            </select>
            <select class="select select-bordered bg-white flex-1 text-black">
              <option disabled selected>Модель</option>
              <option>X5</option>
              <option>A6</option>
            </select>
            <select class="select select-bordered bg-white flex-1 text-black">
              <option selected>Год выпуска: Все</option>
              <option>2023</option>
              <option>2022</option>
            </select>
            <select class="select select-bordered bg-white flex-1 text-black">
              <option selected>Цена: Все цены</option>
              <option>До 500 000 ₽</option>
              <option>До 1 000 000 ₽</option>
            </select>
            <button class="btn btn-outline text-black">Все фильтры</button>
            <button class="btn btn-dark"><img src="/src/assets/icon_seartch.png" alt="Добавить"
                class="h-3 w-3 mr-0">Поиск</button>
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