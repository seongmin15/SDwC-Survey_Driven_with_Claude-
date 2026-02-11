import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getProject, getDownloadUrl } from '../api/client';
import type { ProjectData } from '../types/api';

type State = 'loading' | 'success' | 'error';

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function isValidUUID(id: string | undefined): id is string {
  return !!id && UUID_REGEX.test(id);
}

export default function CompletePage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [state, setState] = useState<State>('loading');
  const [project, setProject] = useState<ProjectData | null>(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [downloadError, setDownloadError] = useState('');

  const fetchProject = useCallback(async (id: string) => {
    setState('loading');
    setErrorMessage('');
    try {
      const response = await getProject(id);
      const data = response.data;
      
      if (data.status !== 'generated') {
        if (data.status === 'intake_saved') {
          navigate(`/generate/${id}`);
        } else {
          navigate('/');
        }
        return;
      }
      
      setProject(data);
      setState('success');
    } catch (error) {
      setState('error');
      setErrorMessage(error instanceof Error ? error.message : String(error));
    }
  }, [navigate]);

  useEffect(() => {
    if (!isValidUUID(projectId)) {
      navigate('/');
      return;
    }
    fetchProject(projectId);
  }, [projectId, navigate, fetchProject]);

  const handleCopy = async () => {
    if (!projectId) return;
    const url = getDownloadUrl(projectId);
    const fullUrl = `${window.location.origin}${url}`;
    await navigator.clipboard.writeText(fullUrl);
  };

  const handleDownload = async () => {
    if (!projectId) return;
    setDownloadError('');
    try {
      const url = getDownloadUrl(projectId);
      const response = await fetch(url);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const blob = await response.blob();
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = blobUrl;
      a.download = `${projectId}.zip`;
      a.click();
      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      setDownloadError(error instanceof Error ? error.message : String(error));
    }
  };

  return (
    <div data-testid="complete-page" className="flex flex-col items-center justify-center py-16">
      <div className="max-w-md w-full text-center">
        {state === 'loading' && (
          <div role="status" className="flex flex-col items-center">
            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-6" />
            <p className="text-gray-600">프로젝트 정보를 불러오는 중...</p>
          </div>
        )}

        {state === 'error' && (
          <div role="alert" className="bg-white rounded-lg shadow-lg p-8">
            <svg className="w-16 h-16 mx-auto mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">오류가 발생했습니다</h2>
            <p className="text-gray-600 mb-6">{errorMessage}</p>
          </div>
        )}

        {state === 'success' && project && (
          <div className="bg-white rounded-lg shadow-lg p-8">
            <svg className="w-16 h-16 mx-auto mb-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">{project.project_name}</h2>
            <p className="text-gray-600 mb-6">프로젝트가 성공적으로 생성되었습니다.</p>

            <div className="space-y-3">
              <button
                onClick={handleDownload}
                className="w-full bg-blue-600 text-white font-medium py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
                aria-label="ZIP 파일 다운로드"
              >
                다운로드
              </button>

              {downloadError && (
                <div role="alert" className="text-red-600 text-sm mt-2">
                  {downloadError}
                </div>
              )}

              <button
                onClick={handleCopy}
                aria-label="URL 클립보드에 복사"
                className="w-full bg-gray-100 text-gray-700 font-medium py-3 px-4 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-colors"
              >
                URL 복사
              </button>

              <Link
                to="/"
                className="block w-full text-center text-blue-600 font-medium py-3 px-4 rounded-md hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
              >
                새 프로젝트 시작
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
