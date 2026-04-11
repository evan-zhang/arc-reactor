# RT-013: AI-Oriented Development Standards (AODW Governance)

## 1. 简介 (Introduction)
本项目采用 AODW (Agent-Oriented Development Workflow) 开发模式。由于该项目存在多个 AI Agent（如 Antigravity, OpenClaw, Codex 等）协作修改代码，为了防止架构漂移（Architectural Drift）和代码混乱，必须执行严格的治理协议。

## 2. 核心规约 (Core Protocols)

### 2.1 需求驱动制 (RT-Centricity)
- **准则**：禁止在没有对应 RT (Requirement Traceability) 的情况下修改任何代码或文档。
- **操作**：
    1.  开启新任务前，必须在 `RT/index.yaml` 中注册条目。
    2.  创建配套的 `RT/RT-xxx-description.md` 规范。
    3.  所有的 Commit 信息必须引用对应的 RT 编号。

### 2.2 归档工具锁定 (Tool Locking)
- **准则**：禁止通过手动文件操作直接修改 Wiki 知识层。
- **操作**：必须通过 `scripts/archive-manager.py` 命令集（Ingest/Query/Lint/Export）进行所有知识操作，以保证 metadata 的一致性。

### 2.3 原子化提交与作者标注 (Atomic Commits & Attribution)
- **准则**：每个 Commit 应当是原子化的，且必须标注操作 Agent。
- **格式**：`[Type]: [Description] (by [AgentName])`
- **示例**：`feat: implement backlink search in export (by Antigravity)`

### 2.4 分支与 PR 治理 (Branch & PR Governance)
- **分支名格式**：`agent-name/issue-number-description` (例: `openclaw/18-entity-export`)。
- **PR 要求**：
    - 必须包含对应的 Issue 链接。
    - 必须通过 `verify-v42.sh` (或相关测试脚本) 验证。
    - 严禁合并带有 Lint 错误的 PR。

## 3. 角色定义 (Role Definitions)
- **Lead Architect (Antigravity)**: 负责维护整体架构规范，拥有合并代码库核心逻辑的最高权限。
- **Collaboration Agent (OpenClaw/XiaoLongXia)**: 负责执行具体的编译任务、事实提取和特定维度的代码修改。必须严格遵守本规约。

## 4. 冲突处理 (Conflict Resolution)
- 发生文件重叠修改冲突时，以 `RT/` 目录下较新的规范为准。
- 严禁删除其他 Agent 留下的已合入 RT 条目和规范。
