import json
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal, init_db
from app.models.document import Document

PROCESSED_DIR = Path("data/processed")
INDEX_PATH = PROCESSED_DIR / "index.json"


def load_index() -> dict[str, list[dict[str, Any]]]:
    if not INDEX_PATH.exists():
        return _empty_index()

    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    for key, value in _empty_index().items():
        index.setdefault(key, value)
    return index


def save_index(index: dict[str, list[dict[str, Any]]]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    saveable_index = _empty_index()
    saveable_index.update(index)
    INDEX_PATH.write_text(
        json.dumps(saveable_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def upsert_document(document: dict[str, Any]) -> None:
    index = load_index()
    document_id = document["document_id"]
    index["documents"] = [
        item for item in index["documents"] if item["document_id"] != document_id
    ]
    index["documents"].append(document)
    save_index(index)
    _upsert_document_db(document)


def _upsert_document_db(document: dict[str, Any]) -> bool:
    if not init_db():
        return False

    try:
        with SessionLocal() as session:
            existing = session.get(Document, document["document_id"])
            if existing is None:
                existing = Document(id=document["document_id"])
                session.add(existing)

            existing.filename = document["filename"]
            existing.source_path = document.get("source_path")
            existing.processed_path = document.get("processed_path")
            existing.content_type = document.get("content_type")
            existing.status = document.get("status", "indexed")
            existing.chunk_count = document.get("chunk_count", 0)
            existing.error_message = document.get("error_message")
            existing.updated_at = datetime.utcnow()
            session.commit()
        return True
    except SQLAlchemyError:
        return False


def _empty_index() -> dict[str, list[dict[str, Any]]]:
    return {"documents": [], "chunks": [], "qa_logs": []}
