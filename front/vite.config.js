import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from "path";

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "assets": path.resolve(__dirname, "./src/assets"),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@import "@/assets/css/main.scss";@import "@/assets/css/snippets.scss";`,
      },
    },
  },
  plugins: [vue()],
});
