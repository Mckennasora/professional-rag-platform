from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    # TODO: Add document_id, filename, status, and metadata after upload is implemented.
    message: str
