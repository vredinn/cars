<template>
  <div id="app" class="bg-base-100">
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
  components: { Header } ,
  watch: {
    $route() {
      // Сбрасываем прокрутку при смене маршрута
      window.scrollTo(0, 0)
    }
  }
}

</script>

<style>
/* Глобальные стили */
body {
  @apply min-h-screen;
}
</style>