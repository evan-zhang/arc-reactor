# RT-027: Fact Index Verification (Issue #27)

## 1. 简介 (Introduction)
本项目实现了“三层知识架构”中的第二层：Fact Index（事实索引）。本规约旨在验证其核心逻辑：结构化解析 CWork 报告中的事实，并支持去重与精准查询。

## 2. 核心规约 (Core Protocols)

### 2.1 格式要求
- **输入**：必须采用 `### ID-XXX: 标题` 格式。
- **元数据**：必须包含 `- 时间`, `- 作者`, `- 摘要` 等字段。

### 2.2 归档规范
- **命令**：使用 `archive-manager.py --type fact-index --stdin`。
- **存储**：结果必须落盘至 `wiki/index-facts.json`。

### 2.3 验证计划
- [x] 验证结构化解析（金额、日期、项目提取）。
- [x] 验证全局去重逻辑。
- [x] 验证基于 `--filter` 的多字段查询。

---
*Verified at: 2026-04-09 | Closed under Issue #27*
