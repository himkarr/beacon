from app.modules.scanner.tools.semgrep import SemgrepScanner
from app.modules.scanner.tools.gitleaks import GitleaksScanner

ALL_SCANNERS = [
    SemgrepScanner,
    GitleaksScanner,
]

class ScannerRegistry:

    def resolve(self, profile):

        scanners = []

        for scanner_cls in ALL_SCANNERS:

            scanner = scanner_cls()

            if not scanner.supported_languages:
                scanners.append(scanner)
                continue

            if (
                profile.languages
                &
                scanner.supported_languages
            ):
                scanners.append(scanner)

        return scanners