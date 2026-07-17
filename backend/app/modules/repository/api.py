import asyncio

from fastapi import APIRouter, HTTPException
from git.exc import GitCommandError
from app.shared.job_store import create_job, get_job, update_job

# Scanner manager instance
from app.modules.scanner.manager import ScanManager
scanner = ScanManager()

from app.modules.repository.schemas import GitHubRepoRequest
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


@router.post("/scan/github")
async def scan_repository(data: GitHubRepoRequest):
    job_id = create_job()
    update_job(
        job_id,
        status="RUNNING",
    )

    try:
        repo = parse_github_url(str(data.github_url))

        path = await asyncio.to_thread(
            clone_repository,
            repo["owner"],
            repo["repository"],
        )

        info = await asyncio.to_thread(repository_info, path)
        results = scanner.run(path)

        update_job(
            job_id,
            status="COMPLETED",
            result=results,
        )

        return {
            "job_id": job_id,
            "status": "COMPLETED",
        }

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except GitCommandError as exc:
        raise HTTPException(
            status_code=422,
            detail="Unable to clone the repository. Verify that it exists and is public.",
        ) from exc


@router.get("/scan/job/{job_id}")
def scan_job(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job
