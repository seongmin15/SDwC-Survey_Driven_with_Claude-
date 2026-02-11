/// <reference types="vitest/config" />
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { healthPlugin } from './src/plugins/health';

const apiTarget = process.env.API_URL || 'http://localhost:8000';

export default defineConfig({
  plugins: [react(), healthPlugin()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/intakes': apiTarget,
      '/generate': apiTarget,
      '/projects': apiTarget,
    },
  },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
});
