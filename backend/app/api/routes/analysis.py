from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisRequest
from app.services.analysis_service import (
    analyze_question,
    compare_experts
)


router = APIRouter(
    prefix="/api/analysis",
    tags=["Analysis"]
)


@router.post("/question")
def analyze_interview_question(request: AnalysisRequest):
    """
    Analyze one interview-guide question across
    all available expert transcripts.
    """

    try:
        result = analyze_question(request.question)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/compare")
def compare_all_experts():
    """
    Identify common themes, agreements and
    differences across the three expert calls.
    """

    try:
        result = compare_experts()

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )