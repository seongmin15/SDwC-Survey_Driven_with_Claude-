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

import { postGenerate, getProject, getDownloadUrl } from '../../src/api/client';
const mockPostGenerate = vi.mocked(postGenerate);
const mockGetProject = vi.mocked(getProject);
const mockGetDownloadUrl = vi.mocked(getDownloadUrl);

const VALID_UUID = '550e8400-e29b-41d4-a716-446655440000';

/**
 * WCAG 2.1 contrast ratio calculation
 * Uses Tailwind CSS default color palette hex values
 */
function sRGBtoLinear(c: number): number {
  const s = c / 255;
  return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
}

function relativeLuminance(hex: string): number {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return 0.2126 * sRGBtoLinear(r) + 0.7152 * sRGBtoLinear(g) + 0.0722 * sRGBtoLinear(b);
}

function contrastRatio(fg: string, bg: string): number {
  const l1 = relativeLuminance(fg);
  const l2 = relativeLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Tailwind default color palette
const colors: Record<string, string> = {
  white: '#FFFFFF',
  'gray-100': '#F3F4F6',
  'gray-500': '#6B7280',
  'gray-600': '#4B5563',
  'gray-700': '#374151',
  'gray-800': '#1F2937',
  'gray-900': '#111827',
  'red-500': '#EF4444',
  'red-600': '#DC2626',
  'blue-600': '#2563EB',
  'green-500': '#22C55E',
  'red-50': '#FEF2F2',
};

describe('A-014: Normal text contrast ratio >= 4.5:1', () => {
  // All text/background pairings used in the app for normal-sized text
  const normalTextPairings: [string, string, string][] = [
    // [description, foreground color key, background color key]
    ['body text (gray-900 on white)', 'gray-900', 'white'],
    ['secondary text (gray-700 on white)', 'gray-700', 'white'],
    ['muted text (gray-600 on white)', 'gray-600', 'white'],
    ['footer text (gray-600 on gray-100)', 'gray-600', 'gray-100'],
    ['header text (white on gray-800)', 'white', 'gray-800'],
    ['button text (white on blue-600)', 'white', 'blue-600'],
    ['error text (red-600 on white)', 'red-600', 'white'],
    ['error text on red bg (red-600 on red-50)', 'red-600', 'red-50'],
    ['link text (blue-600 on white)', 'blue-600', 'white'],
    ['hint text (gray-500 on white)', 'gray-500', 'white'],
    ['required asterisk (red-600 on white)', 'red-600', 'white'],
    ['field error (red-600 on white)', 'red-600', 'white'],
  ];

  normalTextPairings.forEach(([desc, fg, bg]) => {
    it(`${desc}: contrast ratio >= 4.5:1`, () => {
      const ratio = contrastRatio(colors[fg], colors[bg]);
      expect(ratio).toBeGreaterThanOrEqual(4.5);
    });
  });
});

describe('A-015: Large text contrast ratio >= 3:1', () => {
  // Large text (18px+ or 14px+ bold) pairings
  const largeTextPairings: [string, string, string][] = [
    ['page heading (gray-900 on white)', 'gray-900', 'white'],
    ['section heading (gray-900 on white)', 'gray-900', 'white'],
    ['header h1 (white on gray-800)', 'white', 'gray-800'],
    ['success icon (green-500 on white)', 'green-500', 'white'],
    ['error icon (red-500 on white)', 'red-500', 'white'],
  ];

  largeTextPairings.forEach(([desc, fg, bg]) => {
    it(`${desc}: contrast ratio >= 3:1`, () => {
      const ratio = contrastRatio(colors[fg], colors[bg]);
      expect(ratio).toBeGreaterThanOrEqual(3.0);
    });
  });
});

describe('A-016: Information not conveyed by color alone', () => {
  it('Survey error state uses icon/text in addition to color', async () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // Submit form with empty fields to trigger validation errors
    const user = userEvent.setup();
    const submitButton = screen.getByRole('button', { name: /제출|submit/i });
    await user.click(submitButton);

    await waitFor(() => {
      // Error messages should exist as text (not just color)
      const alerts = screen.getAllByRole('alert');
      expect(alerts.length).toBeGreaterThan(0);
      // Each alert should have text content
      alerts.forEach((alert) => {
        expect(alert.textContent?.trim().length).toBeGreaterThan(0);
      });
    });
  });

  it('Generate error state uses icon + text, not just color', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter initialEntries={[`/generate/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const alert = screen.getByRole('alert');
      expect(alert).toBeInTheDocument();
      // Should have text content
      expect(alert.textContent?.trim().length).toBeGreaterThan(0);
      // Should have an SVG icon (aria-hidden)
      const icon = alert.querySelector('svg[aria-hidden="true"]');
      expect(icon).toBeInTheDocument();
    });
  });

  it('Complete error state uses icon + text, not just color', async () => {
    mockGetProject.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const alert = screen.getByRole('alert');
      expect(alert).toBeInTheDocument();
      expect(alert.textContent?.trim().length).toBeGreaterThan(0);
      const icon = alert.querySelector('svg[aria-hidden="true"]');
      expect(icon).toBeInTheDocument();
    });
  });
});

describe('A-017: Focus indicator on all interactive elements', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
    mockPostGenerate.mockReset();
  });

  it('Survey form inputs have focus ring classes', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // All text inputs, textareas, selects should have focus styles
    const inputs = screen.getAllByRole('textbox');
    inputs.forEach((input) => {
      const className = input.getAttribute('class') || '';
      expect(
        className.includes('focus:ring') || className.includes('focus:outline'),
      ).toBe(true);
    });
  });

  it('Survey submit button has focus ring classes', () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>,
    );

    // The submit button should not have focus:outline-none without a replacement focus:ring
    const submitBtn = screen.getByRole('button', { name: /제출|submit/i });
    const className = submitBtn.getAttribute('class') || '';
    // If focus:outline-none is used, there must be focus:ring as replacement
    if (className.includes('focus:outline-none')) {
      expect(className.includes('focus:ring')).toBe(true);
    }
  });

  it('Complete page buttons have focus ring classes', async () => {
    mockGetProject.mockResolvedValue({
      data: {
        project_id: VALID_UUID,
        project_name: 'Test',
        status: 'generated',
        intake_data: {},
        created_at: '2026-01-01T00:00:00Z',
        generated_at: '2026-01-01T00:01:00Z',
      },
    });
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/Test/)).toBeInTheDocument();
    });

    // Check all buttons and links on Complete page
    const buttons = screen.getAllByRole('button');
    buttons.forEach((btn) => {
      const className = btn.getAttribute('class') || '';
      if (className.includes('focus:outline-none')) {
        expect(className.includes('focus:ring')).toBe(true);
      }
    });

    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      const className = link.getAttribute('class') || '';
      if (className.includes('focus:outline-none')) {
        expect(className.includes('focus:ring')).toBe(true);
      }
    });
  });

  it('Generate page retry button has focus ring classes', async () => {
    mockPostGenerate.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter initialEntries={[`/generate/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const retryBtn = screen.getByRole('button', { name: /재시도|retry/i });
      const className = retryBtn.getAttribute('class') || '';
      if (className.includes('focus:outline-none')) {
        expect(className.includes('focus:ring')).toBe(true);
      }
    });
  });
});
