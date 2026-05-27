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

最小 RAG 问答接口。当前使用轻量本地 embedding 和文件索引完成检索，不接入真实 LLM 或数据库。

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
  "answer": "当前收到的问题是：什么是 RAG？\n已从知识库检索到 1 个相关片段。第一版暂不接入真实 LLM，后续会基于 sources 生成可溯源回答。",
  "sources": [
    {
      "document_id": "string",
      "chunk_id": "string",
      "source": "sample.txt",
      "score": 0.42,
      "content": "检索到的原文片段"
    }
  ]
}
```

## POST /api/documents/upload

上传 UTF-8 编码的 TXT 文档，完成保存、切分、轻量 embedding 和本地文件索引。

Response:

```json
{
  "document_id": "string",
  "filename": "sample.txt",
  "chunk_count": 1,
  "status": "indexed"
}
```

## GET /api/eval/status

TODO: 后续实现评估任务状态和指标查询。
