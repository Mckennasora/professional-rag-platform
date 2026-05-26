from app.schemas.chat import ChatRequest, ChatResponse, Source


def answer_question(request: ChatRequest) -> ChatResponse:
    # TODO: Connect document retrieval, rerank, and LLM generation.
    return ChatResponse(
        answer=f"当前收到的问题是：{request.question}",
        sources=[
            Source(
                document_id=None,
                chunk_id=None,
                content="这里后续返回检索到的原文片段。",
            )
        ],
    )
