# tpr-framework 设计档案

## 产品概述
- **Slug**：tpr-framework
- **当前版本**：v2.0.0
- **定位**：TPR（Think / Probe / Review）统一工作方法。认知闭环 + 三层四阶段执行框架。

## 核心设计决策

### D-01：为什么要三层分治
AI 在单 Agent 场景下很容易"自问自答"——起草了 GRV 又自己审查，立场天然趋同。三层分治强制把起草/审查/执行拆给不同 sub-agent，批判性审查才有意义。

### D-02：Battle 为什么必须用真实 sub-agent
自己扮演 Menxi 和 Shangshu 时，两个角色共享同一个上下文窗口，审查会无意识偏向起草立场。真实 sub-agent 有独立上下文，立场更中立。

### D-03：Orchestrator "Brain Only, No Hands" 原则
一旦 Orchestrator 开始亲手执行，角色边界彻底崩溃，后续所有角色分工都名存实亡。429/失败 → 重派，不自己动手。

### D-04：T/P/R 认知内核（v2.0 新增）
v1 的 TPR 本质是组织架构（三层分工），只在编排型 agent 上有意义。v2 引入 Think/Probe/Review 认知方法，使任何 agent 都可以使用 TPR（作为思维方法），编排型 agent 可以使用完整流程。这解锁了 Skill 的可移植性。

### D-05：两种使用模式（v2.0 新增）
TPR 思维（任何 agent）和 TPR 全流程（编排型 agent）的分离，通过四项判定矩阵硬切换，避免模糊判断导致使用分裂。

### D-06：红线分层（v2.0 新增）
将规则分为三层：Core Redlines（通用）、Orchestrator Guardrails（全流程）、Battle Rules（Battle 阶段）。避免规则混写和重复。

### D-07：术语现代化 (v2.1.0 新增)
TPR 框架最初借鉴了中国古代官名（中书省、门下省、尚书省）来指代架构角色。为降低用户的认知门槛及与业界协同标准拉齐，在 V2.1.0 撤销所有古代官名，并正式更名为基于机制的现代化分层：策划层 (Planner)、审查层 (Auditor)、执行层 (Executor)。

## 版本历史
| 版本 | 日期 | 摘要 |
|------|------|------|
| v1.0.0 | 2026-03 | 初版：四阶段流程 + 三层角色表 + Critical Rules |
| v1.0.1 | 2026-04-01 | SKILL.md 重构（189→57行），新增 references/，补 design/ 档案 |
| v1.1.0 | 2026-04-05 | SKILL.md 扩展（445行），新增 Hermes 原则、上下文管理等 |
| v2.0.0 | 2026-04-07 | 重大升级：引入 T/P/R 认知内核，两种使用模式，红线三层分类，references/ 全面重构（7文件+templates），SKILL.md 精简为入口（~160行） |
