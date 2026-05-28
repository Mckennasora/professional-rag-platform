# Professional RAG Platform

面向专业文档的检索增强生成问答系统，目标是逐步支持文档上传、解析、切分、Embedding 入库、混合检索、Rerank、答案生成、引用溯源与 RAG 自动评估。

本项目不是为了简单调用大模型 API，也不是一个普通聊天机器人，而是为了研究和实践专业文档 RAG 系统中的文档切分、检索增强、混合检索、Rerank、引用溯源和自动评估问题。

## 项目背景

项目面向专业文档知识库问答场景，围绕“如何让大模型基于可检索、可引用、可评估的专业文档回答问题”展开。长期目标是形成可展示项目、论文实验材料和实习简历项目。

暂定研究问题：

> 面向专业文档的 RAG 问答系统中，如何通过合理切分、混合检索和重排序，提高检索质量、答案可信度和引用可溯源性？

## 项目目标

- 构建一个可运行的 FastAPI RAG 后端系统。
- 实现文档入库 pipeline：解析、清洗、切分、Embedding、入库。
- 对比 BM25、向量检索、混合检索在专业文档问答中的效果。
- 引入 Rerank 提升 top-k 证据片段质量。
- 返回带 sources 的答案，降低幻觉并支持引用溯源。
- 使用 RAGAS 或自建脚本评估 context precision、context recall、faithfulness、answer relevancy 等指标。
- 沉淀实验结果、错误案例、技术报告和论文材料。

## 技术栈

- Python
- FastAPI
- Pydantic / pydantic-settings
- LangChain
- Sentence Transformers / BGE Embedding
- PostgreSQL + pgvector
- Elasticsearch / OpenSearch
- RAGAS
- pytest
- uv

## 项目结构

```text
professional-rag-platform/
├── app/
│   ├── api/              # Controller 层，定义 HTTP 接口
│   ├── schemas/          # DTO / VO，定义请求响应结构
│   ├── services/         # Service 层，放 RAG 核心业务逻辑
│   ├── repositories/     # Repository / Mapper 层，负责数据访问
│   ├── models/           # Entity，后期放 SQLAlchemy ORM 模型
│   ├── core/             # 配置、日志、环境变量
│   └── db/               # 数据库连接与 session
├── scripts/              # 离线任务：入库、评估、重置数据库
├── data/                 # raw、processed、samples、eval 数据
├── notebooks/            # 实验 notebook
├── experiments/          # chunk、retrieval、rerank 实验材料
├── docs/                 # 路线图、架构、API、实验计划、论文笔记
└── tests/                # 自动化测试
```

## 快速启动

安装依赖：

```bash
uv sync
```

启动服务：

```bash
uv run uvicorn app.main:app --reload
```

运行测试：

```bash
uv run pytest
```

访问：

- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`

## 当前已实现功能

- FastAPI 应用初始化。
- `GET /health` 健康检查。
- `POST /api/documents/upload` 支持 UTF-8 TXT 文档上传、原文保存、清洗、切分、轻量 embedding 和本地索引。
- `POST /api/chat` 支持从本地索引检索 sources，返回 mock answer，并记录本地问答日志。
- 使用 Pydantic 定义 `ChatRequest`、`ChatResponse`、`Source`。
- 使用轻量本地 embedding 跑通最小检索链路。
- 预留真实 Embedding、LLM、Rerank、Repository、ORM 模块。
- 已定义 `documents`、`chunks`、`qa_logs` SQLAlchemy ORM 模型，数据库由后续环境配置接入。
- 初始化 sample 文档和 eval 数据文件。

## Git 与版本控制

项目使用 Git 做阶段化版本管理，推荐在每个稳定阶段通过 tag 固化快照，例如 `v0.1.0` 表示项目骨架和 mock 接口版本。详细规范见 [docs/git_workflow.md](docs/git_workflow.md)。

推荐第一版验证通过后：

```bash
git add .
git commit -m "feat: initialize FastAPI RAG project skeleton"
git tag -a v0.1.0 -m "v0.1.0: initialize FastAPI project skeleton"
```

后续 GitHub Actions 可以基于 `push`、`pull_request` 和 `v*.*.*` tag 触发自动测试、构建和发布。

## 路线图

详细路线图见 [docs/roadmap.md](docs/roadmap.md)。

- [x] 阶段 0：项目初始化与定题
- [x] 阶段 1：最小 RAG 系统
- [x] 阶段 2：文档入库 pipeline
- [ ] 阶段 3：chunk size 与 overlap 实验
- [ ] 阶段 4：检索方式对比
- [ ] 阶段 5：Rerank 与引用溯源
- [ ] 阶段 6：评测集构建
- [ ] 阶段 7：RAGAS 与自建评估
- [ ] 阶段 8：论文与技术报告
- [ ] 阶段 9：工程化与简历化

## 后续扩展方向

短期扩充：

- 接入 PostgreSQL + pgvector，替换当前本地 JSON 索引。
- 实现 PDF 文档解析。
- 使用 sentence-transformers 或 BGE 生成真实 embedding。
- 使用 pgvector 实现向量检索。
- 接入真实 LLM。
- 返回 answer + sources。

中期扩充：

- 接入 PostgreSQL + pgvector。
- 接入 Elasticsearch / OpenSearch 实现 BM25 检索。
- 实现 BM25 + Vector 混合检索。
- 实现 Rerank。
- 记录问答日志。
- 构建专业文档问答评测集。
- 使用 RAGAS 做自动评估。

长期扩充：

- 支持 PDF、Word、Excel、Markdown、HTML 等多格式文档。
- 支持表格和复杂版面解析。
- 支持多知识库、权限控制和多租户。
- 支持模型配置、多 LLM 切换、Query Rewrite、Agentic RAG。
- 支持知识图谱增强 RAG。
- 支持前端管理页面。
- 支持 Docker Compose 一键部署。
- 支持论文实验复现脚本和脱敏后开源展示。

## 与论文和实验的关系

本项目会把工程实现与实验评估放在同一条主线上：先做系统，再做实验，再做评估，最后沉淀论文和简历材料。

计划沉淀的论文材料包括：

- 专业文档 RAG 系统架构。
- 文档切分策略实验。
- BM25 / Vector / Hybrid 检索对比实验。
- Hybrid + Rerank 前后对比实验。
- 自建专业文档问答评测集。
- RAGAS 与自建指标评估结果。
- 错误案例分析和改进方向。
