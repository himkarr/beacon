from pathlib import Path

from app.shared.models.repository import RepositoryProfile


class RepositoryAnalyzer:

    def analyze(self, repository_path: Path) -> RepositoryProfile:

        profile = RepositoryProfile()

        for file in repository_path.rglob("*"):

            if not file.is_file():
                continue

            suffix = file.suffix.lower()
            name = file.name.lower()

            match suffix:
                case ".py":
                    profile.languages.add("python")

                case ".js":
                    profile.languages.add("javascript")

                case ".jsx":
                    profile.languages.add("javascript")

                case ".ts":
                    profile.languages.add("typescript")

                case ".tsx":
                    profile.languages.add("typescript")

                case ".java":
                    profile.languages.add("java")

                case ".go":
                    profile.languages.add("go")

                case ".rs":
                    profile.languages.add("rust")

            match name:

                case "package.json":
                    profile.package_managers.add("npm")

                case "requirements.txt":
                    profile.package_managers.add("pip")

                case "pyproject.toml":
                    profile.package_managers.add("pip")

                case "pom.xml":
                    profile.package_managers.add("maven")

                case "cargo.toml":
                    profile.package_managers.add("cargo")

                case "dockerfile":
                    profile.containers = True

                case "github":
                    profile.ci = True

        return profile