def run_gitleaks(repository_path):

    return [
        {
            "tool": "Gitleaks",
            "severity": "CRITICAL",
            "title": "Hardcoded API Key",
            "file": ".env",
            "line": 3,
        }
    ]