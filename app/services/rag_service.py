from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services.retriever_service import retrieve


def answer_question(request: ChatRequest) -> ChatResponse:
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
        return ChatResponse(answer="当前知识库中还没有可检索的文档。", sources=[])

    # TODO: Replace this mock answer with LLM generation grounded in retrieved sources.
    return ChatResponse(
        answer=(
            f"当前收到的问题是：{request.question}\n"
            f"已从知识库检索到 {len(sources)} 个相关片段。"
            "第一版暂不接入真实 LLM，后续会基于 sources 生成可溯源回答。"
        ),
        sources=sources,
    )
