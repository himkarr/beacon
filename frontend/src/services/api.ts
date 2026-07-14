import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000",
});

export interface ScanGithubResponse {
  status: "success";
  owner: string;
  repository: string;
  github_url: string;
  branch: string;
  last_commit: string;
  last_commit_message: string;
}

export const scanGithubRepository = (github_url: string) =>
  api.post<ScanGithubResponse>("/scan/github", { github_url });
