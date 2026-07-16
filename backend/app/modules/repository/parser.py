from urllib.parse import urlparse
import re


_GITHUB_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")


def parse_github_url(url: str):
    parsed = urlparse(url)

    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.username
        or parsed.password
        or parsed.port is not None
        or parsed.params
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("Only GitHub repositories are supported.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) != 2:
        raise ValueError("Invalid GitHub repository.")

    owner, repository = parts
    if repository.endswith(".git"):
        repository = repository[:-4]

    if not _GITHUB_NAME.fullmatch(owner) or not _GITHUB_NAME.fullmatch(repository):
        raise ValueError("Invalid GitHub owner or repository name.")

    return {
        "owner": owner,
        "repository": repository,
    }
