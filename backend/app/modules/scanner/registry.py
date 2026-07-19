from app.modules.scanner.tools.semgrep import SemgrepScanner
from app.modules.scanner.tools.gitleaks import GitleaksScanner

SCANNERS = {
    "all": [
        SemgrepScanner,
        GitleaksScanner,
    ]
}