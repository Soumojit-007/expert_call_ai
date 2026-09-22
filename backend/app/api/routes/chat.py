from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest
from app.services.rag_service import answer_question


router = APIRouter(
    prefix="/api/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(request: ChatRequest):

    try:
        result = answer_question(
            request.question
        )

        return {
            "success": True,
            "answer": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )