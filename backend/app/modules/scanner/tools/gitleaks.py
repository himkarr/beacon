import json
import subprocess
from pathlib import Path

from app.modules.scanner.base import BaseScanner
from app.modules.scanner.normalizer import normalize_gitleaks


class GitleaksScanner(BaseScanner):

    name = "Gitleaks"

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

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            findings = json.loads(result.stdout or "[]")

            return normalize_gitleaks(findings)

        except subprocess.CalledProcessError:
            return []