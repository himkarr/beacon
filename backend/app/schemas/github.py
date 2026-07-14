from pydantic import BaseModel, HttpUrl


class GitHubRepoRequest(BaseModel):
    github_url: HttpUrl


class GitHubRepoResponse(BaseModel):
    status: str
    owner: str
    repository: str
    github_url: str
    branch: str
    last_commit: str
    last_commit_message: str
