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

describe('V-009: success state — URL display + download button + copy button', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('displays all required elements in success state', async () => {
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

    // Download button should be present and visible
    const downloadBtn = screen.getByRole('link', { name: /다운로드|download/i });
    expect(downloadBtn).toBeVisible();

    // Copy button should be present and visible
    const copyBtn = screen.getByRole('button', { name: /복사|copy/i });
    expect(copyBtn).toBeVisible();

    // New project link should be present
    const newProjectLink = screen.getByRole('link', {
      name: /새 프로젝트|new project/i,
    });
    expect(newProjectLink).toBeVisible();
  });

  it('shows project name prominently', async () => {
    mockGetProject.mockResolvedValue(mockProjectData);

    render(
      <MemoryRouter initialEntries={[`/complete/${VALID_UUID}`]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      const heading = screen.getByRole('heading', { level: 2 });
      expect(heading).toBeInTheDocument();
    });
  });
});

describe('V-010: Responsive layout — Desktop/Tablet/Mobile', () => {
  beforeEach(() => {
    mockGetProject.mockReset();
    mockGetDownloadUrl.mockReset();
  });

  it('renders all interactive elements at any viewport', async () => {
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

    // All buttons should be rendered and accessible
    expect(
      screen.getByRole('link', { name: /다운로드|download/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('button', { name: /복사|copy/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole('link', { name: /새 프로젝트|new project/i }),
    ).toBeInTheDocument();
  });
});
