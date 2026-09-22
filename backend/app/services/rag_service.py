from typing import Any

import chromadb

from app.core.config import (
    GEMINI_EMBEDDING_MODEL,
    VECTORSTORE_DIR,
)

from app.core.prompts import CHAT_PROMPT

from app.services.ingestion_service import (
    load_all_transcripts,
)

from app.services.llm_service import (
    client,
    generate_text,
)


# ==========================================
# ChromaDB
# ==========================================

chroma_client = chromadb.PersistentClient(
    path=str(VECTORSTORE_DIR)
)


collection = chroma_client.get_or_create_collection(
    name="expert_transcripts"
)


# ==========================================
# Create Embedding
# ==========================================

def create_embedding(
    text: str,
) -> list[float]:
    """
    Generate a Gemini embedding for text.
    """

    response = client.models.embed_content(
        model=GEMINI_EMBEDDING_MODEL,
        contents=text,
    )

    if not response.embeddings:
        raise ValueError(
            "Gemini returned no embedding."
        )

    return response.embeddings[0].values


# ==========================================
# Build Search Text
# ==========================================

def build_search_text(chunk) -> str:
    """
    Create searchable text while preserving
    important transcript metadata.
    """

    return (
        f"Expert: {chunk.expert}\n"
        f"Role: {chunk.role}\n"
        f"Market: {chunk.market}\n"
        f"Timestamp: {chunk.timestamp}\n"
        f"Speaker: {chunk.speaker}\n"
        f"Transcript: {chunk.text}"
    )


# ==========================================
# Initialize Vector Store
# ==========================================

def initialize_vectorstore() -> dict[str, Any]:
    """
    Load all transcripts, create embeddings,
    and store them in ChromaDB.
    """

    chunks = load_all_transcripts()

    if not chunks:
        raise RuntimeError(
            "No transcript chunks were found."
        )

    existing_count = collection.count()

    if existing_count > 0:
        return {
            "status": "already_initialized",
            "chunks": existing_count,
        }

    documents = []
    embeddings = []
    metadatas = []
    ids = []

    for index, chunk in enumerate(chunks):

        search_text = build_search_text(
            chunk
        )

        embedding = create_embedding(
            search_text
        )

        documents.append(
            search_text
        )

        embeddings.append(
            embedding
        )

        metadatas.append(
            {
                "expert": chunk.expert,
                "role": chunk.role,
                "market": chunk.market,
                "timestamp": chunk.timestamp,
                "timestamp_seconds": (
                    chunk.timestamp_seconds
                ),
                "speaker": chunk.speaker,
                "text": chunk.text,
            }
        )

        ids.append(
            f"{chunk.market.lower()}-{index}"
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return {
        "status": "initialized",
        "chunks": len(chunks),
    }


# ==========================================
# Retrieve Relevant Chunks
# ==========================================

def retrieve_relevant_chunks(
    question: str,
    market:str | None=None,
    top_k: int = 8,
) -> list[dict[str, Any]]:
    """
    Retrieve transcript chunks that are
    semantically relevant to the question.
    """

    if collection.count() == 0:
        initialize_vectorstore()

    question_embedding = create_embedding(
        question
    )

    # results = collection.query(
    #     query_embeddings=[
    #         question_embedding
    #     ],
    #     n_results=top_k,
    # )

    query_kwargs= {
        "query_embeddings":[question_embedding],
        "n_results":top_k
    }

    if market:
        query_kwargs["where"]= {"market" : market}

    results = collection.query(**query_kwargs)
    retrieved = []

    metadatas = results.get(
        "metadatas",
        [[]],
    )[0]

    distances = results.get(
        "distances",
        [[]],
    )[0]

    for metadata, distance in zip(
        metadatas,
        distances,
    ):

        retrieved.append(
            {
                "expert": metadata["expert"],
                "role": metadata["role"],
                "market": metadata["market"],
                "timestamp": metadata["timestamp"],
                "timestamp_seconds": (
                    metadata[
                        "timestamp_seconds"
                    ]
                ),
                "speaker": metadata["speaker"],
                "quote": metadata["text"],
                "distance": distance,
            }
        )

    return retrieved


# ==========================================
# Build LLM Context
# ==========================================

def build_context(
    chunks: list[dict[str, Any]],
) -> str:
    """
    Convert retrieved chunks into a structured
    context for Gemini.
    """

    context_parts = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        context_parts.append(
            f"""
EVIDENCE {index}

Expert: {chunk['expert']}
Role: {chunk['role']}
Market: {chunk['market']}
Timestamp: {chunk['timestamp']}
Speaker: {chunk['speaker']}

EXACT TRANSCRIPT:
{chunk['quote']}
"""
        )

    return "\n".join(
        context_parts
    )


# ==========================================
# Answer User Question
# ==========================================

def answer_question(
    question: str,
) -> dict[str, Any]:
    """
    Answer a user question using only
    retrieved transcript evidence.
    """

    chunks = retrieve_relevant_chunks(
        question,
        top_k=8,
    )

    if not chunks:
        return {
            "answer": (
                "No relevant evidence "
                "was found."
            ),
            "evidence": [],
        }

    context = build_context(
        chunks
    )

    prompt = CHAT_PROMPT.format(
        question=question,
        context=context,
    )

    answer = generate_text(
        prompt
    )

    return {
        "answer": answer,
        "evidence": chunks,
    }