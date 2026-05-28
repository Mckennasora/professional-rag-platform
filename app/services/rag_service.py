from time import perf_counter

from app.core.config import settings
from app.repositories.qa_log_repo import save_qa_log
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services.retriever_service import retrieve


def answer_question(request: ChatRequest) -> ChatResponse:
    started_at = perf_counter()
    chunks = retrieve(request.question, request.top_k)
    sources = [
        Source(
            document_id=chunk["document_id"],
            chunk_id=chunk["chunk_id"],
            source=chunk["source"],
            score=round(chunk["score"], 4),
            content=chunk["content"],
        )
        for chunk in chunks
    ]

    if not sources:
        response = ChatResponse(answer="当前知识库中还没有可检索的文档。", sources=[])
        _save_log(request, response, started_at)
        return response

    # TODO: Replace this mock answer with LLM generation grounded in retrieved sources.
    response = ChatResponse(
        answer=(
            f"当前收到的问题是：{request.question}\n"
            f"已从知识库检索到 {len(sources)} 个相关片段。"
            "第一版暂不接入真实 LLM，后续会基于 sources 生成可溯源回答。"
        ),
        sources=sources,
    )
    _save_log(request, response, started_at)
    return response


def _save_log(request: ChatRequest, response: ChatResponse, started_at: float) -> None:
    latency_ms = int((perf_counter() - started_at) * 1000)
    save_qa_log(
        question=request.question,
        answer=response.answer,
        sources=[source.model_dump() for source in response.sources],
        top_k=request.top_k,
        latency_ms=latency_ms,
        llm_provider=settings.llm_provider or None,
        llm_model=settings.llm_model or None,
    )
