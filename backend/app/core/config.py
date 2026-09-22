from pathlib import Path

from dotenv import load_dotenv
import os


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Load .env from backend/
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured. "
        "Please add it to backend/.env"
    )


# Gemini models
GEMINI_MODEL = "gemini-3.5-flash-lite"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"


# Vector database
VECTORSTORE_DIR = BASE_DIR / "vectorstore"


# Application
APP_NAME = "Expert Call AI"
APP_VERSION = "1.0.0"