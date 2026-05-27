from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    document_id: str | None = None
    chunk_id: str | None = None
    source: str | None = None
    score: float | None = None
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
