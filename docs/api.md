# API

## GET /health

健康检查。

Response:

```json
{
  "status": "ok"
}
```

## POST /api/chat

最小 mock 问答接口。当前不接入真实 LLM、Embedding 或向量库。

Request:

```json
{
  "question": "什么是 RAG？",
  "top_k": 5
}
```

Response:

```json
{
  "answer": "当前收到的问题是：什么是 RAG？",
  "sources": [
    {
      "document_id": null,
      "chunk_id": null,
      "content": "这里后续返回检索到的原文片段。"
    }
  ]
}
```

## POST /api/documents/upload

TODO: 后续实现文档上传、解析、切分、Embedding 和入库。

## GET /api/eval/status

TODO: 后续实现评估任务状态和指标查询。
