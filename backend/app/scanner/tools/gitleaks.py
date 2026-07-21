import json
import os
import subprocess
import tempfile
from pathlib import Path


class GitleaksScanner:

    def scan(self, repository_path: Path):

        report_path = None

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as report_file:
            report_path = report_file.name

        command = [
            "gitleaks",
            "detect",
            "--source",
            str(repository_path),
            "--report-format",
            "json",
            "--report-path",
            report_path,
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
            )

            # Gitleaks returns exit code 1 when leaks are found.
            if result.returncode not in (0, 1):
                raise RuntimeError(result.stderr)

            if not report_path or not os.path.exists(report_path):
                return []

            with open(report_path, encoding="utf-8") as report:
                content = report.read().strip()

            if not content:
                return []

            return json.loads(content)
        finally:
            if report_path and os.path.exists(report_path):
                os.unlink(report_path)