from abc import ABC, abstractmethod
from pathlib import Path

from app.shared.models import Finding


class BaseScanner(ABC):

    name = ""

    category = ""

    supported_languages = set()

    supported_package_managers = set()

    requires_container = False

    @abstractmethod
    def scan(
        self,
        repository_path: Path
    ) -> list[Finding]:
        pass