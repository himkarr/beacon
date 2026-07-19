from pydantic import BaseModel, Field


class RepositoryProfile(BaseModel):
    languages: set[str] = Field(default_factory=set)
    frameworks: set[str] = Field(default_factory=set)
    package_managers: set[str] =Field(default_factory=set)
    containers: bool = False
    ci: bool = False
    repository_size: int = 0
    total_files: int = 0