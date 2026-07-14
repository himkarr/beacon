from fastapi import APIRouter, HTTPException

from app.schemas.github import GitHubRepoRequest, GitHubRepoResponse
from app.services.github_service import parse_github_url

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Beacon Backend"
    }


@router.post("/scan/github", response_model=GitHubRepoResponse)
async def scan_repository(data: GitHubRepoRequest):
    try:
        repo = parse_github_url(str(data.github_url))

        return {
            "status": "success",
            "owner": repo["owner"],
            "repository": repo["repository"],
            "github_url": str(data.github_url),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))