from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_txt_document_indexes_chunks() -> None:
    response = client.post(
        "/api/documents/upload",
        files={
            "file": (
                "demo.txt",
                "RAG 系统需要先检索专业文档，再基于证据片段生成答案。",
                "text/plain",
            )
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["filename"] == "demo.txt"
    assert body["chunk_count"] >= 1
    assert body["status"] == "indexed"


def test_upload_rejects_non_txt_file() -> None:
    response = client.post(
        "/api/documents/upload",
        files={"file": ("demo.pdf", b"%PDF", "application/pdf")},
    )

    assert response.status_code == 400
