import { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { postGenerate } from '../api/client';

type State = 'idle' | 'loading' | 'success' | 'error';

const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

function isValidUUID(id: string | undefined): id is string {
  return !!id && UUID_REGEX.test(id);
}

export default function GeneratePage() {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [state, setState] = useState<State>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const triggerGenerate = useCallback(async (id: string) => {
    setState('loading');
    setErrorMessage('');

    try {
      await postGenerate(id);
      setState('success');
      navigate(`/complete/${id}`);
    } catch (error) {
      const msg = error instanceof Error ? error.message : String(error);

      if (msg.includes('409')) {
        navigate(`/complete/${id}`);
        return;
      }

      setState('error');
      setErrorMessage(msg);
    }
  }, [navigate]);

  useEffect(() => {
    if (!isValidUUID(projectId)) {
      navigate('/');
      return;
    }
    triggerGenerate(projectId);
  }, [projectId, navigate, triggerGenerate]);

  const handleRetry = () => {
    if (isValidUUID(projectId)) {
      triggerGenerate(projectId);
    }
  };

  return (
    <div
      data-testid="generate-page"
      aria-busy={state === 'loading'}
      className="flex flex-col items-center justify-center py-16"
    >
      <div className="max-w-md w-full text-center">
        {(state === 'idle' || state === 'loading') && (
          <div role="status" className="flex flex-col items-center">
            <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              프로젝트 생성 중
            </h2>
            <p className="text-gray-600">잠시만 기다려주세요...</p>
          </div>
        )}

        {state === 'error' && (
          <div role="alert" className="bg-white rounded-lg shadow-lg p-8">
            <svg
              className="w-16 h-16 mx-auto mb-4 text-red-500"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              오류가 발생했습니다
            </h2>
            <p className="text-gray-600 mb-6">{errorMessage}</p>
            <button
              onClick={handleRetry}
              className="w-full bg-blue-600 text-white font-medium py-3 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
            >
              재시도
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
