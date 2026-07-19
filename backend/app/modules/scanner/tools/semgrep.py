import json
import subprocess
from pathlib import Path

from app.modules.scanner.base import BaseScanner
from app.modules.scanner.normalizer import normalize_semgrep


class SemgrepScanner(BaseScanner):

    name = "Semgrep"

    category = "SAST"

    supported_languages = {
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "rust",
    }

    def scan(self, repository_path: Path):

        command = [
            "semgrep",
            "scan",
            "--config",
            "auto",
            "--json",
            str(repository_path),
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
            )

            output = json.loads(result.stdout)

            return normalize_semgrep(
                output.get("results", [])
            )

        except subprocess.CalledProcessError:

            return []