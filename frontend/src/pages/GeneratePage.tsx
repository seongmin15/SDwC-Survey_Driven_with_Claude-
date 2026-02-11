import { useParams } from 'react-router-dom';

export default function GeneratePage() {
  const { projectId } = useParams<{ projectId: string }>();

  return (
    <div data-testid="generate-page">
      <h2 className="text-2xl font-bold mb-4">Generating Project</h2>
      <p className="text-gray-600">Project ID: {projectId}</p>
      <p className="text-gray-600">Generation in progress...</p>
    </div>
  );
}
