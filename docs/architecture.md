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

## 第一版调用链

```text
POST /api/chat
  -> app/api/routes_chat.py
  -> app/services/rag_service.py
  -> mock ChatResponse(answer, sources)
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
