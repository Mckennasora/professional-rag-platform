from fastapi.testclient import TestClient

from app.main import app
from app.repositories.document_repo import load_index

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_mock_answer_and_sources() -> None:
    response = client.post("/api/chat", json={"question": "什么是 RAG？", "top_k": 5})

    assert response.status_code == 200
    body = response.json()
    assert "当前收到的问题是：什么是 RAG？" in body["answer"]
    assert isinstance(body["sources"], list)
    assert len(body["sources"]) >= 1
    assert body["sources"][0]["document_id"]
    assert body["sources"][0]["chunk_id"]
    assert body["sources"][0]["content"]


def test_chat_records_qa_log() -> None:
    response = client.post("/api/chat", json={"question": "什么是 pipeline？", "top_k": 2})

    assert response.status_code == 200
    qa_logs = load_index()["qa_logs"]
    assert qa_logs[-1]["question"] == "什么是 pipeline？"
    assert qa_logs[-1]["top_k"] == 2
    assert "answer" in qa_logs[-1]
