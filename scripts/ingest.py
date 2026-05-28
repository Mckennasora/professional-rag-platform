import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.services.document_service import index_text_document


def main() -> None:
    parser = argparse.ArgumentParser(description="Index a UTF-8 TXT document.")
    parser.add_argument(
        "path",
        nargs="?",
        default="data/samples/sample.txt",
        help="Path to a UTF-8 TXT document. Defaults to data/samples/sample.txt.",
    )
    args = parser.parse_args()

    document_path = Path(args.path)
    result = index_text_document(
        document_path.name,
        document_path.read_text(encoding="utf-8"),
    )
    print(result)


if __name__ == "__main__":
    main()
