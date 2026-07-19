from pydantic import BaseModel


class Finding(BaseModel):
    tool: str
    tools: list[str] = []
    severity: str
    title: str
    message: str
    file: str
    line: int | None = None

    owasp: str | None = None
    cwe: str | None = None
    cvss: float | None = None

    recommendation: str | None = None
    references: list[str] = []
