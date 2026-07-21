import json

from google import genai
from google.genai import types

from app.core.config import settings
from app.ai.prompts import SYSTEM_INSTRUCTION, build_prompt
from app.ai.schemas import AIAnalysis

_client = genai.Client(api_key=settings.gemini_api_key)


def analyze_findings(findings: list[dict], summary: dict) -> AIAnalysis:
    if not findings:
        return AIAnalysis(
            executive_summary="No issues were found by the scanners.",
            security_score=100,
            risk_level="LOW",
            top_recommendations=[],
            findings=[],
        )

    response = _client.models.generate_content(
        model=settings.gemini_model,
        contents=build_prompt(findings, summary),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
        ),
    )

    data = json.loads(response.text)
    return AIAnalysis(**data)