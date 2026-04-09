# ARC Reactor v4.1 — AI Agent 知识编译引擎

[![OpenClaw](https://img.shields.io/badge/Ecosystem-OpenClaw-blue.svg)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/Version-4.1.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

> ARC = **Acquire** (获取) → **Research** (研究) → **Catalogue** (编目)

ARC Reactor 把任何信息源（文章、视频、工作汇报）编译成结构化的个人知识库。基于 Karpathy 风格的 Wiki 架构，支持多知识库实例、事实索引、Obsidian 同步。

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 📥 **Ingest** | 给一个链接 → 自动提取 → 生成 Source + Entity + Index + Log |
| 🔍 **Query** | 从知识库中语义检索，回答你的问题 |
| 🩺 **Lint** | 健康检查：断链、格式、缺失字段 |
| 📚 **多知识库** | 个人学习、工作协同、项目知识——天然隔离 |
| 📊 **事实索引** | 结构化 JSON 索引，按人/项目/金额/类型精准查询 |
| 📱 **Obsidian 同步** | 自动同步到你的 Obsidian 仓库 |

---

## 📦 安装

```bash
# 1. 下载最新 Release
curl -L https://github.com/evan-zhang/arc-reactor/releases/download/v4.1.0/arc-reactor-v4.1.0.tar.gz | tar -xz

# 2. 放到 OpenClaw skills 目录
mv arc-reactor ~/.openclaw/skills/

# 3. 验证安装
python3 ~/.openclaw/skills/arc-reactor/scripts/archive-manager.py --help
```

---

## 🎯 使用案例

### Case 1：存一篇技术文章

**你说：**
> 帮我存一下这篇文章 https://karpathy.github.io/2024/01/03/chatgpt-is-blazing/

**AI 做什么：**
1. 抓取文章内容
2. 编译成 Source（原始资料）
3. 提取 Entity（关键概念：ChatGPT、RLHF、RLGA）
4. 更新 Index（知识索引）
5. 回复你："✅ 已入库，提取了 3 个核心概念"

**之后你可以问：**
> ChatGPT 的训练方法有什么创新？

**AI 从知识库里直接回答，不是从网上现搜。**

---

### Case 2：建一个工作知识库

**你说：**
> 帮我新建一个知识库，存工作协同的汇报数据

**AI 做什么：**
1. `--kb-init --root cwork-kb --name "工作协同"` 创建独立知识库
2. 跟个人学习库完全隔离
3. 之后拉工作汇报自动归到这个库

---

### Case 3：查项目进展

**你说：**
> SFE 项目现在进展怎么样？有什么困难？

**AI 做什么：**
1. 查事实索引：`--query-facts --filter "project=SFE系统"`
2. 找到相关汇报（验收公示、奖金申请）
3. 综合回答："SFE 两项子项目验收通过，评分 5/5，奖金 1 万元待审批。注意德镁试点日反馈只有 16 条，活跃度可能需要关注。"

**不用翻 367 条未读汇报，一句话出答案。**

---

### Case 4：查某个同事在做什么

**你说：**
> 屈军利最近在忙什么？

**AI 做什么：**
1. 事实索引过滤：`--query-facts --filter "author=屈军利"`
2. 列出他最近的所有汇报和任务
3. 回复："最近主要在推 Skill 闭环测试（已通过）、AI 成本日报（自动运行）、GitHub 组织管理流程"

---

### Case 5：健康检查

**你说：**
> 帮我检查一下知识库有没有问题

**AI 做什么：**
```
python3 archive-manager.py --lint --root arc-reactor-doc
```
输出：58 个文件、41 个实体、115 条链接、197 个待修复问题

---

## 🏗️ 架构

```
信息源（URL / 文件 / API）
        ↓
   ┌────────────┐
   │  Ingest    │  4 次操作：Source → Entity → Index → Log
   └─────┬──────┘
         ↓
   ┌────────────┐
   │  Wiki 知识库 │  多实例隔离
   └─────┬──────┘
         ↓
   ┌────────────┐
   │  Query     │  事实索引 / 实体检索 / 跨库搜索
   └────────────┘
```

---

## 📂 目录结构

```
arc-reactor/
├── scripts/
│   └── archive-manager.py    # 核心归档引擎（959行）
├── references/
│   ├── spawn-template.md     # Worker spawn 模板
│   ├── output-style.md       # 输出样式规范
│   └── dedup-rules.md        # 去重规则
├── arc-reactor-config.yaml   # 路由配置
├── SKILL.md                  # Agent 主控协议
├── CLAUDE.md                 # AI 协作规范
└── CONTRIBUTING.md           # 多 Agent 协作指南
```

---

## 🤝 多 Agent 协作

本项目支持多个 AI Agent 并行开发，详见 [CONTRIBUTING.md](./CONTRIBUTING.md) 和 [CLAUDE.md](./CLAUDE.md)。

---

*Created by [Evan Zhang](https://github.com/evan-zhang) | ARC Reactor v4.1.0*
