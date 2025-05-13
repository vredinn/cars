<template>
  <div id="app" class="">
    <Header />
    <main>
      <router-view />
    </main>
    <Footer />
  </div>
</template>

<script>
import Header from '@/components/Header.vue'
import { useAuthStore } from '@/stores/auth'
import Footer from '@/components/Footer.vue';

export default {
  name: 'App',
  components: { Header, Footer } ,
  created() {
    const auth = useAuthStore();    
    auth.fetchUser().then(() => {
      auth.startAutoRefresh()
    })
  },
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