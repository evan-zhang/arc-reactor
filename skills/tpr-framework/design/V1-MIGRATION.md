# TPR Skill v1 to v2 迁移映射表

本表记录了 v1 版本中所有分散的旧规则在 v2 中的新归属地。供查阅和追溯使用。

| 原归属地 (v1) | 内容 / 概念 | 现归属地 (v2) | 处理方式 |
|--------------|------------|--------------|----------|
| `skills/tpr-framework/SKILL.md` (旧入门) | 三层分工定义 | `SKILL.md` | 精简并重归纳为入口的三层角色表 |
| `skills/tpr-framework/SKILL.md` (旧入门) | Battle 机制（部分） | `references/battle-protocol.md` | 重构，强化审查层作为 Probe 角色的定义 |
| `gateways/.../spawning-guide.md` | Sub-agent 派遣流 | `references/orchestrator-ops.md` | 合并至 Orchestrator Guardrails |
| `gateways/.../best-practices.md` | 编排防线 | `references/orchestrator-ops.md` | 合并，作为 Layer 2 防线 |
| `gateways/.../TPR-framework.md` | 完整执行流程纲要 | `references/tpr-execution.md` | 按四阶段重构 |
| `gateways/.../TPR-framework.md` | 洞察阶段、各种工具包 | `references/tpr-cognitive.md` | 拆出思维方式，并强化为 T/P/R 认知模型 |
| `gateways/.../TPR-pattern.md` | 多 Agent 协作模式 16 条 | `references/multi-agent-pattern.md` | 精简保留核心规则 |
| `gateways/.../methodology/V1/manifest` | 项目分级方案 (Simple/Standard/Complex) | `references/project-grading.md` 和 `references/templates/` | 分割：判断逻辑归 grading，模板归 templates |
| `gateways/.../AGENTS.md` (旧项目级) | 方法论防线及编排者职责 | `SKILL.md` 的 Layer 1 红线及 `orchestrator-ops.md` | 从项目 workspace 踢出，收敛为 Skill 防线 |
| 各子 agent `SOUL.md` | 各省细化工作说明 | `references/tpr-cognitive.md` 及相关流程文件 | 从项目 workspace 踢出，由 Orchestrator 直接通过 Spawn 指令传递或指令自取 |

## 遗弃的概念
- 部分无用或不再推进的临时协同尝试文件（如 `bindings-guide.md` 中属于 OpenClaw 平台配置层面的琐碎细节）。

## 给使用者的建议
如果是第一次接触 TPR，请**不要**按本表去反向找旧文件。直接从 v2 的 `SKILL.md` 入口开始，根据自身的任务类型由判断矩阵决定进入“TPR 思维”或者“TPR 全流程”，然后通过指令自动或手动加载相应的文件即可。
