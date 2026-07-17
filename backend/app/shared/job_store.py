from uuid import uuid4

jobs = {}


def create_job():
    job_id = str(uuid4())

    jobs[job_id] = {
        "status": "QUEUED",
        "result": None,
        "error": None,
    }

    return job_id


def update_job(job_id, **kwargs):
    jobs[job_id].update(kwargs)


def get_job(job_id):
    return jobs.get(job_id)