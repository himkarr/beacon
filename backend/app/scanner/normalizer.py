from app.models.finding import Finding


def normalize_semgrep(results):

    findings = []

    for item in results:

        extra = item.get("extra", {})

        findings.append(
            Finding(
                tool="Semgrep",
                severity=extra.get("severity", "INFO"),
                title=item.get("check_id", "Unknown"),
                message=extra.get("message", ""),
                file=item.get("path", ""),
                line=item.get("start", {}).get("line"),
            )
        )

    return findings

def normalize_gitleaks(results):

    findings = []

    for item in results:

        findings.append(
            Finding(
                tool="Gitleaks",
                severity="HIGH",
                title=item.get("RuleID", "Secret"),
                message=f"Potential secret detected ({item.get('Description', '')})",
                file=item.get("File", ""),
                line=item.get("StartLine"),
            )
        )

    return findings

def normalize_bandit(results):

    findings = []

    severity_map = {
        "LOW": "LOW",
        "MEDIUM": "MEDIUM",
        "HIGH": "HIGH",
    }

    for item in results:

        findings.append(
            Finding(
                tool="Bandit",
                severity=severity_map.get(
                    item.get("issue_severity", "LOW"),
                    "LOW",
                ),
                title=item.get("test_name", "Bandit Finding"),
                message=item.get("issue_text", ""),
                file=item.get("filename", ""),
                line=item.get("line_number"),
            )
        )

    return findings


def normalize_trivy(results):

    findings = []

    severity_map = {
        "UNKNOWN": "INFO",
        "LOW": "LOW",
        "MEDIUM": "MEDIUM",
        "HIGH": "HIGH",
        "CRITICAL": "CRITICAL",
    }

    for result in results:

        target = result.get("Target", "")

        for vuln in result.get("Vulnerabilities", []):

            findings.append(
                Finding(
                    tool="Trivy",
                    severity=severity_map.get(
                        vuln.get("Severity", "LOW"),
                        "LOW",
                    ),
                    title=vuln.get("VulnerabilityID", ""),
                    message=vuln.get("Title")
                    or vuln.get("Description", ""),
                    file=target,
                    line=None,
                )
            )

        for secret in result.get("Secrets", []):

            findings.append(
                Finding(
                    tool="Trivy",
                    severity=severity_map.get(
                        secret.get("Severity", "LOW"),
                        "LOW",
                    ),
                    title=secret.get("RuleID", "Secret"),
                    message=secret.get("Title", secret.get("Category", "Secret detected")),
                    file=target,
                    line=secret.get("StartLine"),
                )
            )

        for misconfig in result.get("Misconfigurations", []):

            findings.append(
                Finding(
                    tool="Trivy",
                    severity=severity_map.get(
                        misconfig.get("Severity", "LOW"),
                        "LOW",
                    ),
                    title=misconfig.get("ID", "Misconfiguration"),
                    message=misconfig.get("Title", misconfig.get("Message", "")),
                    file=target,
                    line=misconfig.get("StartLine"),
                )
            )

    return findings