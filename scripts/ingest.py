from pathlib import Path

from app.services.document_service import index_text_document


def main() -> None:
    sample_path = Path("data/samples/sample.txt")
    result = index_text_document(sample_path.name, sample_path.read_text(encoding="utf-8"))
    print(result)


if __name__ == "__main__":
    main()
