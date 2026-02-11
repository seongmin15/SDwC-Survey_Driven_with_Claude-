import { describe, it, expect } from 'vitest';
import { healthHandler, readyHandler } from '../src/plugins/health';

describe('Frontend Health Endpoints', () => {
  it('/health returns status ok', () => {
    const result = healthHandler();
    expect(result).toEqual({ status: 'ok' });
  });

  it('/ready returns status ready', () => {
    const result = readyHandler();
    expect(result).toEqual({ status: 'ready' });
  });
});
