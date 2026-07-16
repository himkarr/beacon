from app.services.scanner.tools.semgrep import run_semgrep
from app.services.scanner.tools.gitleaks import run_gitleaks
from app.services.scanner.normalizer import normalize_findings


class ScanManager:

    def run(self, repository_path):
        findings = []

        findings.extend(run_semgrep(repository_path))
        findings.extend(run_gitleaks(repository_path))

        return normalize_findings(findings)