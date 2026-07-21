SYSTEM_INSTRUCTION = """You are an application security expert reviewing automated
scanner output for a codebase. You will be given a JSON list of findings from
Semgrep, Gitleaks, Bandit, and Trivy. Respond with ONLY valid JSON matching the
schema you are given — no markdown fences, no commentary outside the JSON.
Keep explanations understandable for a developer with limited security background.
Be concise but specific — reference the actual finding titles, not generic advice."""


def build_prompt(findings: list[dict], summary: dict) -> str:
    return f"""Findings summary: {summary}

Findings (JSON array, indices correspond to finding_index in your output):
{findings}

Analyze these findings and respond with JSON matching this shape:
{{
  "executive_summary": "...",
  "security_score": 0-100,
  "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
  "top_recommendations": ["...", "..."],
  "findings": [
    {{"finding_index": 0, "explanation": "...", "remediation": "...", "priority": 1}}
  ]
}}"""