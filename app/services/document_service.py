import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.repositories.chunk_repo import list_chunks, replace_chunks_for_document
from app.repositories.document_repo import load_index, upsert_document
from app.services.embedding_service import embed_text

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
SAMPLE_PATH = Path("data/samples/sample.txt")


def index_text_document(filename: str, content: str) -> dict[str, Any]:
    safe_filename = Path(filename).name
    text = _clean_text(content)
    document_id = _document_id(safe_filename, text)
    chunks = _split_text(text)
    now = datetime.utcnow().isoformat(timespec="seconds")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    raw_path = RAW_DIR / safe_filename
    processed_path = PROCESSED_DIR / f"{document_id}.txt"
    raw_path.write_text(content, encoding="utf-8")
    processed_path.write_text(text, encoding="utf-8")

    upsert_document(
        {
            "document_id": document_id,
            "filename": safe_filename,
            "source_path": str(raw_path),
            "processed_path": str(processed_path),
            "content_type": "text/plain",
            "status": "indexed",
            "chunk_count": len(chunks),
            "created_at": now,
            "updated_at": now,
        }
    )

    chunk_records: list[dict[str, Any]] = []
    for position, chunk_text in enumerate(chunks):
        chunk_id = f"{document_id}-chunk-{position + 1}"
        chunk_records.append(
            {
                "document_id": document_id,
                "chunk_id": chunk_id,
                "source": safe_filename,
                "page": None,
                "section": None,
                "position": position,
                "content": chunk_text,
                "embedding": embed_text(chunk_text),
                "embedding_model": settings.embedding_model,
                "created_at": now,
            }
        )
    replace_chunks_for_document(document_id, chunk_records)

    return {
        "document_id": document_id,
        "filename": safe_filename,
        "chunk_count": len(chunks),
        "status": "indexed",
        "source_path": str(raw_path),
        "processed_path": str(processed_path),
    }


def ensure_sample_document_indexed() -> None:
    index = load_index()
    if index["chunks"] or not SAMPLE_PATH.exists():
        return
    index_text_document(SAMPLE_PATH.name, SAMPLE_PATH.read_text(encoding="utf-8"))


def load_chunks() -> list[dict[str, Any]]:
    ensure_sample_document_indexed()
    return list_chunks()


def _clean_text(content: str) -> str:
    lines = [line.strip() for line in content.splitlines()]
    return "\n".join(line for line in lines if line)


def _split_text(text: str) -> list[str]:
    chunk_size = settings.chunk_size
    overlap = min(settings.chunk_overlap, max(chunk_size - 1, 0))
    if len(text) <= chunk_size:
        return [text]

    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks


def _document_id(filename: str, text: str) -> str:
    digest = hashlib.sha1(f"{filename}:{text}".encode("utf-8")).hexdigest()
    return digest[:16]
