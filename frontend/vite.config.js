import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import path from "path";


export default defineConfig({
  optimizeDeps: {
    include: ['vue-yandex-maps']
  },
  plugins: [
    tailwindcss(),
    vue(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      '@assets': path.resolve(__dirname, './src/assets')
    },
  },
  server: {
    proxy: {
      '/api': {
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false,
        ws: true
      },
      '/uploads': {
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false,
      },
      '/brand_logos': {
        target: "http://backend:8000",
        changeOrigin: true,
        secure: false,
      },
      '/messages/ws': {
        target: "ws://backend:8000",
        ws: true,
        changeOrigin: true,
        secure: false,
      }
    },
    watch: {
      usePolling: true,
    },
    host: true
  },
});
