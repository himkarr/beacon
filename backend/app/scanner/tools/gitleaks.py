import json
import subprocess
from pathlib import Path


class GitleaksScanner:

    def scan(self, repository_path: Path):

        command = [
            "gitleaks",
            "detect",
            "--source",
            str(repository_path),
            "--report-format",
            "json",
            "--report-path",
            "-",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        # Gitleaks returns exit code 1 when leaks are found.
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        if not result.stdout.strip():
            return []

        return json.loads(result.stdout)