/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { healthPlugin } from './src/plugins/health';

export default defineConfig({
  plugins: [react(), healthPlugin()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/intakes': 'http://localhost:8000',
      '/generate': 'http://localhost:8000',
      '/projects': 'http://localhost:8000',
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
});
