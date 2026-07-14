import { isAxiosError } from "axios";
import { useState } from "react";
import { scanGithubRepository, type ScanGithubResponse } from "../services/api";

export default function RepoInput() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<ScanGithubResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    try {
      setLoading(true);

      const res = await scanGithubRepository(url.trim());

      setResult(res.data);
    } catch (err: unknown) {
      const detail = isAxiosError<{ detail?: string }>(err)
        ? err.response?.data?.detail
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
