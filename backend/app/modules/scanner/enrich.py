from app.shared.models import Finding


ENRICHMENT_RULES = {
    "sql injection": {
        "owasp": "A03 Injection",
        "cwe": "CWE-89",
        "cvss": 9.8,
        "severity": "CRITICAL",
        "recommendation": "Use parameterized queries.",
        "references": ["OWASP", "MITRE"],
    },
}


class FindingEnricher:

    def enrich(self, findings: list[Finding]) -> list[Finding]:
        enriched = []

        for finding in findings:
            text = f"{finding.title} {finding.message}".lower()
            rule = next(
                (values for term, values in ENRICHMENT_RULES.items() if term in text),
                None,
            )
            enriched.append(finding.model_copy(update=rule) if rule else finding)

        return enriched

# from app.shared.models import Finding


# class FindingEnricher:

#     def enrich(self, findings: list[Finding]):

#         for finding in findings:

#             if "sql" in finding.title.lower():

#                 finding.owasp = "A03:2021 Injection"
#                 finding.cwe = "CWE-89"

#             elif "xss" in finding.title.lower():

#                 finding.owasp = "A03:2021 Injection"
#                 finding.cwe = "CWE-79"

#         return findings