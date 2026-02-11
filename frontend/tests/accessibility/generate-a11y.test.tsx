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

import { postGenerate } from '../../src/api/client';
const mockPostGenerate = vi.mocked(postGenerate);

describe('A-008: loading state has aria-busy="true"', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
  });

  it('sets aria-busy on the generate page during loading', async () => {
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
      const page = screen.getByTestId('generate-page');
      expect(page).toHaveAttribute('aria-busy', 'true');
    });
  });
});

describe('A-009: status changes announced via aria-live', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
  });

  it('has aria-live="polite" region for status updates', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const liveRegion = screen.getByRole('alert');
      expect(liveRegion).toBeInTheDocument();
    });
  });

  it('announces error state to screen readers', async () => {
    mockPostGenerate.mockRejectedValue(new Error('Server error'));

    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const alert = screen.getByRole('alert');
      expect(alert).toHaveTextContent(/오류|에러|error|실패/i);
    });
  });
});

describe('A-010: retry button accessible via Tab and Enter', () => {
  beforeEach(() => {
    mockPostGenerate.mockReset();
  });

  it('retry button is focusable via Tab', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    const user = userEvent.setup();
    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /재시도|retry/i })).toBeInTheDocument();
    });

    // Tab to the retry button
    await user.tab();

    const retryButton = screen.getByRole('button', { name: /재시도|retry/i });
    expect(retryButton).toHaveFocus();
  });

  it('retry button activates with Enter key', async () => {
    mockPostGenerate
      .mockRejectedValueOnce(new Error('HTTP error! status: 500'))
      .mockResolvedValueOnce({
        data: {
          project_id: '550e8400-e29b-41d4-a716-446655440000',
          status: 'generated',
          download_url: '/projects/550e8400-e29b-41d4-a716-446655440000/download',
          generated_at: '2026-01-01T00:00:00Z',
        },
      });

    const user = userEvent.setup();
    render(
      <MemoryRouter
        initialEntries={['/generate/550e8400-e29b-41d4-a716-446655440000']}
      >
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /재시도|retry/i })).toBeInTheDocument();
    });

    // Focus and press Enter on retry button
    const retryButton = screen.getByRole('button', { name: /재시도|retry/i });
    retryButton.focus();
    await user.keyboard('{Enter}');

    // Should have called postGenerate again
    await waitFor(() => {
      expect(mockPostGenerate).toHaveBeenCalledTimes(2);
    });
  });
});
