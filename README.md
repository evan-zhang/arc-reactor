# ARC Reactor v4.2 — AI Agent 知识编译引擎 (Subconscious Edition)

[![OpenClaw](https://img.shields.io/badge/Ecosystem-OpenClaw-blue.svg)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/Version-4.2.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

> ARC = **Acquire** (获取) → **Research** (研究) → **Catalogue** (编目)

ARC Reactor 把任何信息源（文章、视频、工作汇报）编译成结构化的个人知识库。基于 Karpathy 风格的 Wiki 架构，支持多知识库实例、潜意识注入、自动化周报。

---

## ✨ 核心能力 (v4.2.0 新特性)

| 能力 | 说明 |
|------|------|
| 🧠 **Subconscious Injection** | **[NEW]** 潜意识注入。Agent 在回答前自动检索 Wiki 命中词条，实现“无感”知识增强。 |
| 📅 **Weekly Executive Brief** | **[NEW]** 自动化周报。一键聚合过去 7 天的摄入内容，通过 AI 生成深度横向洞察。 |
| 📥 **Wiki Ingest** | 给一个链接 → 自动提取 → 生成 Source + Entity + Index + Log (4连击模式) |
| 🩺 **Wiki Lint** | 自动健康检查：修复孤岛词条、断开的 `[[wiki-links]]`。 |
| 📚 **多知识库隔离** | 个人学习、工作协同、项目知识——在配置中一键切换。 |

---

## 📂 项目结构 (Monorepo)

本项目采用 Monorepo 结构，将“研发管理”与“技能分发”严格隔离：
- **`RT/`**: 研发追踪、设计决策与版本档案。
- **`skills/arc-reactor/`**: **[正式发布目录]** 包含 Agent 运行所需的所有脚本、指令与配置。

---

## 📦 安装与挂载

### 1. 克隆代码仓库
```bash
git clone https://github.com/evan-zhang/arc-reactor.git
```

### 2. 在 OpenClaw 中配置
将技能目录指向子路径：`./arc-reactor/skills/arc-reactor`。

### 3. 验证安装
```bash
cd arc-reactor
python3 skills/arc-reactor/scripts/archive-manager.py --help
```

---

## 🎯 新功能实战

### Case 1：潜意识注入 (无感增强)
**现状**：你的库里已有 `[[OpenClaw]]` 的卡片。
**输入**：你直接问：“OpenClaw 怎么部署？”
**效果**：Agent 会在内部静默调用 `context-injector.py`，它会发现“OpenClaw”是已知实体，自动把卡片内容贴在它的思维前方。Agent 还没开口，就已经记住了你的私域知识。

### Case 2：自动化周报 (深度聚合)
**输入**：“生成本周的知识周报。”
**效果**：Agent 运行 `weekly-reporter.py --days 7`。它会扫描过去 7 天所有 `wiki/sources/` 下的文件，告诉你这周主要研究了什么，并提炼出下周的关注建议。

---

## 🏗️ 开发者指南 (AODW 规范)

本项目严格遵守 **AODW-Next** 工程规范：
- 所有开发任务必须通过 `RT (Release Tracker)` 追踪。
- 修改代码前，请先查阅 `RT/index.yaml` 确认当前任务状态。
- 设计决策请见 `RT/RT-XXX/spec-full.md`。

---

*Created by [Evan Zhang](https://github.com/evan-zhang) | ARC Reactor v4.2.0*
