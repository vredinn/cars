<template>
  <div id="app" class="bg-white">
    <Header />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
import Header from '@/components/Header.vue'


export default {
  name: 'App',
  components: { Header } 
}
</script>

<style>
/* Глобальные стили */
body {
  @apply min-h-screen;
}
</style>