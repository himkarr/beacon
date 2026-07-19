import json
import subprocess
from pathlib import Path

from app.modules.scanner.base import BaseScanner
from app.shared.models import Finding


class BanditScanner(BaseScanner):

    name = "Bandit"

    def scan(self, repository_path: Path) -> list[Finding]:
        command = [
            "bandit",
            "-r",
            str(repository_path),
            "-f",
            "json",
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )
            output = json.loads(result.stdout or "{}")
        except (json.JSONDecodeError, OSError):
            return []

        return [
            Finding(
                tool=self.name,
                severity=item.get("issue_severity", "MEDIUM"),
                title=item.get("test_name", item.get("test_id", "Bandit finding")),
                message=item.get("issue_text", ""),
                file=item.get("filename", ""),
                line=item.get("line_number"),
            )
            for item in output.get("results", [])
        ]
