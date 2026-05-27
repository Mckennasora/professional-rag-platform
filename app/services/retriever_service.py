from typing import Any

from app.services.document_service import load_chunks
from app.services.embedding_service import embed_text


def retrieve(query: str, top_k: int) -> list[dict[str, Any]]:
    """Retrieve top-k chunks with a lightweight vector similarity demo."""
    query_embedding = embed_text(query)
    scored_chunks = []

    for chunk in load_chunks():
        score = _cosine_similarity(query_embedding, chunk["embedding"])
        scored_chunks.append({**chunk, "score": score})

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)
    return scored_chunks[:top_k]


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(left_value * right_value for left_value, right_value in zip(left, right))
