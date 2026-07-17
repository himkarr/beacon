from app.shared.models import Finding


def normalize_findings(results):

    findings = []

    for finding in results:

        findings.append(
            Finding(
                tool="Semgrep",
                severity=finding["extra"]["severity"],
                title=finding["check_id"],
                message=finding["extra"]["message"],
                file=finding["path"],
                line=finding["start"]["line"],
            )
        )

    return findings

def normalize_gitleaks(results):

    findings = []

    for item in results:

        findings.append(
            Finding(
                tool="Gitleaks",
                severity="CRITICAL",
                title=item.get("RuleID", "Secret Detected"),
                message=item.get("Description", "Hardcoded secret found"),
                file=item.get("File", ""),
                line=item.get("StartLine"),
            )
        )

    return findings