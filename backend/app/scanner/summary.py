from collections import Counter


def build_summary(findings):

    severity = Counter()

    tool = Counter()

    for finding in findings:

        severity[finding.severity] += 1
        tool[finding.tool] += 1

    return {
        "total": len(findings),
        "severity": dict(severity),
        "tools": dict(tool),
    }