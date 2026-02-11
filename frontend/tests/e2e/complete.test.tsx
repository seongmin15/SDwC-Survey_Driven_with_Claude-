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

describe('E-001: Happy path — Complete page displays project info + download', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('loads project info and shows download button on success', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    // Should show loading initially
    expect(screen.getByTestId('complete-page')).toBeInTheDocument();

    // Should display project info after loading
    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });

    // Should show download button
    expect(
      screen.getByRole('link', { name: /다운로드|download/i }),
    ).toBeInTheDocument();
  });
});

describe('E-002: URL copy button', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    Object.assign(navigator, {
      clipboard: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
  });

  it('copies download URL to clipboard when copy button is clicked', async () => {
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

    const copyButton = screen.getByRole('button', { name: /복사|copy/i });
    await user.click(copyButton);

    expect(navigator.clipboard.writeText).toHaveBeenCalled();
  });
});

describe('E-003: New project start', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
  });

  it('navigates to Survey when "new project" link is clicked', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);

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
    await user.click(newProjectLink);

    await waitFor(() => {
      expect(screen.getByTestId('survey-page')).toBeInTheDocument();
    });
  });
});

describe('E-008: Project fetch failure → error state', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
  });

  it('shows error state when project fetch fails', async () => {
    mockGetProject.mockRejectedValue(new Error('HTTP error! status: 500'));

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
      expect(screen.getByText(/오류가 발생했습니다/)).toBeInTheDocument();
    });
  });
});

describe('E-009: Download network failure', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
  });

  it('shows error notification when download fails', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);
    mockGetDownloadUrl.mockReturnValue(`/projects/${VALID_UUID}/download`);

    // Mock fetch to fail for download URL
    const originalFetch = global.fetch;
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });

    const user = userEvent.setup();
    const downloadButton = screen.getByRole('button', {
      name: /다운로드|download/i,
    });
    await user.click(downloadButton);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });

    global.fetch = originalFetch;
  });
});

describe('E-011: intake_saved status → redirect', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
  });

  it('redirects when project status is intake_saved (not generated)', async () => {
    mockGetProject.mockResolvedValue({
      data: {
        ...mockProjectData.data,
        status: 'intake_saved',
        generated_at: null,
      },
    });

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      // Should redirect away from Complete page
      expect(screen.queryByText(/다운로드|download/i)).not.toBeInTheDocument();
    });

    // Should redirect to Generate page for intake_saved status
    await waitFor(() => {
      expect(
        screen.getByTestId('generate-page') || screen.getByTestId('survey-page'),
      ).toBeInTheDocument();
    });
  });
});

describe('E-015: Browser refresh → state restoration', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
  });

  it('re-fetches project data on page re-entry', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(mockGetProject).toHaveBeenCalledWith(VALID_UUID);
    });

    await waitFor(() => {
      expect(screen.getByText(/Test Project/)).toBeInTheDocument();
    });
  });
});
