import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

// Mock the API client
vi.mock('../../src/api/client', () => ({
  postIntake: vi.fn(),
  postGenerate: vi.fn(),
  getProject: vi.fn(),
  getDownloadUrl: vi.fn(),
}));

import { postGenerate, getProject } from '../../src/api/client';
const mockPostGenerate = vi.mocked(postGenerate);
const mockGetProject = vi.mocked(getProject);

describe('E-007: Generate API 500 → error + retry', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
    mockGetProject.mockReset();
  });

  it('shows error state with retry button when API returns 500', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter initialEntries={['/generate/a1b2c3d4-e5f6-7890-abcd-ef1234567890']}>
        <App />
      </MemoryRouter>,
    );

    // Should show error message and retry button
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
      expect(screen.getByText(/오류가 발생했습니다/)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /재시도|retry/i })).toBeInTheDocument();
    });
  });

  it('retries generation when retry button is clicked', async () => {
    mockPostGenerate
      .mockRejectedValueOnce(new Error('HTTP error! status: 500'))
      .mockResolvedValueOnce({
        data: {
          project_id: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
          status: 'generated',
          download_url: '/projects/a1b2c3d4-e5f6-7890-abcd-ef1234567890/download',
          generated_at: '2026-01-01T00:00:00Z',
        },
      });

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/generate/a1b2c3d4-e5f6-7890-abcd-ef1234567890']}>
        <App />
      </MemoryRouter>,
    );

    // Wait for error
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /재시도|retry/i })).toBeInTheDocument();
    });

    // Click retry
    await user.click(screen.getByRole('button', { name: /재시도|retry/i }));

    // Should navigate to complete page on success
    await waitFor(() => {
      expect(screen.getByTestId('complete-page')).toBeInTheDocument();
    });
  });
});

describe('E-010: invalid-id direct access → redirect to Survey', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
    mockGetProject.mockReset();
  });

  it('redirects to Survey when project_id is not a valid UUID', async () => {
    render(
      <MemoryRouter initialEntries={['/generate/invalid-id']}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('survey-page')).toBeInTheDocument();
    });
  });

  it('redirects to Survey when project_id is empty-like', async () => {
    render(
      <MemoryRouter initialEntries={['/generate/---']}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('survey-page')).toBeInTheDocument();
    });
  });
});

describe('E-013: already generated → redirect to Complete', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
    mockGetProject.mockReset();
  });

  it('redirects to Complete when API returns 409 (already generated)', async () => {
    const error = new Error('HTTP error! status: 409');
    (error as any).status = 409;
    mockPostGenerate.mockRejectedValue(error);

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('complete-page')).toBeInTheDocument();
    });
  });
});

describe('E-014: browser refresh → state restoration', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
    mockGetProject.mockReset();
  });

  it('re-triggers generation on page re-entry with valid project_id', async () => {
    mockPostGenerate.mockResolvedValue({
      data: {
        project_id: '550e8400-e29b-41d4-a716-446655440000',
        status: 'generated',
        download_url: '/projects/550e8400-e29b-41d4-a716-446655440000/download',
        generated_at: '2026-01-01T00:00:00Z',
      },
    });

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    // Should call postGenerate automatically
    await waitFor(() => {
      expect(mockPostGenerate).toHaveBeenCalledWith(
        '550e8400-e29b-41d4-a716-446655440000',
      );
    });

    // Should navigate to complete page
    await waitFor(() => {
      expect(screen.getByTestId('complete-page')).toBeInTheDocument();
    });
  });
});

describe('Generate page: auto-trigger and success navigation', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
    mockGetProject.mockReset();
  });

  it('auto-calls POST /generate on page entry and navigates to Complete on success', async () => {
    mockPostGenerate.mockResolvedValue({
      data: {
        project_id: '550e8400-e29b-41d4-a716-446655440000',
        status: 'generated',
        download_url: '/projects/550e8400-e29b-41d4-a716-446655440000/download',
        generated_at: '2026-01-01T00:00:00Z',
      },
    });

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    // Should show loading state initially
    expect(screen.getByTestId('generate-page')).toBeInTheDocument();

    // Should navigate to complete
    await waitFor(() => {
      expect(screen.getByTestId('complete-page')).toBeInTheDocument();
    });
  });
});
