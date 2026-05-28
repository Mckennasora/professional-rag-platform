from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal, init_db
from app.models.qa_log import QALog
from app.repositories.document_repo import load_index, save_index


def save_qa_log(
    *,
    question: str,
    answer: str,
    sources: list[dict[str, Any]],
    top_k: int,
    latency_ms: int | None = None,
    llm_provider: str | None = None,
    llm_model: str | None = None,
) -> dict[str, Any]:
    log = {
        "qa_log_id": uuid4().hex,
        "question": question,
        "answer": answer,
        "sources": sources,
        "top_k": top_k,
        "latency_ms": latency_ms,
        "llm_provider": llm_provider,
        "llm_model": llm_model,
        "created_at": datetime.utcnow().isoformat(timespec="seconds"),
    }

    index = load_index()
    index["qa_logs"].append(log)
    save_index(index)
    _save_qa_log_db(log)
    return log


def _save_qa_log_db(log: dict[str, Any]) -> bool:
    if not init_db():
        return False

    try:
        with SessionLocal() as session:
            session.add(
                QALog(
                    id=log["qa_log_id"],
                    question=log["question"],
                    answer=log["answer"],
                    sources=log["sources"],
                    top_k=log["top_k"],
                    llm_provider=log["llm_provider"],
                    llm_model=log["llm_model"],
                    latency_ms=log["latency_ms"],
                )
            )
            session.commit()
        return True
    except SQLAlchemyError:
        return False
