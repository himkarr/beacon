from app.scanner.summary import build_summary

from app.scanner.normalizer import normalize_bandit, normalize_gitleaks, normalize_trivy

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
        errors = {}

        scanners = (
            ("semgrep", self.semgrep.scan, None),
            ("gitleaks", self.gitleaks.scan, normalize_gitleaks),
            ("bandit", self.bandit.scan, normalize_bandit),
            ("trivy", self.trivy.scan, normalize_trivy),
        )

        for name, scan, normalize in scanners:
            try:
                results = scan(repository_path)
                findings.extend(normalize(results) if normalize else results)
            except Exception as exc:
                errors[name] = str(exc)

        return {
            "summary": build_summary(findings),
            "findings": [finding.model_dump() for finding in findings],
            "errors": errors,
        }
