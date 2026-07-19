from app.modules.scanner.orchestrator import ScanOrchestrator


class ScanManager:

    def run(self, path):
        return ScanOrchestrator().run(path)
    
    # def __init__(self):
    #     self.orchestrator = ScanOrchestrator()

    # def run(self, repository_path):
    #     return self.orchestrator.run(repository_path)