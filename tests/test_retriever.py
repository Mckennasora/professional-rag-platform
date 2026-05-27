from app.services.document_service import index_text_document
from app.services.retriever_service import retrieve


def test_retrieve_returns_top_k_chunks() -> None:
    index_text_document(
        "retriever-demo.txt",
        "专业文档 RAG 系统包含文档切分、向量检索、引用溯源和自动评估。",
    )

    results = retrieve("什么是向量检索？", top_k=1)

    assert len(results) == 1
    assert results[0]["chunk_id"]
    assert results[0]["content"]
    assert "score" in results[0]
