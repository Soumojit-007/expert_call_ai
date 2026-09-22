import re
from pathlib import Path
from typing import Optional

from app.models.transcript import TranscriptChunk


BASE_DIR = Path(__file__).resolve().parent.parent

TRANSCRIPTS_DIR = BASE_DIR / "data" / "transcripts"


TRANSCRIPT_CONFIG = {
    "france": {
        "file": "france.txt",
        "expert": "Dr. Jean Martin",
        "role": "Head of Urology",
        "market": "France",
    },
    "germany": {
        "file": "germany.txt",
        "expert": "Anna Keller",
        "role": "Former Hospital Procurement Director",
        "market": "Germany",
    },
    "uk": {
        "file": "uk.txt",
        "expert": "Dr. Emily Carter",
        "role": "Consultant Urologist",
        "market": "United Kingdom",
    },
}


TIMESTAMP_PATTERN = re.compile(
    r"^(\d{2}:\d{2})\s*$"
)


def parse_timestamp(timestamp: str) -> int:
    """
    Convert MM:SS timestamp into total seconds.
    """

    minutes, seconds = map(int, timestamp.split(":"))

    return minutes * 60 + seconds


def parse_transcript(
    file_path: Path,
    expert: str,
    role: str,
    market: str,
) -> list[TranscriptChunk]:
    """
    Parse a transcript while preserving:
    - timestamp
    - speaker
    - exact text
    - expert
    - role
    - market
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Transcript file not found: {file_path}"
        )

    lines = file_path.read_text(
        encoding="utf-8"
    ).splitlines()

    chunks = []

    current_timestamp: Optional[str] = None
    current_speaker: Optional[str] = None
    current_text = []

    def save_current_chunk():
        if (
            current_timestamp
            and current_speaker
            and current_text
        ):
            text = " ".join(
                line.strip()
                for line in current_text
                if line.strip()
            ).strip()

            if text:
                chunks.append(
                    TranscriptChunk(
                        expert=expert,
                        role=role,
                        market=market,
                        timestamp=current_timestamp,
                        timestamp_seconds=parse_timestamp(
                            current_timestamp
                        ),
                        speaker=current_speaker,
                        text=text,
                    )
                )

    for line in lines:

        line = line.strip()

        if not line:
            continue

        timestamp_match = TIMESTAMP_PATTERN.match(line)

        if timestamp_match:

            save_current_chunk()

            current_timestamp = timestamp_match.group(1)
            current_speaker = None
            current_text = []

            continue

        if ":" in line and current_speaker is None:

            speaker, text = line.split(":", 1)

            current_speaker = speaker.strip()

            if text.strip():
                current_text.append(text.strip())

        else:

            current_text.append(line)

    save_current_chunk()

    return chunks


def load_transcript(market: str) -> list[TranscriptChunk]:
    """
    Load one transcript using its market name.
    """

    market_key = market.lower().strip()

    config = TRANSCRIPT_CONFIG.get(market_key)

    if not config:
        return []

    file_path = TRANSCRIPTS_DIR / config["file"]

    return parse_transcript(
        file_path=file_path,
        expert=config["expert"],
        role=config["role"],
        market=config["market"],
    )


def load_all_transcripts() -> list[TranscriptChunk]:
    """
    Load all three expert transcripts.
    """

    all_chunks = []

    for market in TRANSCRIPT_CONFIG:
        chunks = load_transcript(market)

        all_chunks.extend(chunks)

    return all_chunks


def get_all_transcripts():
    """
    Return basic transcript information.
    """

    result = []

    for key, config in TRANSCRIPT_CONFIG.items():

        result.append(
            {
                "id": key,
                "expert": config["expert"],
                "role": config["role"],
                "market": config["market"],
            }
        )

    return result


def get_transcript(market: str):
    """
    Return one complete transcript.
    """

    chunks = load_transcript(market)

    if not chunks:
        return None

    return {
        "expert": chunks[0].expert,
        "role": chunks[0].role,
        "market": chunks[0].market,
        "chunks": [
            chunk.model_dump()
            for chunk in chunks
        ],
    }