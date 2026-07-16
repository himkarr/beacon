import asyncio

from fastapi import APIRouter, HTTPException
from git.exc import GitCommandError

# Scanner manager instance
from app.modules.scanner.manager import ScanManager
scanner = ScanManager()

from app.modules.repository.schemas import GitHubRepoRequest, GitHubRepoResponse
from app.modules.repository.service import (
    parse_github_url,
    clone_repository,
    repository_info,
)

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Beacon Backend",
    }


@router.post("/scan/github", response_model=GitHubRepoResponse)
async def scan_repository(data: GitHubRepoRequest):
    try:
        repo = parse_github_url(str(data.github_url))

        path = await asyncio.to_thread(
            clone_repository,
            repo["owner"],
            repo["repository"],
        )

        info = await asyncio.to_thread(repository_info, path)
        results = scanner.run(path)

        return {
            "status": "success",
            "repository": repo["repository"],
            "owner": repo["owner"],
            # "github_url": str(data.github_url),
            # "branch": info["branch"],
            # "last_commit": info["last_commit"],
            # "last_commit_message": info["last_commit_message"],
            "scan": results,
        }

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitCommandError as exc:
        raise HTTPException(
            status_code=422,
            detail="Unable to clone the repository. Verify that it exists and is public.",
        ) from exc
