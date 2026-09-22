from pydantic import BaseModel, Field
from typing import List, Optional


# =========================
# Interview Guide / Analysis
# =========================

class AnalysisRequest(BaseModel):
    market:str | None = None


    question: str = Field(
        ...,
        min_length=5,
        description="Interview guide question to analyze"
    )


class Evidence(BaseModel):
    expert: str
    role: str
    market: str
    timestamp: str
    speaker: str
    quote: str


class AnalysisResponse(BaseModel):
    question: str
    answer: str
    evidence: List[Evidence]


# =========================
# Chat
# =========================

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        description="Question to ask across all expert transcripts"
    )


class ChatResponse(BaseModel):
    answer: str
    evidence: List[Evidence]


# =========================
# Transcript
# =========================

class TranscriptResponse(BaseModel):
    expert: str
    role: str
    market: str
    chunks: list


# =========================
# Comparison
# =========================

class ComparisonResponse(BaseModel):
    comparison: str
    experts: List[dict]