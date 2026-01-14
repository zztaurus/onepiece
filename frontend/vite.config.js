import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      },
      // 如果后端有其他非 /api 开头的接口（比如 /auth），可以在这里添加
      // 但建议后端统一规范为 /api
      '/auth': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      }
    }
  }
})
