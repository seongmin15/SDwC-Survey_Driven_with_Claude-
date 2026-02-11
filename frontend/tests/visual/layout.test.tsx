import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

describe('V-011: Consistent header/footer across all pages', () => {
  const routes = [
    { path: '/', name: 'Survey' },
    { path: '/generate/test-id', name: 'Generate' },
    { path: '/complete/test-id', name: 'Complete' },
  ];

  routes.forEach(({ path, name }) => {
    it(`renders header on ${name} page`, () => {
      render(
        <MemoryRouter initialEntries={[path]}>
          <App />
        </MemoryRouter>,
      );
      expect(screen.getByRole('banner')).toBeInTheDocument();
    });

    it(`renders footer on ${name} page`, () => {
      render(
        <MemoryRouter initialEntries={[path]}>
          <App />
        </MemoryRouter>,
      );
      expect(screen.getByRole('contentinfo')).toBeInTheDocument();
    });
  });
});

describe('V-012: Content area centered with max-width', () => {
  const routes = [
    { path: '/', name: 'Survey' },
    { path: '/generate/test-id', name: 'Generate' },
    { path: '/complete/test-id', name: 'Complete' },
  ];

  routes.forEach(({ path, name }) => {
    it(`content area is centered on ${name} page`, () => {
      render(
        <MemoryRouter initialEntries={[path]}>
          <App />
        </MemoryRouter>,
      );
      const main = screen.getByRole('main');
      expect(main).toBeInTheDocument();
      expect(main.className).toMatch(/mx-auto/);
      expect(main.className).toMatch(/max-w-/);
    });
  });
});
