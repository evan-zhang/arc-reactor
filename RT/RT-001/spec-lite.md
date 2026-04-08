# Spec-Lite: RT-001 - TPR Framework 架构心智补完

## 1. 背景（Context）
TPR Framework 旨在解决 AI Agent 在长时任务中的失控、偷懒与注意力管理问题。

## 2. 目标（Goal）
- 建立“三省六部”式的多层分发与审计机制。
- 确立 Orchestrator（编排者）作为系统绝对核心的总控地位。
- 引入量化指标硬卡控（Metrics Baseline）与知识进化（Flywheel）。

## 3. 核心定义：编排者 (Orchestrator)
编排者不仅是入口，更是主宰。
- **职责**：调度、监控、反馈拦截、知识凝练。
- **禁忌**：禁止参与具体的业务代码实现。
- **守候**：在每个门禁点守候甲方的最终判词。

## 4. 协作架构
- **中书省 (Discovery)**：需求洞察与 GRV 契约起草。
- **门下省 (Review)**：主客观并行的争辩式审计。
- **尚书省 (Execution)**：包含自修复环路的高质量交付。

## 5. 影响范围（Scope）
- 全局 Skill 管理逻辑。
- 开发者与 Agent 的交互界面。
