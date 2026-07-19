from app.modules.scanner.tools.semgrep import SemgrepScanner
from app.modules.scanner.tools.gitleaks import GitleaksScanner


class ScannerRegistry:

    def resolve(self, profile):

        scanners = [
            GitleaksScanner(),
            SemgrepScanner(),
        ]

        # Python specific scanners
        if "python" in profile.languages:
            pass

        # Node scanners
        if "npm" in profile.package_managers:
            pass

        # Docker scanners
        if profile.containers:
            pass

        return scanners