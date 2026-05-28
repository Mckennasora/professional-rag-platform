from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal, init_db
from app.models.chunk import Chunk
from app.repositories.document_repo import load_index, save_index


def replace_chunks_for_document(document_id: str, chunks: list[dict[str, Any]]) -> None:
    index = load_index()
    index["chunks"] = [
        chunk for chunk in index["chunks"] if chunk["document_id"] != document_id
    ]
    index["chunks"].extend(chunks)
    save_index(index)
    _replace_chunks_db(document_id, chunks)


def list_chunks() -> list[dict[str, Any]]:
    db_chunks = _list_chunks_db()
    if db_chunks:
        return db_chunks

    return load_index()["chunks"]


def _replace_chunks_db(document_id: str, chunks: list[dict[str, Any]]) -> bool:
    if not init_db():
        return False

    try:
        with SessionLocal() as session:
            session.execute(delete(Chunk).where(Chunk.document_id == document_id))
            for chunk in chunks:
                session.add(
                    Chunk(
                        id=chunk["chunk_id"],
                        document_id=chunk["document_id"],
                        source=chunk["source"],
                        page=chunk.get("page"),
                        section=chunk.get("section"),
                        position=chunk["position"],
                        content=chunk["content"],
                        embedding=chunk.get("embedding"),
                        embedding_model=chunk.get("embedding_model"),
                    )
                )
            session.commit()
        return True
    except SQLAlchemyError:
        return False


def _list_chunks_db() -> list[dict[str, Any]] | None:
    if not init_db():
        return None

    try:
        with SessionLocal() as session:
            rows = session.scalars(select(Chunk).order_by(Chunk.created_at, Chunk.position)).all()
            return [
                {
                    "document_id": row.document_id,
                    "chunk_id": row.id,
                    "source": row.source,
                    "page": row.page,
                    "section": row.section,
                    "position": row.position,
                    "content": row.content,
                    "embedding": row.embedding,
                    "embedding_model": row.embedding_model,
                }
                for row in rows
            ]
    except SQLAlchemyError:
        return None
