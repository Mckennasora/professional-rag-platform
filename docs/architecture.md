# Architecture

本项目采用接近 Java / Spring Boot 后端项目的分层结构，便于后续把 RAG 能力逐步工程化。

## 分层说明

`app/api/`

- 类似 Spring Boot 的 Controller 层。
- 负责 HTTP 接口定义。
- 不写复杂业务逻辑。

`app/schemas/`

- 类似 DTO / VO。
- 使用 Pydantic 定义请求和响应结构。

`app/services/`

- 类似 Service 层。
- 放 RAG 核心逻辑、文档处理、Embedding、检索、Rerank、评估。

`app/repositories/`

- 类似 Repository / Mapper 层。
- 负责数据库访问。
- 初期可以用内存或文件模拟，后期接 PostgreSQL。

`app/models/`

- 类似 Entity。
- 后期定义 SQLAlchemy ORM 模型。

`app/core/`

- 配置、日志、环境变量管理。

`scripts/`

- 离线任务。
- 包括文档入库、评估、重置数据库等。

`data/`

- `raw`：原始文档。
- `processed`：处理后的中间文件。
- `samples`：演示文档。
- `eval`：评测集和标准答案。

`experiments/`

- 保存实验脚本、实验结果和对比表。

`docs/`

- 保存路线图、架构说明、API 说明、实验计划、论文笔记。

## 当前调用链

```text
POST /api/chat
  -> app/api/routes_chat.py
  -> app/services/rag_service.py
  -> app/services/retriever_service.py
  -> app/repositories/chunk_repo.py
  -> app/repositories/qa_log_repo.py
  -> ChatResponse(answer, sources)
```

```text
POST /api/documents/upload
  -> app/api/routes_document.py
  -> app/services/document_service.py
  -> app/services/embedding_service.py
  -> app/repositories/document_repo.py
  -> app/repositories/chunk_repo.py
  -> DocumentUploadResponse(document_id, filename, chunk_count, status)
```

后续会扩展为：

```text
question
  -> query rewrite，可选
  -> BM25 / vector / hybrid retriever
  -> rerank
  -> LLM generation
  -> answer + sources
  -> qa log + evaluation data
```

## 阶段 2：文档入库 pipeline

当前阶段先使用本地文件模拟数据库，核心数据统一落到 `data/processed/index.json`：

- `documents`：保存文档 ID、文件名、原文路径、清洗后路径、状态、chunk 数量。
- `chunks`：保存 chunk ID、document ID、source、page、section、position、content、embedding、embedding model。
- `qa_logs`：保存 question、answer、sources、top_k、latency、model 配置。

后续接入 PostgreSQL + pgvector 时，Repository 层会从本地 JSON 切换到数据库，API 和 Service 层尽量保持不变。

## 数据库表设计草案

`documents`

- `id`：文档主键。
- `filename`：原始文件名。
- `source_path`：原始文件保存路径。
- `processed_path`：清洗后文本路径。
- `content_type`：文件类型。
- `status`：`uploaded` / `parsed` / `indexed` / `failed`。
- `chunk_count`：切分后的 chunk 数。
- `error_message`：失败原因。
- `created_at` / `updated_at`：创建与更新时间。

`chunks`

- `id`：chunk 主键。
- `document_id`：关联文档 ID。
- `source`：来源文件。
- `page`：页码，TXT 暂为空。
- `section`：章节，当前暂为空。
- `position`：chunk 在文档中的顺序。
- `content`：chunk 原文。
- `embedding_model`：embedding 模型名。
- `created_at`：创建时间。
- TODO: 接入 pgvector 后补 `embedding vector` 字段。

`qa_logs`

- `id`：问答日志主键。
- `question`：用户问题。
- `answer`：系统回答。
- `sources`：检索到的证据片段。
- `top_k`：检索数量。
- `llm_provider` / `llm_model`：模型配置。
- `latency_ms`：响应耗时。
- `created_at`：创建时间。
