from .clone import clone_repository
from .info import repository_info
from .parser import parse_github_url


class RepositoryService:

    def prepare(self, github_url: str):

        repo = parse_github_url(github_url)

        path = clone_repository(
            repo["owner"],
            repo["repository"],
        )

        info = repository_info(path)

        return {
            **repo,
            **info,
            "path": path,
        }