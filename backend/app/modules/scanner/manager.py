from app.modules.scanner.tools.semgrep import SemgrepScanner
from app.modules.scanner.tools.gitleaks import GitleaksScanner
from app.modules.scanner.normalizer import normalize_findings


class ScanManager:

    def __init__(self):

        self.scanners = [
            SemgrepScanner(),
            GitleaksScanner(),
        ]

    def run(self, repository_path):

        findings = []

        for scanner in self.scanners:
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