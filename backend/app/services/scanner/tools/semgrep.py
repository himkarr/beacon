import json
import subprocess
from pathlib import Path


def run_semgrep(repository_path: Path):
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

        return output.get("results", [])

    except subprocess.CalledProcessError as e:
        print(e.stderr)
        return []