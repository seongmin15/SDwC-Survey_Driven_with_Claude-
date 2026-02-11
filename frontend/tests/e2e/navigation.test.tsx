import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

describe('E-012: Unknown route redirects to Survey', () => {
  it('redirects /unknown to Survey page', () => {
    render(
      <MemoryRouter initialEntries={['/unknown']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('survey-page')).toBeInTheDocument();
  });

  it('redirects /foo/bar/baz to Survey page', () => {
    render(
      <MemoryRouter initialEntries={['/foo/bar/baz']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('survey-page')).toBeInTheDocument();
  });

  it('renders Survey page at /', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('survey-page')).toBeInTheDocument();
  });

  it('renders Generate page at /generate/:id', () => {
    render(
      <MemoryRouter initialEntries={['/generate/test-id']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('generate-page')).toBeInTheDocument();
  });

  it('renders Complete page at /complete/:id', () => {
    render(
      <MemoryRouter initialEntries={['/complete/test-id']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('complete-page')).toBeInTheDocument();
  });
});
