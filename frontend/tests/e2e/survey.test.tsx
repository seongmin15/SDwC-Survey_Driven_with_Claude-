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

import { postIntake } from '../../src/api/client';
const mockPostIntake = vi.mocked(postIntake);

describe('E-004: Required field empty → validation error', () => {
  beforeEach(() => {
    mockPostIntake.mockReset();
  });

  it('shows validation errors when submitting with empty required fields', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Find and click the submit button without filling fields
    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    // Validation errors should appear
    await waitFor(() => {
      const errors = screen.getAllByRole('alert');
      expect(errors.length).toBeGreaterThan(0);
    });

    // API should NOT have been called
    expect(mockPostIntake).not.toHaveBeenCalled();
  });
});

describe('E-005: Wrong format → error message', () => {
  beforeEach(() => {
    mockPostIntake.mockReset();
  });

  it('shows error when list field has no items', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Fill text fields but leave list fields empty (scope.in_scope requires min 1 item)
    const nameInput = screen.getByLabelText(/프로젝트 이름/);
    await user.type(nameInput, 'test-project');

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    // Should show validation error for empty required list
    await waitFor(() => {
      const errors = screen.getAllByRole('alert');
      expect(errors.length).toBeGreaterThan(0);
    });
  });
});

describe('E-006: API timeout → error state', () => {
  beforeEach(() => {
    mockPostIntake.mockReset();
  });

  it('shows error state when API call fails', async () => {
    mockPostIntake.mockRejectedValue(new Error('Network timeout'));

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Fill all required fields in the first section at minimum
    const nameInput = screen.getByLabelText(/프로젝트 이름/);
    await user.type(nameInput, 'test-project');

    // Use force-submit data attribute to bypass client validation for this test
    const form = screen.getByTestId('survey-form');
    form.dataset.forceSubmit = 'true';

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    // Should show error state
    await waitFor(() => {
      expect(screen.getByText(/오류|에러|error|실패|failed/i)).toBeInTheDocument();
    });
  });
});

describe('Survey: success → navigate to Generate', () => {
  beforeEach(() => {
    mockPostIntake.mockReset();
  });

  it('navigates to Generate page on successful submission', async () => {
    mockPostIntake.mockResolvedValue({
      data: {
        project_id: 'test-uuid-123',
        status: 'intake_saved',
        created_at: '2026-01-01T00:00:00Z',
      },
    });

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Use force-submit to bypass validation for this navigation test
    const form = screen.getByTestId('survey-form');
    form.dataset.forceSubmit = 'true';

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByTestId('generate-page')).toBeInTheDocument();
    });
  });
});
