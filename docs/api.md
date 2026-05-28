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

上传 UTF-8 编码的 TXT 文档，完成原文保存、清洗、切分、轻量 embedding 和本地文件索引。

当前阶段处理流程：

```text
UploadFile
  -> 校验 .txt 后缀
  -> UTF-8 解码
  -> 保存原文到 data/raw/
  -> 清洗文本并保存到 data/processed/{document_id}.txt
  -> 按 CHUNK_SIZE / CHUNK_OVERLAP 切分
  -> 生成轻量 mock embedding
  -> 写入 data/processed/index.json
```

Response:

```json
{
  "document_id": "string",
  "filename": "sample.txt",
  "chunk_count": 1,
  "status": "indexed",
  "source_path": "data/raw/sample.txt",
  "processed_path": "data/processed/{document_id}.txt"
}
```

TODO: 后续接入 PostgreSQL + pgvector 后，将 `documents`、`chunks` 和 `qa_logs` 写入数据库。

## GET /api/eval/status

TODO: 后续实现评估任务状态和指标查询。
