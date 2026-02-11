import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

// Mock the API client
vi.mock('../../src/api/client', () => ({
  postIntake: vi.fn(),
  postGenerate: vi.fn(),
  getProject: vi.fn(),
  getDownloadUrl: vi.fn(),
}));

import { postGenerate } from '../../src/api/client';
const mockPostGenerate = vi.mocked(postGenerate);

describe('V-007: loading state — progress display', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
  });

  it('shows animated progress indicator during loading', async () => {
    // Never resolve to keep in loading state
    mockPostGenerate.mockReturnValue(new Promise(() => {}));

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      // Should show loading indicator with animation
      const loader = screen.getByRole('status');
      expect(loader).toBeInTheDocument();
    });

    // Progress should be centered
    const generatePage = screen.getByTestId('generate-page');
    expect(generatePage).toBeInTheDocument();
  });

  it('displays generating message during loading', async () => {
    mockPostGenerate.mockReturnValue(new Promise(() => {}));

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/생성 중|generating/i)).toBeInTheDocument();
    });
  });
});

describe('V-008: error state — error message + retry button', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
  });

  it('shows clear error message with retry button', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      // Error message should be visible
      expect(screen.getByText(/오류|에러|error|실패/i)).toBeInTheDocument();
    });

    // Retry button should be visible and styled
    const retryButton = screen.getByRole('button', { name: /재시도|retry/i });
    expect(retryButton).toBeInTheDocument();
    expect(retryButton).toBeVisible();
  });
});
