def run_semgrep(repository_path):

    return [
        {
            "tool": "Semgrep",
            "severity": "HIGH",
            "title": "Dummy SQL Injection",
            "file": "app.py",
            "line": 21,
        }
    ]