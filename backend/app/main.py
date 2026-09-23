from fastapi import FastAPI

from app.api.routes import analysis
from app.api.routes import chat
from app.api.routes import transcripts

from fastapi.middleware.cors import CORSMiddleware
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


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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