import {useState} from "react";
import {scanGithubRepository} from "../services/api";

export default function RepoInput() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    try {
      setLoading(true);

      const res = await scanGithubRepository(url);

      setResult(res.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{width: 600}}>
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

      <button onClick={analyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Repository"}
      </button>

      {result && (
        <pre style={{marginTop: 20}}>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}
