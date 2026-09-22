from fastapi import APIRouter , HTTPException


from app.services.ingestion_service import get_all_transcripts , get_transcript


router = APIRouter(
    prefix="/api/transcripts",
    tags=["Transcripts"]
)


@router.get("/")
def list_transcripts():
    """
    Return all available expert transcripts.
    """
    return {
        "transcripts": get_all_transcripts()
    }


@router.get("/{market}")
def get_transcript_by_market(market: str):
    """
    Return a transcript for a specific market.
    
    Example:
    /api/transcripts/france
    """
    transcript = get_transcript(market)

    if transcript is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transcript not found for market: {market}"
        )

    return transcript