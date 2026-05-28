# Roadmap

## 阶段 0：项目初始化与定题

参考周期：约 1 周

实际完成时间：2026-05-27

目标：

- 搭建项目目录结构。
- 初始化 FastAPI 服务。
- 写清楚项目目标、技术栈和研究问题。
- 确定项目主线：专业文档 RAG 知识库系统。

成果：

- README.md
- docs/roadmap.md
- docs/architecture.md
- FastAPI health check 接口

## 阶段 1：最小 RAG 系统

参考周期：约 1-2 周

实际完成时间：2026-05-27

目标：

- 实现最小问答接口。
- 支持上传或读取一份本地文档。
- 实现文本切分、embedding、向量检索、LLM 回答的最小流程。

成果：

- POST /api/chat
- POST /api/documents/upload
- 简单 answer + sources 返回格式
- 最小 demo 数据

## 阶段 2：文档入库 pipeline

参考周期：约 2-4 周

实际完成时间：2026-05-28

目标：

- 将文档上传、解析、清洗、切分、embedding、入库流程规范化。
- 保存 document、chunk、metadata、问答日志等数据。

成果：

- scripts/ingest.py
- documents 表设计：已完成 ORM 草案
- chunks 表设计：已完成 ORM 草案
- qa_logs 表设计：已完成 ORM 草案
- chunk 元数据：source、page、section、chunk_id：已在本地索引中保留字段

当前状态：

- 已有 PostgreSQL + 本地 JSON 镜像版入库 pipeline，可支持接口上传和 `scripts/ingest.py` 离线入库。
- 已记录原文路径、清洗后路径、chunk、embedding model 和问答日志。
- 已接入 PostgreSQL，`documents`、`chunks`、`qa_logs` 表可自动创建。
- 当前 embedding 暂以 JSON 字段保存，后续向量检索阶段再迁移到 pgvector `vector` 类型。

## 阶段 3：chunk size 与 overlap 实验

参考周期：约 2-3 周

实际完成时间：

目标：

- 比较不同 chunk size 和 overlap 对检索质量和回答质量的影响。
- 解释为什么某个 chunk size 更适合专业文档。

成果：

- experiments/chunk_size/
- chunk size 对比实验脚本
- chunk size 对比结果表
- docs/experiment_plan.md 中记录实验设计

## 阶段 4：检索方式对比

参考周期：约 3-4 周

实际完成时间：

目标：

- 实现 BM25 检索、向量检索和混合检索。
- 比较三种检索方式在专业文档问答中的表现。

成果：

- retriever_service.py 支持多检索模式
- BM25 / Vector / Hybrid 对比实验
- 能解释为什么混合检索比单纯向量检索更稳

## 阶段 5：Rerank 与引用溯源

参考周期：约 3-4 周

实际完成时间：

目标：

- 在混合检索后加入 reranker。
- 提升 top-k 证据片段质量。
- 返回答案引用来源。

成果：

- rerank_service.py
- Hybrid + Rerank 检索链路
- 引用溯源格式
- rerank 前后对比实验

## 阶段 6：评测集构建

参考周期：约 3-4 周

实际完成时间：

目标：

- 构建 100-300 条专业文档问答评测集。
- 每条数据包含 question、ground_truth、evidence、type、difficulty。

成果：

- data/eval/eval_questions.json
- data/eval/ground_truth.json
- 问题类型分类
- 证据片段标注

## 阶段 7：RAGAS 与自建评估

参考周期：约 2-4 周

实际完成时间：

目标：

- 使用 RAGAS 或自建指标评估 RAG 系统。
- 分别评估检索侧和生成侧表现。

成果：

- scripts/evaluate.py
- context precision
- context recall
- faithfulness
- answer relevancy
- response time
- docs/evaluation_report.md

## 阶段 8：论文与技术报告

参考周期：约 4-8 周

实际完成时间：

目标：

- 将系统设计、实验结果和错误案例整理为论文或技术报告。

成果：

- docs/paper_notes.md
- docs/technical_report.md
- 系统架构图
- 方法流程图
- 实验结果表
- 错误案例分析

## 阶段 9：工程化与简历化

参考周期：约 2-4 周

实际完成时间：

目标：

- 补齐 Docker、日志、配置、README、接口文档和示例数据。
- 形成可展示项目。

成果：

- docker-compose.yml
- .env.example
- README.md 完整版
- API 文档
- GitHub 脱敏版
- 简历项目描述
