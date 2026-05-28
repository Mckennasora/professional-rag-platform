import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.repositories.document_repo import INDEX_PATH, save_index


def main() -> None:
    # TODO: Replace this local reset with PostgreSQL table truncation after DB setup.
    save_index({"documents": [], "chunks": [], "qa_logs": []})
    print(f"local index reset: {INDEX_PATH}")


if __name__ == "__main__":
    main()
