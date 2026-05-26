from fastapi import APIRouter

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload")
def upload_document() -> dict[str, str]:
    # TODO: Implement document upload, parsing, chunking, embedding, and indexing.
    return {"message": "document upload is not implemented yet"}
