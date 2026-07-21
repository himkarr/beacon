import json
import subprocess
import sys
from pathlib import Path


class BanditScanner:

    def scan(self, repository_path: Path):

        command = [
            sys.executable,
            "-m",
            "bandit",
            "-r",
            str(repository_path),
            "-f",
            "json",
            "-q",
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        # 0 = No issues
        # 1 = Issues found
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)

        if not result.stdout.strip():
            return []

        output = json.loads(result.stdout)

        return output.get("results", [])