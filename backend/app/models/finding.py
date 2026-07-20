from pydantic import BaseModel


class Finding(BaseModel):
    tool: str
    severity: str
    title: str
    message: str
    file: str
    line: int | None = None
    category: str | None = None
    recommendation: str | None = None
    package: str | None = None