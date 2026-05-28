from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class QALog(Base):
    __tablename__ = "qa_logs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    sources: Mapped[list[dict]] = mapped_column(JSON, default=list, nullable=False)
    top_k: Mapped[int] = mapped_column(Integer, nullable=False)
    llm_provider: Mapped[str | None] = mapped_column(String(100))
    llm_model: Mapped[str | None] = mapped_column(String(255))
    latency_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
