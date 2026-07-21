from pydantic import BaseModel


class AIFindingExplanation(BaseModel):
    finding_index: int          # position in the findings list you sent
    explanation: str            # plain-English "what this means"
    remediation: str            # how to fix it
    priority: int                # 1 = fix first


class AIAnalysis(BaseModel):
    executive_summary: str
    security_score: int          # 0-100
    risk_level: str               # LOW / MEDIUM / HIGH / CRITICAL
    top_recommendations: list[str]
    findings: list[AIFindingExplanation]