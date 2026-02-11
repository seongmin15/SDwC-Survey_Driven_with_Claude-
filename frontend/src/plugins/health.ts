import type { Plugin } from 'vite';

export function healthHandler() {
  return { status: 'ok' };
}

export function readyHandler() {
  return { status: 'ready' };
}

export function healthPlugin(): Plugin {
  return {
    name: 'health-endpoints',
    configureServer(server) {
      server.middlewares.use('/health', (_req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(healthHandler()));
      });
      server.middlewares.use('/ready', (_req, res) => {
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(readyHandler()));
      });
    },
  };
}
