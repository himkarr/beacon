import json
import subprocess
from pathlib import Path


class TrivyScanner:

    def scan(self, repository_path: Path):

        command = [
            "trivy",
            "fs",
            "--format",
            "json",
            "--quiet",
            str(repository_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode not in (0, 5):
            raise RuntimeError(result.stderr)

        if not result.stdout.strip():
            return []

        output = json.loads(result.stdout)

        return output.get("Results", [])