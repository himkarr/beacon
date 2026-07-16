def normalize_findings(findings):
    normalized = []

    for finding in findings:
        normalized.append({
            "tool": "Semgrep",
            "title": finding.get("check_id"),
            "severity": finding.get("extra", {}).get("severity"),
            "message": finding.get("extra", {}).get("message"),
            "file": finding.get("path"),
            "line": finding.get("start", {}).get("line"),
        })

    return {
        "total": len(normalized),
        "findings": normalized,
    }