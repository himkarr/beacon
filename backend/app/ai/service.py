import json
import logging

import httpx
from pydantic import ValidationError

from app.core.config import settings
from app.ai.prompts import SYSTEM_INSTRUCTION, build_prompt
from app.ai.schemas import AIAnalysis

logger = logging.getLogger(__name__)

GROQ_API_BASE = "https://api.groq.com/openai/v1"


class AIAnalysisError(Exception):
    """Raised when the AI provider fails or returns something we can't parse.

    Callers should catch this and degrade gracefully — a scan with working
    findings but a broken AI summary should still return successfully.
    """


# ---------------------------------------------------------------------------
# Gemini  —  commented out in favour of xAI (Grok)
# ---------------------------------------------------------------------------
# from google import genai
# from google.genai import types
# from google.genai.errors import APIError
#
# _client = genai.Client(api_key=settings.gemini_api_key)
#
# def analyze_findings(findings: list[dict], summary: dict) -> AIAnalysis:
#     if not findings:
#         return AIAnalysis(
#             executive_summary="No issues were found by the scanners.",
#             security_score=100,
#             risk_level="LOW",
#             top_recommendations=[],
#             findings=[],
#         )
#     try:
#         response = _client.models.generate_content(
#             model=settings.gemini_model,
#             contents=build_prompt(findings, summary),
#             config=types.GenerateContentConfig(
#                 system_instruction=SYSTEM_INSTRUCTION,
#                 response_mime_type="application/json",
#             ),
#         )
#     except APIError as exc:
#         logger.exception("Gemini API call failed")
#         raise AIAnalysisError(f"Gemini API error ({exc.code}): {exc.message}") from exc
#     if not response.text:
#         raise AIAnalysisError("Gemini returned an empty response.")
#     try:
#         data = json.loads(response.text)
#     except json.JSONDecodeError as exc:
#         logger.exception("Gemini returned non-JSON output: %s", response.text[:500])
#         raise AIAnalysisError("Gemini returned output that wasn't valid JSON.") from exc
#     try:
#         return AIAnalysis(**data)
#     except ValidationError as exc:
#         logger.exception("Gemini JSON didn't match expected schema")
#         raise AIAnalysisError("Gemini's response didn't match the expected schema.") from exc


# ---------------------------------------------------------------------------
# Groq (free tier — Llama 3, Mixtral, DeepSeek, etc.)
# ---------------------------------------------------------------------------

def analyze_findings(findings: list[dict], summary: dict) -> AIAnalysis:
    if not findings:
        return AIAnalysis(
            executive_summary="No issues were found by the scanners.",
            security_score=100,
            risk_level="LOW",
            top_recommendations=[],
            findings=[],
        )

    if not settings.groq_api_key:
        raise AIAnalysisError("GROQ_API_KEY is not configured. Set it in .env")

    try:
        with httpx.Client(timeout=120) as client:
            response = client.post(
                f"{GROQ_API_BASE}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.groq_model,
                    "messages": [
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": build_prompt(findings, summary)},
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": settings.groq_max_tokens,
                },
            )
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        body = exc.response.text[:500]
        logger.exception("Groq API call failed (HTTP %s)", status)
        raise AIAnalysisError(f"Groq API error ({status}): {body}") from exc
    except httpx.RequestError as exc:
        logger.exception("Groq API request failed")
        raise AIAnalysisError(f"Groq API request failed: {exc}") from exc

    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    if not text:
        raise AIAnalysisError("Groq returned an empty response.")

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        logger.exception("Groq returned non-JSON output: %s", text[:500])
        raise AIAnalysisError("Groq returned output that wasn't valid JSON.") from exc

    try:
        return AIAnalysis(**parsed)
    except ValidationError as exc:
        logger.exception("Groq JSON didn't match expected schema")
        raise AIAnalysisError("Groq's response didn't match the expected schema.") from exc
