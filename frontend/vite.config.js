import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const BASE_URL = process.env.VITE_BASE_URL || 'http://localhost';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    hmr: {
      host: BASE_URL.replace(/^https?:\/\//, ''), 
      protocol: BASE_URL.startsWith('https') ? 'wss' : 'ws',
    },
    port: 3000, 
    host: true, 
  },
})
