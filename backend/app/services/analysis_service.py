import json
from pathlib import Path
from typing import Any

from app.core.prompts import (
    ANALYSIS_PROMPT,
    COMPARISON_PROMPT,
)

from app.services.ingestion_service import (
    load_all_transcripts,
)

from app.services.rag_service import (
    retrieve_relevant_chunks,
    build_context,
)

from app.services.llm_service import (
    generate_text,
)


# ==========================================
# Paths
# ==========================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

GUIDE_PATH = (
    BASE_DIR
    / "data"
    / "interview_guide.json"
)


# ==========================================
# Load Interview Guide
# ==========================================

def load_interview_guide() -> list[dict[str, Any]]:
    """
    Load the interview guide questions
    from interview_guide.json.
    """

    if not GUIDE_PATH.exists():
        raise FileNotFoundError(
            f"Interview guide not found: "
            f"{GUIDE_PATH}"
        )

    with open(
        GUIDE_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    return data


# ==========================================
# Analyze Interview Question
# ==========================================

def analyze_question(
    question: str,
    market: str | None = None
) -> dict[str, Any]:
    """
    Analyze an interview-guide question
    across the expert transcripts.
    """

    relevant_chunks = (
        retrieve_relevant_chunks(
            question,
            market=market,
            top_k=10,
        )
    )

    if not relevant_chunks:

        return {
            "question": question,
            "answer": (
                "No relevant evidence "
                "was found."
            ),
            "evidence": [],
        }

    context = build_context(
        relevant_chunks
    )

    prompt = ANALYSIS_PROMPT.format(
        question=question,
        context=context,
    )

    answer = generate_text(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "evidence": relevant_chunks,
    }


# ==========================================
# Compare Experts
# ==========================================

def compare_experts() -> dict[str, Any]:
    """
    Compare all three expert interviews
    to identify themes, agreements and
    differences.
    """

    chunks = load_all_transcripts()

    if not chunks:

        return {
            "comparison": (
                "No transcripts available."
            ),
            "experts": [],
        }

    context_parts = []

    for chunk in chunks:

        context_parts.append(
            f"""
EXPERT: {chunk.expert}
ROLE: {chunk.role}
MARKET: {chunk.market}
TIMESTAMP: {chunk.timestamp}
SPEAKER: {chunk.speaker}

EXACT TEXT:
{chunk.text}
"""
        )

    context = "\n\n".join(
        context_parts
    )

    prompt = COMPARISON_PROMPT.format(
        context=context
    )

    comparison = generate_text(
        prompt
    )

    experts = []

    seen_experts = set()

    for chunk in chunks:

        if chunk.expert in seen_experts:
            continue

        seen_experts.add(
            chunk.expert
        )

        experts.append(
            {
                "expert": chunk.expert,
                "market": chunk.market,
                "role": chunk.role,
            }
        )

    return {
        "comparison": comparison,
        "experts": experts,
    }