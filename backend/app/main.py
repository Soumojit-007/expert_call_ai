from fastapi import FastAPI

from app.api.routes import analysis
from app.api.routes import chat
from app.api.routes import transcripts


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Expert Call AI",
    description=(
        "AI-powered expert interview analysis "
        "for the European Robotic Surgery Market."
    ),
    version="1.0.0",
)


# ==========================================
# Register API Routes
# ==========================================

app.include_router(
    transcripts.router
)

app.include_router(
    analysis.router
)

app.include_router(
    chat.router
)


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/")
def root():
    return {
        "message": "Expert Call AI API is running",
        "version": "1.0.0",
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }