# EP-OPENHARNESS-001：OpenHarness — Claude Code 开源平替深度解析

> **来源**: https://github.com/HKUDS/OpenHarness
> **团队**: HKUDS（香港大学数据科学实验室）
> **核心受众**: AI Agent 开发者、Claude Code 用户、关注开源 Agent 框架的研究者
> **调研日期**: 2026-04-08

---

## 一、项目概述

### 1.1 什么是 OpenHarness

OpenHarness 是港大 HKUDS 团队开源的轻量级 AI Agent Harness，用 **~11,700 行 Python** 实现了 Claude Code 的核心能力。定位为 Claude Code 的开源平替——44 倍轻量、98% 工具覆盖、模型无关。

**核心战绩**：
- 4 天 GitHub Trending
- 6.2k+ Stars（快速增长中）
- 完全兼容 Anthropic Skills 和 Claude Code 插件生态
- 支持任意 LLM（Ollama 本地 / OpenAI / Anthropic / Deepseek / Qwen）

### 1.2 设计哲学

三个关键词：**Clarity（清晰）、Hackability（可 hack）、Compatibility（兼容）**

目标不是复刻 Claude Code 的全部功能，而是提供一个**可理解的生产级 Agent 框架**——让研究者和开发者能真正看懂 Agent 是怎么运作的，而不是面对一个 50 万行 TypeScript 的黑盒。

---

## 二、核心架构：10 大子系统

### 2.1 子系统总览

| 子系统 | 功能 |
|--------|------|
| **Agent Loop** | 流式 Tool-Call 循环，API 指数退避重试，并行工具执行，Token 计数与成本追踪 |
| **Harness Toolkit** | 43+ 工具（文件/Shell/搜索/Web/MCP），按需加载 .md Skills，插件生态 |
| **Context & Memory** | CLAUDE.md 自动发现与注入，自动紧凑上下文压缩，持久化 MEMORY.md，会话恢复 |
| **Governance** | 多级权限（ask/trust/deny），路径级/命令级规则，工具前后置 Hook，交互式审批 |
| **Swarm Coordination** | 子 Agent 派遣/委托，团队注册/任务管理，后台任务生命周期 |
| **Git Integration** | AI 编辑自动 git commit，`/undo` 撤销支持 |
| **CI/CD Mode** | Headless 模式，适合自动化流水线 |
| **Terminal UI** | React + Ink 终端界面 |
| **Skill System** | 兼容 Anthropic Skills 标准，.md 文件按需加载 |
| **Multi-LLM** | 统一接口，Ollama/OpenAI/Anthropic/Deepseek/Qwen 一键切换 |

### 2.2 核心工作流

```
用户输入 → Agent Loop（流式 Tool-Call）
  ↓
工具调用 → Governance 检查（权限/Hook） → 执行
  ↓
结果 → Context 压缩（超限时自动 compact） → 下一轮
  ↓
AI 编辑 → 自动 git commit → 可 /undo
```

---

## 三、与 Claude Code 深度对比

| 维度 | Claude Code | OpenHarness |
|------|-------------|-------------|
| **代码量** | ~500k+ 行 TypeScript | ~11.7k 行 Python（**44x 轻量**） |
| **工具覆盖** | 44+ 工具 | 43+ 工具（**98% 覆盖**） |
| **模型支持** | 仅 Claude | 任意 LLM（Ollama/OpenAI/Deepseek/Qwen...） |
| **Skills 生态** | Anthropic 原生 | 完全兼容 Anthropic Skills + 插件 |
| **可理解性** | 黑盒（50 万行 TS） | 透明（1.2 万行 Python，可读可 hack） |
| **部署方式** | `npm install -g @anthropic-ai/claude-code` | `npm install -g @zhijiewang/openharness` / Python |
| **Git 集成** | 原生 | 原生（auto-commit + /undo） |
| **子 Agent** | 原生支持 | Swarm Coordination（含团队管理） |
| **权限系统** | ask/trust/bypass | ask/trust/deny + 路径级/命令级规则 |
| **价格** | 按 Anthropic 定价 | 可用免费本地模型（Ollama） |

### 关键差距

- **缺少**：Claude Code 的一些高级特性（如完整的 IDE 深度集成、企业级 SSO）
- **优势**：模型自由度、代码可理解性、研究友好性、零成本可用

---

## 四、竞品生态对比

| 项目 | 类型 | Stars | 语言 | 核心差异 |
|------|------|-------|------|---------|
| **OpenHarness** | Agent Harness | 6.2k+ | Python | 44x 轻量，模型无关，学术背景 |
| langchain-ai/open-swe | 异步编码代理 | — | Python | LangChain 生态，异步架构 |
| OpenCode | 终端 AI 编辑器 | — | Go | Go 实现，轻量 |
| claude-hud | Claude Code 插件 | — | — | 上下文/工具进度可视化 |
| learn-claude-code | 纳米级 Claude Agent | — | — | 教学向，从零构建 |
| gsd-build/get-shit-done | 元提示系统 | 热门 Top10 | — | 轻量元提示 + 规范驱动 |

**OpenHarness 差异化**：唯一同时做到「轻量可理解」+「完整工具覆盖」+「模型无关」的开源方案。

---

## 五、适用场景分析

### ✅ 该用的场景
- **研究者**：想理解 Agent 内部机制，需要可读可 hack 的代码库
- **成本敏感团队**：用 Ollama 跑本地模型，零 API 成本
- **多模型需求**：需要在不同 LLM 之间灵活切换
- **教育场景**：官方交互式教程覆盖 Agent Loop / Tools / Memory / Multi-Agent

### ❌ 不该用的场景
- **企业级生产**：缺少 SSO、审计日志、企业级权限管理
- **深度 IDE 集成**：不如 Claude Code 与 VSCode/JetBrains 的原生集成
- **需要 Claude 专属能力**：如 Extended Thinking、原生多模态等

---

## 六、安装与快速上手

```bash
# 安装
npm install -g @zhijiewang/openharness
# 或 Python 方式
pip install openharness

# 配置模型（以 Ollama 本地为例）
openharness config set model ollama:qwen2.5-coder:14b

# 启动
openharness

# 或用云端模型
openharness config set model anthropic:claude-sonnet-4-20250514
```

---

## 七、活跃度与社区评估

| 指标 | 状态 |
|------|------|
| Stars | 6.2k+（4 天 Trending） |
| 开发活跃度 | GitHub Actions CI/CD，持续提交 |
| 社区参与 | 开放 CONTRIBUTING.md，Issues 活跃 |
| 学术背景 | 港大 HKUDS 实验室，有论文支撑 |
| 官方教程 | 交互式教程覆盖核心功能 |
| 风险点 | Star 增长策略讨论（Issue #7），需关注长期维护 |

---

## 八、关键行动建议

| 发现 | 建议 | 优先级 |
|------|------|--------|
| 1.2 万行 Python 实现 98% Claude Code 能力 | 值得深入研究源码学习 Agent 设计 | 🔴 高 |
| 支持任意 LLM + 零成本可用 | 本地开发场景可用 Ollama 替代 Claude Code | 🔴 高 |
| 完全兼容 Anthropic Skills | 现有 Skills 生态可直接复用 | 🟡 中 |
| 缺少企业级特性 | 生产环境慎用，研究/个人开发优先 | 🟡 中 |
| 社区快速增长但仍在早期 | 持续关注，不宜重仓依赖 | 🟢 低 |

---

**一句话评价**：用 1.2 万行 Python 让 AI Agent 不再是黑盒——是目前开源世界最接近「可理解的生产级 Agent 框架」的项目。适合想真正搞懂 Agent 怎么运作的开发者和研究者。

---

*Compiled by ARC Reactor v3.1 | 2026-04-08*
