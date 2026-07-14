import asyncio
from pathlib import Path
import unittest
from unittest.mock import patch

from app.api.routes import scan_repository
from app.schemas.github import GitHubRepoRequest
from app.services.github import parse_github_url


async def run_synchronously(function, *args):
    return function(*args)


class GitHubServiceTests(unittest.TestCase):
    def test_parse_github_url_accepts_repository_urls(self):
        self.assertEqual(
            parse_github_url("https://github.com/octocat/Hello-World"),
            {"owner": "octocat", "repository": "Hello-World"},
        )
        self.assertEqual(
            parse_github_url("https://github.com/octocat/Hello-World.git"),
            {"owner": "octocat", "repository": "Hello-World"},
        )

    def test_parse_github_url_rejects_unsafe_or_non_repository_urls(self):
        for url in (
            "http://github.com/octocat/Hello-World",
            "https://github.com/octocat/Hello-World/issues",
            "https://github.com/../Hello-World",
            "https://example.com/octocat/Hello-World",
        ):
            with self.subTest(url=url), self.assertRaises(ValueError):
                parse_github_url(url)

    def test_scan_repository_returns_metadata(self):
        with (
            patch("app.api.routes.asyncio.to_thread", new=run_synchronously),
            patch(
                "app.api.routes.clone_repository",
                return_value=Path("/tmp/test-repository"),
            ),
            patch(
                "app.api.routes.repository_info",
                return_value={
                    "branch": "main",
                    "last_commit": "a" * 40,
                    "last_commit_message": "Initial commit",
                },
            ),
        ):
            result = asyncio.run(
                scan_repository(
                    GitHubRepoRequest(
                        github_url="https://github.com/octocat/Hello-World"
                    )
                )
            )

        self.assertEqual(
            result,
            {
                "status": "success",
                "owner": "octocat",
                "repository": "Hello-World",
                "github_url": "https://github.com/octocat/Hello-World",
                "branch": "main",
                "last_commit": "a" * 40,
                "last_commit_message": "Initial commit",
            },
        )


if __name__ == "__main__":
    unittest.main()
