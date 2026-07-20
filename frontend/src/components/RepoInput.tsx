import { isAxiosError } from "axios";
import { useState } from "react";
import {
  getScanJob,
  scanGithubRepository,
  type ScanJobResponse,
} from "../services/api";

export default function RepoInput() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<ScanJobResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    try {
      setLoading(true);

      const start = await scanGithubRepository(url.trim());

      for (let attempts = 0; attempts < 300; attempts += 1) {
        const job = await getScanJob(start.data.job_id);
        setResult(job.data);

        if (job.data.status === "COMPLETED") return;
        if (job.data.status === "FAILED") {
          throw new Error(job.data.error || "Repository scan failed");
        }

        await new Promise((resolve) => window.setTimeout(resolve, 1000));
      }

      throw new Error("Repository scan timed out");
    } catch (err: unknown) {
      const detail = isAxiosError<{ detail?: string }>(err)
        ? err.response?.data?.detail
        : err instanceof Error
          ? err.message
          : undefined;
      alert(detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ width: 600 }}>
      <input
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="https://github.com/user/repository"
        style={{
          width: "100%",
          padding: "12px",
          marginBottom: "12px",
        }}
      />

      <button onClick={analyze} disabled={loading || !url.trim()}>
        {loading ? "Analyzing..." : "Analyze Repository"}
      </button>

      {result && (
        <pre style={{ marginTop: 20 }}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
