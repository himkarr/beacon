import asyncio

from fastapi import APIRouter, HTTPException
from git.exc import GitCommandError

from app.schemas.github import GitHubRepoRequest, GitHubRepoResponse
from app.services.github import (
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

        return {
            "status": "success",
            "owner": repo["owner"],
            "repository": repo["repository"],
            "github_url": f"https://github.com/{repo['owner']}/{repo['repository']}",
            "branch": info["branch"],
            "last_commit": info["last_commit"],
            "last_commit_message": info["last_commit_message"],
        }

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitCommandError as exc:
        raise HTTPException(
            status_code=422,
            detail="Unable to clone the repository. Verify that it exists and is public.",
        ) from exc
