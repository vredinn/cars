<template>
  <div>
    <HeroSection />
    <!-- Другие секции -->
    <section class="py-20 container mx-auto px-4">
      <h2 class="text-3xl font-bold text-center mb-10">Популярные предложения</h2>
      <!-- Список автомобилей -->
    </section>
  </div>
</template>

<script>
import HeroSection from '@/components/HeroSection.vue'

export default {
  name: 'HomeView',
  components: { HeroSection }
}
</script>