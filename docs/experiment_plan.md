# Experiment Plan

## 目标

围绕专业文档 RAG 系统，逐步评估文档切分、检索方式、Rerank 和生成质量。

## 计划实验

- 阶段 2 数据沉淀：documents、chunks、qa_logs 的字段稳定性。
- chunk size 与 overlap 对比。
- BM25 / Vector / Hybrid 检索对比。
- Hybrid 与 Hybrid + Rerank 对比。
- 不同 top-k 对 context precision、context recall、faithfulness、answer relevancy 的影响。

## 指标

- context precision
- context recall
- hit rate
- MRR
- faithfulness
- answer relevancy
- response time

TODO: 在阶段 3 开始补充实验脚本、数据集版本和结果表。
