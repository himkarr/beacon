from app.shared.models import Finding


class FindingAggregator:

    def aggregate(self, findings: list[Finding]):

        unique = {}

        for finding in findings:

            key = (
                finding.title,
                finding.file,
                finding.line,
            )

            if key not in unique:
                unique[key] = finding

        return list(unique.values())