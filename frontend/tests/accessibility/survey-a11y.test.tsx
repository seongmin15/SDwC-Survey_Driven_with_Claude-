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

describe('A-001: Tab key navigates all form fields in order', () => {
  it('all form inputs are focusable via Tab', async () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Get all visible input/select/textarea/button elements
    const interactiveElements = screen.getByTestId('survey-form')
      .querySelectorAll('input, select, textarea, button');

    expect(interactiveElements.length).toBeGreaterThan(0);

    // All interactive elements should have non-negative tabIndex
    interactiveElements.forEach(el => {
      expect((el as HTMLElement).tabIndex).toBeGreaterThanOrEqual(0);
    });
  });
});

describe('A-002: Enter/Space activates submit button', () => {
  it('submit button is a native button element', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    expect(submitButton.tagName).toBe('BUTTON');
    expect(submitButton).toHaveAttribute('type', 'submit');
  });
});

describe('A-003: All input fields have label or aria-label', () => {
  it('every input has an associated label', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    const inputs = screen.getByTestId('survey-form')
      .querySelectorAll('input, select, textarea');

    inputs.forEach(input => {
      const hasLabel = input.id && document.querySelector(`label[for="${input.id}"]`);
      const hasAriaLabel = input.getAttribute('aria-label');
      const hasAriaLabelledBy = input.getAttribute('aria-labelledby');
      expect(hasLabel || hasAriaLabel || hasAriaLabelledBy).toBeTruthy();
    });
  });
});

describe('A-004: Required fields have required or aria-required', () => {
  it('required fields have the required attribute or aria-required', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // "프로젝트 이름" is required per schema
    const nameInput = screen.getByLabelText(/프로젝트 이름/);
    const isRequired = nameInput.hasAttribute('required') ||
                        nameInput.getAttribute('aria-required') === 'true';
    expect(isRequired).toBe(true);
  });
});

describe('A-005: Validation errors linked via aria-describedby', () => {
  it('error messages are linked to their fields via aria-describedby', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Submit without filling required fields
    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      const nameInput = screen.getByLabelText(/프로젝트 이름/);
      const describedBy = nameInput.getAttribute('aria-describedby');
      expect(describedBy).toBeTruthy();
      const errorEl = document.getElementById(describedBy!);
      expect(errorEl).toBeInTheDocument();
      expect(errorEl!.textContent).toBeTruthy();
    });
  });
});

describe('A-006: Focus moves to first error field on validation', () => {
  it('focuses the first error field after failed validation', async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      // First required field should receive focus
      const nameInput = screen.getByLabelText(/프로젝트 이름/);
      expect(document.activeElement).toBe(nameInput);
    });
  });
});

describe('A-007: Page has title and h1', () => {
  it('has an h1 heading on the Survey page', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toBeInTheDocument();
  });
});
