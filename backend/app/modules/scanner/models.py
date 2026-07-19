from pydantic import BaseModel

class ScannerResult(BaseModel):
    name: str
    status: str
    findings: int
    duration: float
    error: str | None = None