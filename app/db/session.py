from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

_tables_initialized = False


def init_db() -> bool:
    global _tables_initialized
    if _tables_initialized:
        return True

    try:
        # Import models here so their metadata is registered before create_all.
        from app.models import chunk, document, qa_log  # noqa: F401

        Base.metadata.create_all(bind=engine)
        _tables_initialized = True
        return True
    except SQLAlchemyError:
        return False
