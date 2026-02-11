import type {
  IntakeData,
  PostIntakeResponse,
  PostGenerateResponse,
  ProjectResponse,
} from '../types/api';

const BASE_URL = import.meta.env.VITE_API_URL || '';

export async function postIntake(intakeData: IntakeData): Promise<PostIntakeResponse> {
  const response = await fetch(`${BASE_URL}/intakes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ intake_data: intakeData }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function postGenerate(projectId: string): Promise<PostGenerateResponse> {
  const response = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ project_id: projectId }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export async function getProject(id: string): Promise<ProjectResponse> {
  const response = await fetch(`${BASE_URL}/projects/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export function getDownloadUrl(id: string): string {
  return `${BASE_URL}/projects/${id}/download`;
}
