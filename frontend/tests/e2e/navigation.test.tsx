import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

// Mock the API client
vi.mock('../../src/api/client', () => ({
  postIntake: vi.fn(),
  postGenerate: vi.fn(),
  getProject: vi.fn().mockResolvedValue({
    data: {
      project_id: '550e8400-e29b-41d4-a716-446655440000',
      project_name: 'Test',
      status: 'generated',
      intake_data: {},
      created_at: '2026-01-01T00:00:00Z',
      generated_at: '2026-01-01T00:01:00Z',
    },
  }),
  getDownloadUrl: vi.fn().mockReturnValue('/projects/550e8400-e29b-41d4-a716-446655440000/download'),
}));

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
      <MemoryRouter initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}>
        <App />
      </MemoryRouter>,
    );
    expect(screen.getByTestId('generate-page')).toBeInTheDocument();
  });

  it('renders Complete page at /complete/:id', async () => {
    render(
      <MemoryRouter initialEntries={['/complete/550e8400-e29b-41d4-a716-446655440000']}>
        <App />
      </MemoryRouter>,
    );
    await waitFor(() => {
      expect(screen.getByTestId('complete-page')).toBeInTheDocument();
    });
  });
});
