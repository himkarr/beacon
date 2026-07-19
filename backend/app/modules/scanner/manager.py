from app.modules.repository.analyzer import RepositoryAnalyzer
from app.modules.scanner.tools.bandit import BanditScanner
from app.modules.scanner.tools.semgrep import SemgrepScanner
from app.modules.scanner.tools.gitleaks import GitleaksScanner
from app.modules.scanner.normalizer import normalize_findings


class ScanManager:

    def run(self, repository_path):

        findings = []

        analysis = RepositoryAnalyzer().analyze(repository_path)
        languages = analysis["languages"]

        scanners = [
            SemgrepScanner(),
            GitleaksScanner(),
        ]

        if "python" in languages:
            scanners.append(BanditScanner())

        for scanner in scanners:
            try:
                findings.extend(
                    scanner.scan(repository_path)
                )
            except Exception as e:
                 print(f"{scanner.name} failed: {e}")

        return {
            "total": len(findings),
            "findings": [
                finding.model_dump()
                for finding in findings
            ],
        }
