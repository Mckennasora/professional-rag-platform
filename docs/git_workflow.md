# Git Workflow

本文档约定本项目的 Git 使用规范，为后续 GitHub Actions 自动测试、构建和部署做准备。

## 基本原则

- `main` 分支保持可运行、可展示、可发布。
- 所有功能开发优先从独立分支完成，再合并回 `main`。
- 每次提交只做一类事情，避免把功能、重构、格式化、文档混在一个 commit。
- tag 只打在已经通过测试、适合留档或发布的 commit 上。
- 不提交 `.env`、原始私有文档、密钥、真实评测数据或未脱敏日志。

## 分支规范

推荐分支：

- `main`：稳定主分支。
- `dev`：可选，阶段性集成分支。项目早期可以先不用。
- `feature/<name>`：新功能，例如 `feature/document-upload`。
- `experiment/<name>`：实验代码，例如 `experiment/chunk-size`。
- `fix/<name>`：问题修复，例如 `fix/chat-schema-validation`。
- `docs/<name>`：文档更新，例如 `docs/roadmap-update`。
- `ci/<name>`：流水线配置，例如 `ci/pytest-workflow`。

当前项目早期推荐简单流程：

```bash
git checkout -b feature/minimal-rag
uv run pytest
git add .
git commit -m "feat: initialize minimal FastAPI RAG skeleton"
git checkout main
git merge feature/minimal-rag
```

## Commit 规范

使用接近 Conventional Commits 的格式：

```text
<type>: <short summary>
```

常用 `type`：

- `feat`：新增功能。
- `fix`：修复问题。
- `docs`：文档变更。
- `test`：测试相关。
- `refactor`：不改变行为的重构。
- `chore`：依赖、配置、脚手架等杂项。
- `ci`：GitHub Actions 或流水线配置。
- `exp`：实验代码、实验结果或研究记录。

示例：

```bash
git commit -m "feat: add mock chat endpoint"
git commit -m "docs: add roadmap and architecture notes"
git commit -m "test: add health and chat endpoint tests"
git commit -m "ci: add pytest workflow"
git commit -m "exp: add chunk size baseline results"
```

## Tag 与版本号

推荐使用语义化版本：

```text
v<major>.<minor>.<patch>
```

含义：

- `major`：重大架构变化或不兼容 API 变化。
- `minor`：新增阶段性功能，例如文档入库、向量检索、混合检索。
- `patch`：修复、文档补充、小范围改进。

项目早期可以按阶段打 tag：

- `v0.1.0`：项目骨架、health、mock chat。
- `v0.2.0`：最小 RAG 流程。
- `v0.3.0`：文档入库 pipeline。
- `v0.4.0`：chunk 实验。
- `v0.5.0`：BM25 / Vector / Hybrid 检索对比。
- `v0.6.0`：Hybrid + Rerank。
- `v0.7.0`：评测集与 RAGAS。
- `v1.0.0`：可展示工程版本。

创建带说明的 tag：

```bash
git tag -a v0.1.0 -m "v0.1.0: initialize FastAPI project skeleton"
```

推送 tag：

```bash
git push origin v0.1.0
```

推送所有本地 tag：

```bash
git push origin --tags
```

查看 tag：

```bash
git tag
git show v0.1.0
```

删除本地 tag：

```bash
git tag -d v0.1.0
```

删除远程 tag：

```bash
git push origin :refs/tags/v0.1.0
```

## Release 建议

每个阶段性 tag 对应一份 GitHub Release：

- 说明本版本新增了什么。
- 说明如何运行。
- 记录测试结果。
- 附上关键实验结果或文档链接。
- 标注已知限制和下一阶段计划。

示例 release note：

```text
## v0.1.0

### Added
- FastAPI application skeleton.
- GET /health.
- POST /api/chat mock response.
- uv-based dependency management.

### Verified
- uv sync
- uv run pytest
- uv run uvicorn app.main:app --reload

### Limitations
- No real document ingestion, embedding, retrieval, rerank, or LLM integration yet.
```

## 为 GitHub Actions 做准备

后续流水线建议分三步加，不一次性做重：

1. 自动测试：
   - 触发：`push` 到 `main`、`pull_request` 到 `main`。
   - 命令：`uv sync`、`uv run pytest`。

2. 质量检查：
   - 后续引入 `ruff`、`mypy` 后再开启。
   - 命令：`uv run ruff check .`、`uv run mypy app`。

3. 发布或部署：
   - 触发：推送 tag，例如 `v*.*.*`。
   - 行为：构建 Docker 镜像、生成 release notes、部署到测试环境。

推荐触发规则：

```yaml
on:
  push:
    branches: [main]
    tags: ["v*.*.*"]
  pull_request:
    branches: [main]
```

推荐第一版 workflow 名称：

```text
.github/workflows/test.yml
```

第一版只跑测试即可，等项目进入阶段 1 或阶段 2 后再加入 Docker build 和部署。

## 常用检查命令

提交前：

```bash
git status
uv run pytest
```

查看最近提交：

```bash
git log --oneline --decorate -n 10
```

查看当前分支和 tag：

```bash
git branch
git tag
```

查看某个文件改动：

```bash
git diff README.md
```

查看暂存区：

```bash
git diff --cached
```

## 建议的阶段节奏

- 完成一个可运行阶段后合并到 `main`。
- 测试通过后打 tag。
- tag 推送到 GitHub 后由 Actions 自动跑测试。
- 若是重要阶段，创建 GitHub Release。
- 实验结果、评估报告和论文笔记也随版本留档。

这样做的好处是，每个阶段都有明确代码快照，后续写论文、回看实验、准备简历和排查问题时都能追溯。
