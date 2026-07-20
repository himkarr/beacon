from app.scanner.summary import build_summary

from app.scanner.normalizer import (
    normalize_semgrep,
    normalize_gitleaks,
    normalize_bandit,
    normalize_trivy,
)

from app.scanner.tools.semgrep import SemgrepScanner
from app.scanner.tools.gitleaks import GitleaksScanner
from app.scanner.tools.bandit import BanditScanner
from app.scanner.tools.trivy import TrivyScanner

class ScanManager:

    def __init__(self):

        self.semgrep = SemgrepScanner()
        self.gitleaks = GitleaksScanner()
        self.bandit = BanditScanner()
        self.trivy = TrivyScanner()

    def run(self, repository_path):

        findings = []

        findings.extend(
            normalize_semgrep(
                self.semgrep.scan(repository_path)
            )
        )

        findings.extend(
            normalize_gitleaks(
                self.gitleaks.scan(repository_path)
            )
        )

        findings.extend(
            normalize_bandit(
                self.bandit.scan(repository_path)
            )
        )

        findings.extend(
            normalize_trivy(
                self.trivy.scan(repository_path)
            )
        )

        return {
    "summary": build_summary(findings),
    "findings": [f.model_dump() for f in findings],
}