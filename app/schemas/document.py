from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    status: str
    source_path: str | None = None
    processed_path: str | None = None
