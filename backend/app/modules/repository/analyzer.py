from pathlib import Path

class RepositoryAnalyzer:

    def analyze(self, repository_path: Path):

        languages = set()

        for file in repository_path.rglob("*"):

            suffix = file.suffix.lower()

            if suffix == ".py":
                languages.add("python")

            elif suffix in [".js", ".jsx"]:
                languages.add("javascript")

            elif suffix in [".ts", ".tsx"]:
                languages.add("typescript")

            elif suffix == ".java":
                languages.add("java")

            elif suffix == ".go":
                languages.add("go")

            elif suffix == ".rs":
                languages.add("rust")

        return {
            "languages": sorted(languages)
        }