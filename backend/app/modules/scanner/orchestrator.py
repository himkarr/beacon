from app.modules.repository.analyzer import RepositoryAnalyzer
from app.modules.scanner.aggregator import FindingAggregator
from app.modules.scanner.enrich import FindingEnricher
from app.modules.scanner.registry import ScannerRegistry


class ScanOrchestrator:

    def run(self, repository_path):

        profile = RepositoryAnalyzer().analyze(repository_path)

        scanners = ScannerRegistry().resolve(profile)

        findings = []

        for scanner in scanners:

            findings.extend(
                scanner.scan(repository_path)
            )

        findings = FindingAggregator().aggregate(findings)

        findings = FindingEnricher().enrich(findings)

        return {
            "profile": profile.model_dump(),
            "total": len(findings),
            "findings": [
                finding.model_dump()
                for finding in findings
            ],
        }