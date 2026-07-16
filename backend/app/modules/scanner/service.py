from .manager import ScanManager


class ScannerService:

    def scan(self, repository_path):

        manager = ScanManager()

        return manager.run(repository_path)