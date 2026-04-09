# RT-002: ARC Reactor (Acquire / Research / Catalogue) Skill 抽离与统一管理 (Intake)

## 原始描述
将目前内嵌在 `chat-main-agent` 的 `AGENTS.md` 中的"调研工作流 SOP"抽离为一个独立 Skill —— **ARC Reactor**，使其可以被任意 Agent 挂载，并通过 RT-002 进行长期维护。

## ARC 是什么
- **A** = Acquire（获取）：接收 URL 或需求描述，抓取原始内容
- **R** = Research（研究）：深度分析、提炼关键信息、交叉验证
- **C** = Catalogue（编目）：按标准格式输出报告，归档至个人知识库（Obsidian）

## 现状分析
### 能力所在位置
- **当前位置**：`~/.openclaw/gateways/life/state/workspace-life/AGENTS.md` 末尾（第 210-229 行）
- **触发方式**：用户在 #资料&调研 频道发送 URL 或需求描述
- **输出格式**：标准化 Markdown 报告（含基本信息表、分章节分析、关联调研索引）

### 既有基础设施
- **cms-sop**（已归档）：包含 Lite/Full 五步流程和四件套文档模板
- **报告产出物**：工作区根目录散落大量已完成报告，可作为模板参考
- **reports/ 目录**：存有 10+ 份编号专题调研报告

### 核心问题
1. 调研逻辑硬编码在 Agent 启动指令中，无法被其他 Agent 复用
2. 报告散落在工作区根目录，没有统一归档机制
3. 没有独立的 SKILL.md 入口，不符合 OpenClaw Skill 标准

## 目标
1. 抽离为独立 Skill：`skills/arc-reactor/`
2. 建立标准化 SKILL.md + references/ 结构
3. 统一报告输出格式与归档路径
4. 纳入 RT-002 长期管理，后续可发布到 GitHub

## 概要估算
- **需求类型**: Enhancement
- **开发范围**: Skill 级别
- **风险等级**: 低风险
- **影响模块**: `arc-reactor`（新建）、`chat-main-agent`（AGENTS.md 瘦身）
- **开发类型**: Spec-Lite
