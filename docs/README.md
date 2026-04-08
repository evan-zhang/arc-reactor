# OpenClaw 文档系统

> 统一文档管理和索引系统
> 由 Nova 自动维护

---

## 📋 概述

这是一个统一的文档管理系统，用于管理所有 OpenClaw Agents 生成的文档、经验总结和系统设计文档。

所有文档存储在 `~/.openclaw/docs/` 目录下，通过 Google Drive 客户端自动同步到云端。

---

## 🎯 使用场景

### 查找文档

1. **浏览**: 查看 `index.md`，按主题或 agent 浏览
2. **搜索**: 使用 Google Drive 搜索功能
3. **询问**: 让 Nova 帮你查找文档

### 查看文档

**在手机上**:
- 打开 Google Drive 应用
- 进入 `openclaw-docs` 文件夹
- 浏览或搜索文档

**在 Mac 上**:
- 直接打开 `~/.openclaw/docs/` 目录
- 使用任何编辑器查看

---

## 📁 目录结构

```
~/.openclaw/docs/
├── 📄 index.json              # 机器可读索引
├── 📄 index.md                # 人类可读目录
├── 📄 README.md               # 本文件
├── 📁 agents/                 # 按 agent 分类
│   ├── assistant-agent/
│   ├── code-agent/
│   ├── stock-agent/
│   ├── trade-agent/
│   ├── ops-agent/
│   ├── docs-agent/
│   └── ai-news/
├── 📁 topics/                 # 按主题分类
│   ├── model-management/
│   ├── discord-operations/
│   ├── agent-integration/
│   └── system-design/
├── 📁 lessons/                # 经验总结
└── 📁 archive/                # 归档
```

---

## 🔄 工作流程

### Nova 生成文档

1. 在本地创建文档
2. 保存到合适的位置（`agents/` 或 `topics/` 或 `lessons/`）
3. 更新 `index.json` 索引
4. 更新 `index.md` 目录
5. 通过 Discord 通知你

### Google Drive 自动同步

1. 文件保存后，Google Drive 客户端自动同步
2. 你可以在手机上立即看到新文档
3. Google Drive 自动保存版本历史

### 查找和阅读

1. 在手机上打开 Google Drive 应用
2. 进入 `openclaw-docs` 文件夹
3. 浏览或搜索需要的文档

---

## 📊 索引系统

### index.json

机器可读的索引文件，包含：
- 所有文档的元数据
- 文件路径和描述
- 创建和更新时间
- 标签和分类

### index.md

人类可读的目录，包含：
- 按主题分类的文档列表
- 按 agent 分类的文档列表
- 文档概述和摘要
- 快速导航链接

---

## 🤖 自动化

Nova 会自动：

1. **创建文档**: 生成文档并保存到合适的位置
2. **更新索引**: 自动更新 `index.json` 和 `index.md`
3. **组织文件**: 按主题和 agent 分类
4. **归档文档**: 定期将旧文档移到 `archive/`
5. **通知变化**: 通过 Discord 通知你新文档

---

## 🔍 搜索技巧

### 通过 Nova 搜索

```
查找关于模型容灾的文档
搜索 Discord 相关的文档
列出所有 assistant-agent 的文档
查找今天创建的文档
```

### 通过 Google Drive 搜索

1. 打开 Google Drive 应用
2. 在 `openclaw-docs` 文件夹中搜索
3. 使用关键词或文件名搜索

---

## 📝 文档类型

### System Design

系统设计和架构文档

### Integration Guide

集成和配置指南

### Lessons

经验总结和最佳实践

### Report

工作报告和完成情况

---

## 🎓 快速开始

### 首次使用

1. 确保已安装并配置 Google Drive 客户端
2. 确认 `~/.openclaw/docs/` 已同步到 Google Drive
3. 在手机上打开 Google Drive 应用
4. 进入 `openclaw-docs` 文件夹
5. 浏览或搜索文档

### 日常使用

- Nova 生成新文档后，Google Drive 会自动同步
- 在手机上随时可以查看最新文档
- 如需查找特定文档，让 Nova 帮你搜索

---

## 🔧 配置

### Google Drive 同步

确保 Google Drive 客户端已配置：
- 同步文件夹：`~/.openclaw/docs/`
- 在 Google Drive 中显示为：`openclaw-docs`
- 自动同步：开启

### 本地编辑

如需编辑文档：
1. 在 Mac 上打开 `~/.openclaw/docs/` 目录
2. 使用任何编辑器编辑
3. 保存后，Google Drive 会自动同步

---

## 📞 支持

如有问题或需要帮助，请联系 Nova。

---

*文档系统 v1.0.0*  
*自动维护系统*  
*最后更新: 2026-02-20*
