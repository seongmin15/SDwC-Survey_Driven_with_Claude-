// Common API response wrapper
export interface ApiResponse<T> {
  data: T;
}

export interface ApiError {
  error: string;
  message: string;
}

// POST /intakes
export type IntakeData = Record<string, unknown>;

export interface IntakeResult {
  project_id: string;
  status: string;
  created_at: string;
}

export type PostIntakeResponse = ApiResponse<IntakeResult>;

// POST /generate
export interface GenerateResult {
  project_id: string;
  status: string;
  download_url: string;
  generated_at: string;
}

export type PostGenerateResponse = ApiResponse<GenerateResult>;

// GET /projects/:id
export interface ProjectData {
  project_id: string;
  project_name: string;
  status: string;
  intake_data: Record<string, unknown>;
  created_at: string;
  generated_at: string | null;
}

export type ProjectResponse = ApiResponse<ProjectData>;
