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

import { getProject, getDownloadUrl } from '../../src/api/client';
const mockGetProject = vi.mocked(getProject);
const mockGetDownloadUrl = vi.mocked(getDownloadUrl);

const VALID_UUID = '550e8400-e29b-41d4-a716-446655440000';

const mockProjectData = {
  data: {
    project_id: VALID_UUID,
    project_name: 'Test Project',
    status: 'generated',
    intake_data: {},
    created_at: '2026-01-01T00:00:00Z',
    generated_at: '2026-01-01T00:01:00Z',
  },
};

describe('A-011: URL copy button has aria-label', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('copy button has descriptive aria-label for screen readers', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });

    const copyButton = screen.getByRole('button', { name: /복사|copy/i });
    expect(copyButton).toHaveAttribute('aria-label');
  });
});

describe('A-012: Download button Tab + Enter activation', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('download button is reachable via Tab', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });

    const downloadLink = screen.getByRole('link', {
      name: /다운로드|download/i,
    });

    // Tab to reach the download button
    await user.tab();
    // Keep tabbing until download link is focused (max 10 tabs)
    let found = false;
    for (let i = 0; i < 10; i++) {
      if (document.activeElement === downloadLink) {
        found = true;
        break;
      }
      await user.tab();
    }

    expect(found).toBe(true);
    expect(downloadLink).toHaveAttribute('href');
  });
});

describe('A-013: New project link Tab accessible', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('"new project" link is reachable via Tab', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    const user = userEvent.setup();
    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });

    const newProjectLink = screen.getByRole('link', {
      name: /새 프로젝트|new project/i,
    });

    // Tab until we reach the link
    let found = false;
    for (let i = 0; i < 15; i++) {
      await user.tab();
      if (document.activeElement === newProjectLink) {
        found = true;
        break;
      }
    }

    expect(found).toBe(true);
  });
});
