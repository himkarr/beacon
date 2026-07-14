from urllib.parse import urlparse


def parse_github_url(url: str):
    parsed = urlparse(str(url))

    if parsed.netloc != "github.com":
        raise ValueError("Only GitHub repositories are supported.")

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[0]
    repository = parts[1].replace(".git", "")

    return {
        "owner": owner,
        "repository": repository,
    }