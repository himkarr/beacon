from abc import ABC, abstractmethod
from pathlib import Path

from app.shared.models import Finding


class BaseScanner(ABC):

    name: str

    @abstractmethod
    def scan(self, repository_path: Path) -> list[Finding]:
        """
        Run the scanner and return normalized findings.
        """
        raise NotImplementedError