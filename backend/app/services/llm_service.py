import json
from typing import Any

from google import genai

from app.core.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

from app.core.prompts import SYSTEM_INSTRUCTION


# ==========================================
# Gemini Client
# ==========================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)

MODEL_NAME = GEMINI_MODEL


# ==========================================
# Generate Text
# ==========================================

def generate_text(
    prompt: str,
    temperature: float = 0.2,
) -> str:
    """
    Send a prompt to Gemini and return
    the generated text.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature,
            "system_instruction": SYSTEM_INSTRUCTION,
        },
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# ==========================================
# Generate JSON
# ==========================================

def generate_json(
    prompt: str,
    temperature: float = 0.1,
) -> dict[str, Any]:
    """
    Send a prompt to Gemini and parse the
    response as JSON.

    This can be used later when we want
    structured AI responses.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "temperature": temperature,
            "response_mime_type": "application/json",
            "system_instruction": SYSTEM_INSTRUCTION,
        },
    )

    if not response.text:
        raise ValueError(
            "Gemini returned an empty response."
        )

    try:
        return json.loads(response.text)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Gemini returned invalid JSON."
        ) from exc