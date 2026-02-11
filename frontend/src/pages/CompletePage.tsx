import { useParams } from 'react-router-dom';

export default function CompletePage() {
  const { projectId } = useParams<{ projectId: string }>();

  return (
    <div data-testid="complete-page">
      <h2 className="text-2xl font-bold mb-4">Project Complete</h2>
      <p className="text-gray-600">Project ID: {projectId}</p>
      <p className="text-gray-600">Your project is ready for download.</p>
    </div>
  );
}
