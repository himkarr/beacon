import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000",
});

export interface Finding {
  tool: string;
  severity: string;
  title: string;
  message: string;
  file: string;
  line: number | null;
  category: string | null;
  recommendation: string | null;
  package: string | null;
}

export interface ScanResult {
  summary: {
    total: number;
    severity: Record<string, number>;
    tools: Record<string, number>;
  };
  findings: Finding[];
  errors: Record<string, string>;
}

export interface ScanJobResponse {
  job_id: string;
  status: "QUEUED" | "RUNNING" | "COMPLETED" | "FAILED";
  result: ScanResult | null;
  error: string | null;
}

export const scanGithubRepository = (github_url: string) =>
  api.post<Pick<ScanJobResponse, "job_id" | "status">>("/scan/github", { github_url });

export const getScanJob = (jobId: string) =>
  api.get<ScanJobResponse>(`/scan/job/${jobId}`);
