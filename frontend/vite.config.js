import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import vue from "@vitejs/plugin-vue";
import path from "path";


export default defineConfig({
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
    },
    watch: {
      usePolling: true,
    },
    host: true,
  },
});
