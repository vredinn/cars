<template>
<<<<<<< HEAD
  <div id="app" class="">
=======
  <div id="app" class="bg-base-100">
    <Header />
>>>>>>> 1fe1d7b3ba9e8c678b5a6b4c7defa31d6aa48759
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