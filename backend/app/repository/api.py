from fastapi import APIRouter, BackgroundTasks, HTTPException
from git.exc import GitCommandError
from app.shared.job_store import create_job, get_job, update_job

# Scanner manager instance
from app.scanner.manager import ScanManager
scanner = ScanManager()

# AI analysis service
from app.ai.service import analyze_findings

# Repository utilities
from app.repository.clone import clone_repository
from app.repository.parser import parse_github_url
from app.repository.schemas import GitHubRepoRequest

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "Beacon Backend",
    }


@router.post("/scan/github")
async def scan_repository(data: GitHubRepoRequest, background_tasks: BackgroundTasks):
    try:
        repo = parse_github_url(str(data.github_url))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    job_id = create_job()
    background_tasks.add_task(run_scan_job, job_id, repo)

    return {"job_id": job_id, "status": "QUEUED"}


def run_scan_job(job_id: str, repo: dict[str, str]) -> None:
    update_job(job_id, status="RUNNING")

    try:
        path = clone_repository(repo["owner"], repo["repository"])
        results = scanner.run(path)

        ai_analysis = analyze_findings(results["findings"], results["summary"])
        results["ai_analysis"] = ai_analysis.model_dump()
        
        update_job(job_id, status="COMPLETED", result=results)
    except GitCommandError as exc:
        update_job(
            job_id,
            status="FAILED",
            error="Unable to clone the repository. Verify that it exists and is public.",
        )
    except Exception as exc:
        update_job(job_id, status="FAILED", error=str(exc))


@router.get("/scan/job/{job_id}")
def scan_job(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {"job_id": job_id, **job}
