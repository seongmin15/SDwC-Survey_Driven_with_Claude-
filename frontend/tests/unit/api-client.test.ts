import { describe, it, expect, vi, beforeEach } from 'vitest';
import { postIntake, postGenerate, getProject, getDownloadUrl } from '../../src/api/client';

describe('API Client', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  it('uses VITE_API_URL as base URL', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: {} }),
    });
    vi.stubGlobal('fetch', mockFetch);

    await getProject('test-id');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringContaining('/projects/test-id'),
      expect.any(Object),
    );
  });

  it('postIntake calls POST /intakes', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: { project_id: 'abc', status: 'intake_saved', created_at: '' } }),
    });
    vi.stubGlobal('fetch', mockFetch);

    const result = await postIntake({ project: { name: 'test' } });

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/intakes$/),
      expect.objectContaining({ method: 'POST' }),
    );
    expect(result.data.project_id).toBe('abc');
  });

  it('postGenerate calls POST /generate', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: { project_id: 'abc', status: 'generated' } }),
    });
    vi.stubGlobal('fetch', mockFetch);

    const result = await postGenerate('abc');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/generate$/),
      expect.objectContaining({ method: 'POST' }),
    );
    expect(result.data.project_id).toBe('abc');
  });

  it('getProject calls GET /projects/:id', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: { project_id: 'abc' } }),
    });
    vi.stubGlobal('fetch', mockFetch);

    const result = await getProject('abc');

    expect(mockFetch).toHaveBeenCalledWith(
      expect.stringMatching(/\/projects\/abc$/),
      expect.objectContaining({ method: 'GET' }),
    );
    expect(result.data.project_id).toBe('abc');
  });

  it('getDownloadUrl returns correct download URL', () => {
    const url = getDownloadUrl('abc');
    expect(url).toContain('/projects/abc/download');
  });

  it('throws ApiError on non-ok response', async () => {
    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
      json: () => Promise.resolve({ error: 'PROJECT_NOT_FOUND', message: 'Not found' }),
    });
    vi.stubGlobal('fetch', mockFetch);

    await expect(getProject('nonexistent')).rejects.toThrow();
  });
});
