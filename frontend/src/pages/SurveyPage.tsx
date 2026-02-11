import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import DynamicForm from '../components/DynamicForm';
import schema from '../data/intake-schema.json';
import { postIntake } from '../api/client';
import { buildNestedData } from '../utils/form-data';
import type { IntakeSchema } from '../types/schema';

export default function SurveyPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async (formValues: Record<string, any>) => {
    setStatus('loading');
    setApiError(null);
    try {
      const intakeData = buildNestedData(formValues);
      const result = await postIntake(intakeData);
      setStatus('success');
      navigate(`/generate/${result.data.project_id}`);
    } catch (err) {
      setStatus('error');
      const errorMessage = err instanceof Error ? err.message : '알 수 없는 오류';
      setApiError(`오류가 발생했습니다: ${errorMessage}`);
    }
  };

  return (
    <div data-testid="survey-page">
      <DynamicForm
        schema={schema as IntakeSchema}
        onSubmit={handleSubmit}
        status={status}
        apiError={apiError}
      />
    </div>
  );
}
