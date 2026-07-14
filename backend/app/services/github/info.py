from pathlib import Path

from git import Repo


def repository_info(path: Path) -> dict[str, str]:
    """Return the metadata needed by a repository scan response."""
    repository = Repo(path)
    commit = repository.head.commit

    try:
        branch = repository.active_branch.name
    except TypeError:
        branch = "detached"

    return {
        "branch": branch,
        "last_commit": commit.hexsha,
        "last_commit_message": commit.message.strip(),
    }
