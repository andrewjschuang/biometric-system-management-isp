import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    host: true, // Listen on all network interfaces
    port: 5173, // Default Vite port
    allowedHosts: true,
    proxy: {
      '/api': {
        target: 'http://backend:5003',
        changeOrigin: true,
        rewrite: (path) => path
      }
    }
  },
});
