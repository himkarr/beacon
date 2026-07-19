from pydantic import BaseModel


class RepositoryProfile(BaseModel):
    languages: set[str] = set()
    frameworks: set[str] = set()
    package_managers: set[str] = set()
    containers: bool = False
    ci: bool = False