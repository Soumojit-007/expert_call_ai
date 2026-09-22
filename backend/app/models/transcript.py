from pydantic import BaseModel


class TranscriptChunk(BaseModel):

    expert: str

    role: str

    market: str

    timestamp: str

    timestamp_seconds: int

    speaker: str

    text: str