from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_mock_answer_and_sources() -> None:
    response = client.post("/api/chat", json={"question": "什么是 RAG？", "top_k": 5})

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "当前收到的问题是：什么是 RAG？"
    assert isinstance(body["sources"], list)
    assert body["sources"][0]["content"] == "这里后续返回检索到的原文片段。"
