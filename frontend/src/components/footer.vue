<template>
  <footer class="bg-neutral text-neutral-content py-10">
    <div class="container mx-auto px-4">
      <!-- Верхняя часть: логотип -->
      <div class="flex flex-col md:flex-row justify-between items-center gap-8 mb-8">
        <div class="flex-shrink-0">
          <img src="/src/assets/logo_White.svg" alt="CarPivot" class="h-10" />
        </div>
      </div>

      <!-- Разделительная линия -->
      <div class="border-t border-neutral-content/20 my-6"></div>

      <!-- Нижняя часть -->
      <div class="flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="text-sm text-neutral-content/60">
          © 2025 CarPivot. Все права защищены.
        </div>

        <!-- Кнопка "Наверх" -->
        <button 
          @click="scrollToTop"
          class="btn btn-ghost btn-circle text-neutral-content/60 hover:text-white"
          aria-label="Наверх"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 15l-6-6-6 6" />
          </svg>
        </button>
      </div>
    </div>
  </footer>
</template>

<script setup>
const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
