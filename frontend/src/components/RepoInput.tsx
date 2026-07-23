import { isAxiosError } from "axios";
import { useState } from "react";
import {
  getScanJob,
  scanGithubRepository,
  type ScanJobResponse,
  type Finding,
  type AIAnalysis,
  type AIFindingExplanation,
} from "../services/api";

const severityColors: Record<string, string> = {
  CRITICAL: "bg-red-500/10 text-red-400 border-red-500/20",
  HIGH: "bg-orange-500/10 text-orange-400 border-orange-500/20",
  MEDIUM: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
  LOW: "bg-green-500/10 text-green-400 border-green-500/20",
  INFO: "bg-blue-500/10 text-blue-400 border-blue-500/20",
};

const toolColors: Record<string, string> = {
  semgrep: "bg-rose-500/10 text-rose-400",
  gitleaks: "bg-emerald-500/10 text-emerald-400",
  bandit: "bg-blue-500/10 text-blue-400",
  trivy: "bg-violet-500/10 text-violet-400",
};

function severityValue(s: string): number {
  const order: Record<string, number> = { CRITICAL: 0, HIGH: 1, MEDIUM: 2, LOW: 3, INFO: 4 };
  return order[s] ?? 99;
}

export default function RepoInput() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<ScanJobResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyze = async () => {
    const trimmed = url.trim();
    if (!trimmed) return;

    try {
      setLoading(true);
      setError(null);
      setResult(null);

      const start = await scanGithubRepository(trimmed);

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
      setError(detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex gap-2">
        <div className="relative flex-1">
          <svg
            className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#52525b] pointer-events-none"
            fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
          >
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !loading && analyze()}
            placeholder="https://github.com/user/repository"
            className="w-full pl-10 pr-4 py-3 bg-[#18181b] border border-[#27272a] rounded-xl text-white placeholder-[#52525b] focus:outline-none focus:border-orange-500/50 focus:ring-1 focus:ring-orange-500/20 transition-all text-sm"
            disabled={loading}
            autoFocus
          />
        </div>
        <button
          onClick={analyze}
          disabled={loading || !url.trim()}
          className="px-5 py-3 bg-orange-500 hover:bg-orange-600 disabled:bg-[#27272a] disabled:text-[#52525b] text-white font-medium rounded-xl transition-all text-sm cursor-pointer disabled:cursor-not-allowed flex items-center gap-2 shrink-0"
        >
          {loading ? (
            <>
              <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Scanning
            </>
          ) : (
            <>
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
              Analyze
            </>
          )}
        </button>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/5 border border-red-500/10 text-red-400 text-sm">
          {error}
        </div>
      )}

      {loading && !result && (
        <div className="text-center py-8">
          <div className="w-8 h-8 border-2 border-orange-500/30 border-t-orange-500 rounded-full animate-spin mx-auto mb-3" />
          <p className="text-sm text-[#a1a1aa]">Scanning repository...</p>
        </div>
      )}

      {result?.result && (result.status === "COMPLETED") && (
        <ResultsDisplay
          summary={result.result.summary}
          findings={result.result.findings}
          ai={result.result.ai_analysis}
          aiError={result.result.ai_error}
        />
      )}
    </div>
  );
}

