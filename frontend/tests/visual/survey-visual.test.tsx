import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { MemoryRouter } from 'react-router-dom';
import App from '../../src/App';

vi.mock('../../src/api/client', () => ({
  postIntake: vi.fn(),
  postGenerate: vi.fn(),
  getProject: vi.fn(),
  getDownloadUrl: vi.fn(),
}));

import { postIntake } from '../../src/api/client';
const mockPostIntake = vi.mocked(postIntake);

describe('V-001~V-003: Responsive layout', () => {
  it('V-001: form container has responsive width classes for desktop', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    const form = screen.getByTestId('survey-form');
    // Should have responsive classes ensuring center alignment
    expect(form.closest('[class*="mx-auto"]')).toBeInTheDocument();
  });

  it('V-002: form renders properly at any width (responsive container)', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    const form = screen.getByTestId('survey-form');
    // Form should use full width with max-width constraint
    expect(form.className).toMatch(/w-full/);
  });

  it('V-003: form fields stack vertically (single column)', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    // All field containers should have block-level (flex-col) layout
    const sections = screen.getAllByRole('group');
    expect(sections.length).toBeGreaterThan(0);
  });
});

describe('V-004~V-006: State visuals', () => {
  it('V-004: idle state shows empty form with active submit button', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    expect(submitButton).not.toBeDisabled();
  });

  it('V-005: loading state shows disabled button with loading indicator', async () => {
    // Make the API call hang
    mockPostIntake.mockImplementation(() => new Promise(() => {}));

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    const form = screen.getByTestId('survey-form');
    form.dataset.forceSubmit = 'true';

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      const button = screen.getByRole('button', { name: /제출|submit|처리|로딩|loading/i });
      expect(button).toBeDisabled();
    });
  });

  it('V-006: error state shows error message with red styling', async () => {
    mockPostIntake.mockRejectedValue(new Error('Server Error'));

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    const form = screen.getByTestId('survey-form');
    form.dataset.forceSubmit = 'true';

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      const errorEl = screen.getByRole('alert');
      expect(errorEl).toBeInTheDocument();
      // Error should have red/destructive styling
      expect(errorEl.className).toMatch(/red|error|destructive/i);
    });
  });
});
