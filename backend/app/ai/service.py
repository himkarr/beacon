import json
import logging

from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import ValidationError

from app.core.config import settings
from app.ai.prompts import SYSTEM_INSTRUCTION, build_prompt
from app.ai.schemas import AIAnalysis

logger = logging.getLogger(__name__)

_client = genai.Client(api_key=settings.gemini_api_key)


class AIAnalysisError(Exception):
    """Raised when Gemini fails or returns something we can't parse.

    Callers should catch this and degrade gracefully — a scan with working
    findings but a broken AI summary should still return successfully.
    """


def analyze_findings(findings: list[dict], summary: dict) -> AIAnalysis:
    if not findings:
        return AIAnalysis(
            executive_summary="No issues were found by the scanners.",
            security_score=100,
            risk_level="LOW",
            top_recommendations=[],
            findings=[],
        )

    try:
        response = _client.models.generate_content(
            model=settings.gemini_model,
            contents=build_prompt(findings, summary),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                response_mime_type="application/json",
            ),
        )
    except APIError as exc:
        logger.exception("Gemini API call failed")
        raise AIAnalysisError(f"Gemini API error ({exc.code}): {exc.message}") from exc

    if not response.text:
        raise AIAnalysisError("Gemini returned an empty response.")

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError as exc:
        logger.exception("Gemini returned non-JSON output: %s", response.text[:500])
        raise AIAnalysisError("Gemini returned output that wasn't valid JSON.") from exc

    try:
        return AIAnalysis(**data)
    except ValidationError as exc:
        logger.exception("Gemini JSON didn't match expected schema")
        raise AIAnalysisError("Gemini's response didn't match the expected schema.") from exc