function ResultsDisplay({
  summary,
  findings,
  ai,
  aiError,
}: {
  summary: { total: number; severity: Record<string, number>; tools: Record<string, number> };
  findings: Finding[];
  ai: AIAnalysis | null;
  aiError: string | null;
}) {
  const sorted = [...findings].sort((a, b) => severityValue(a.severity) - severityValue(b.severity));

  return (
    <div className="space-y-4">
      {ai && (
        <div className="p-5 rounded-xl bg-[#18181b] border border-[#27272a] space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-3">
                <span className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider">AI Analysis</span>
                <span className={`px-2 py-0.5 rounded-md text-xs font-medium border ${
                  ai.risk_level === "CRITICAL" || ai.risk_level === "HIGH"
                    ? "bg-red-500/10 text-red-400 border-red-500/20"
                    : ai.risk_level === "MEDIUM"
                    ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
                    : "bg-green-500/10 text-green-400 border-green-500/20"
                }`}>
                  {ai.risk_level}
                </span>
              </div>
              <p className="text-sm text-[#e4e4e7] leading-relaxed">{ai.executive_summary}</p>
              {ai.top_recommendations.length > 0 && (
                <div className="mt-3 pt-3 border-t border-[#27272a]">
                  <span className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider">Recommendations</span>
                  <ul className="mt-2 space-y-1.5">
                    {ai.top_recommendations.map((r, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-[#e4e4e7]">
                        <span className="text-orange-500 mt-0.5 shrink-0">&#8594;</span>
                        {r}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
            <div className="shrink-0 flex flex-col items-center">
              <div className="relative w-20 h-20">
                <svg className="w-20 h-20 -rotate-90" viewBox="0 0 72 72">
                  <circle cx="36" cy="36" r="30" fill="none" stroke="#27272a" strokeWidth="4" />
                  <circle
                    cx="36" cy="36" r="30" fill="none"
                    stroke={ai.security_score >= 80 ? "#22c55e" : ai.security_score >= 60 ? "#eab308" : ai.security_score >= 40 ? "#ea580c" : "#ef4444"}
                    strokeWidth="4"
                    strokeLinecap="round"
                    strokeDasharray={2 * Math.PI * 30}
                    strokeDashoffset={2 * Math.PI * 30 * (1 - ai.security_score / 100)}
                  />
                </svg>
                <span className="absolute inset-0 flex items-center justify-center text-lg font-bold text-white">
                  {ai.security_score}
                </span>
              </div>
              <span className="text-[10px] text-[#a1a1aa] mt-1">Score</span>
            </div>
          </div>
        </div>
      )}

      {aiError && (
        <div className="p-4 rounded-xl bg-yellow-500/5 border border-yellow-500/10 text-yellow-400 text-sm">
          AI analysis unavailable: {aiError}
        </div>
      )}

      <div className="grid grid-cols-4 gap-3">
        <SummaryCard label="Total" value={summary.total} />
        {Object.entries(summary.severity).map(([sev, count]) => (
          <SummaryCard key={sev} label={sev} value={count} />
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div className="p-4 rounded-xl bg-[#18181b] border border-[#27272a]">
          <span className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider">Severity</span>
          <div className="mt-3 space-y-2">
            {["CRITICAL", "HIGH", "MEDIUM", "LOW"].filter(s => summary.severity[s]).map(s => (
              <div key={s} className="flex items-center justify-between text-sm">
                <span className="text-[#e4e4e7]">{s}</span>
                <div className="flex items-center gap-2">
                  <div className="w-24 h-1.5 rounded-full bg-[#27272a] overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${(summary.severity[s] / summary.total) * 100}%`,
                        backgroundColor:
                          s === "CRITICAL" ? "#ef4444" :
                          s === "HIGH" ? "#f97316" :
                          s === "MEDIUM" ? "#eab308" :
                          "#22c55e"
                      }}
                    />
                  </div>
                  <span className="text-[#a1a1aa] w-6 text-right">{summary.severity[s]}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="p-4 rounded-xl bg-[#18181b] border border-[#27272a]">
          <span className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider">Scanners</span>
          <div className="mt-3 space-y-2">
            {Object.entries(summary.tools).map(([tool, count]) => (
              <div key={tool} className="flex items-center justify-between text-sm">
                <span className={`px-2 py-0.5 rounded text-xs font-medium ${toolColors[tool] || ""}`}>
                  {tool}
                </span>
                <span className="text-[#a1a1aa]">{count}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="rounded-xl bg-[#18181b] border border-[#27272a] overflow-hidden">
        <div className="p-4 border-b border-[#27272a]">
          <span className="text-xs font-semibold text-[#a1a1aa] uppercase tracking-wider">
            Findings ({findings.length})
          </span>
        </div>
        <div className="divide-y divide-[#27272a]">
          {sorted.map((f, i) => (
            <FindingRow key={i} finding={f} ai={ai?.findings?.find(a => a.finding_index === i)} />
          ))}
          {sorted.length === 0 && (
            <div className="p-6 text-center text-sm text-[#52525b]">No findings detected</div>
          )}
        </div>
      </div>
    </div>
  );
}

function SummaryCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="p-4 rounded-xl bg-[#18181b] border border-[#27272a] text-center">
      <div className="text-lg font-bold text-white">{value}</div>
      <div className="text-xs text-[#a1a1aa] mt-0.5">{label}</div>
    </div>
  );
}

function FindingRow({ finding, ai }: { finding: Finding; ai?: AIFindingExplanation }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div>
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 p-4 text-left hover:bg-white/[0.02] transition-colors cursor-pointer"
      >
        <span className={`px-2 py-0.5 rounded text-xs font-medium border ${severityColors[finding.severity] || ""}`}>
          {finding.severity}
        </span>
        <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${toolColors[finding.tool] || ""}`}>
          {finding.tool}
        </span>
        <span className="flex-1 text-sm text-[#e4e4e7] truncate">{finding.title}</span>
        <span className="text-xs text-[#52525b] font-mono hidden sm:block truncate max-w-[200px]">
          {finding.file}:{finding.line ?? "-"}
        </span>
        <svg
          className={`w-4 h-4 text-[#52525b] shrink-0 transition-transform ${expanded ? "rotate-180" : ""}`}
          fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
      {expanded && (
        <div className="px-4 pb-4 pt-0 pl-[72px] space-y-2">
          <p className="text-sm text-[#a1a1aa] leading-relaxed">{finding.message}</p>
          {finding.file && (
            <p className="text-xs text-[#52525b] font-mono">{finding.file}{finding.line ? `:${finding.line}` : ""}</p>
          )}
          {ai && (
            <div className="mt-3 pt-3 border-t border-[#27272a] space-y-2">
              <div>
                <span className="text-[10px] font-semibold text-orange-400 uppercase tracking-wider">AI Analysis</span>
                <p className="text-sm text-[#e4e4e7] mt-1 leading-relaxed">{ai.explanation}</p>
              </div>
              <div>
                <span className="text-[10px] font-semibold text-orange-400 uppercase tracking-wider">Remediation</span>
                <p className="text-sm text-[#e4e4e7] mt-1 leading-relaxed">{ai.remediation}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-[10px] font-semibold text-[#a1a1aa] uppercase tracking-wider">Priority</span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-orange-500/10 text-orange-400">
                  P{ai.priority}
                </span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
