import hashlib
import json
from pathlib import Path
from typing import Any

from app.core.config import settings
from app.services.embedding_service import embed_text

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
INDEX_PATH = PROCESSED_DIR / "index.json"
SAMPLE_PATH = Path("data/samples/sample.txt")


def index_text_document(filename: str, content: str) -> dict[str, Any]:
    text = _clean_text(content)
    document_id = _document_id(filename, text)
    chunks = _split_text(text)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / filename).write_text(text, encoding="utf-8")

    index = _load_index()
    index["documents"] = [
        document for document in index["documents"] if document["document_id"] != document_id
    ]
    index["chunks"] = [
        chunk for chunk in index["chunks"] if chunk["document_id"] != document_id
    ]

    index["documents"].append(
        {
            "document_id": document_id,
            "filename": filename,
            "chunk_count": len(chunks),
        }
    )
    for position, chunk_text in enumerate(chunks):
        chunk_id = f"{document_id}-chunk-{position + 1}"
        index["chunks"].append(
            {
                "document_id": document_id,
                "chunk_id": chunk_id,
                "source": filename,
                "position": position,
                "content": chunk_text,
                "embedding": embed_text(chunk_text),
            }
        )

    _save_index(index)
    return {
        "document_id": document_id,
        "filename": filename,
        "chunk_count": len(chunks),
        "status": "indexed",
    }


def ensure_sample_document_indexed() -> None:
    index = _load_index()
    if index["chunks"] or not SAMPLE_PATH.exists():
        return
    index_text_document(SAMPLE_PATH.name, SAMPLE_PATH.read_text(encoding="utf-8"))


def load_chunks() -> list[dict[str, Any]]:
    ensure_sample_document_indexed()
    return _load_index()["chunks"]


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


def _load_index() -> dict[str, list[dict[str, Any]]]:
    if not INDEX_PATH.exists():
        return {"documents": [], "chunks": []}
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def _save_index(index: dict[str, list[dict[str, Any]]]) -> None:
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
