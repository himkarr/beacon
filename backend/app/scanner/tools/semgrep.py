import json
import subprocess
from pathlib import Path

from app.models.finding import Finding
from app.scanner.normalizer import normalize_semgrep


class SemgrepScanner:

    def scan(self, repository_path: Path) -> list[Finding]:

        command = [
            "semgrep",
            "scan",
            "--config",
            "auto",
            "--json",
            str(repository_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        output = json.loads(result.stdout)

        return output.get("results", [])