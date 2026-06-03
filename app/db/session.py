from sqlalchemy import create_engine, inspect
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
        existing_tables = set(inspect(engine).get_table_names())
        required_tables = {"documents", "chunks", "qa_logs"}
        if not required_tables.issubset(existing_tables):
            return False
        _tables_initialized = True
        return True
    except SQLAlchemyError:
        return False
