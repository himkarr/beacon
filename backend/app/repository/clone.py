from pathlib import Path
import shutil
from uuid import uuid4

from git import Repo


BASE_DIR = Path(__file__).resolve().parents[2] / "uploads" / "repos"


def clone_repository(owner: str, repository: str) -> Path:
    """Clone a repository into an isolated directory for one scan."""
    repo_path = BASE_DIR / f"{owner}-{repository}-{uuid4().hex}"
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    try:
        Repo.clone_from(
            f"https://github.com/{owner}/{repository}.git",
            repo_path,
            depth=1,
        )
    except Exception:
        shutil.rmtree(repo_path, ignore_errors=True)
        raise

    return repo_path
