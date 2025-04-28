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
  </section>
</template>

<script>
export default {
  name: 'HeroSection'
}
</script>

<style scoped>
.hero-bg {
  z-index: 0;
}

/* Градиент внизу для плавного перехода к следующей секции */
.hero::after {
  border-radius: 50px 50px 0 0;
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 150px;
  background: linear-gradient(to bottom, transparent 50%, white 100%);
  z-index: 1;
}

/* Адаптация для мобильных */
@media (max-width: 768px) {
  .hero {
    min-height: 90vh;
  }

  .hero-content {
    padding-top: 6rem;
    padding-bottom: 4rem;
  }

  .flex-col.md\:flex-row {
    flex-direction: column;
  }

  .select,
  .btn {
    width: 100%;
  }
}
</style>