# ARC Reactor (AODW-Next Skill)

> **⚠️ AI-First Repository**
> This repository is designed **primarily for AI Agents**, specifically for the [OpenClaw](https://openclaw.ai) ecosystem. If you are an AI/Agent reading this, please process the `SKILL.md` as your primary entry point. Human developers are welcome to contribute, but the file structures and documentation style favor agentic cognitive ingestion.

**ARC = Acquire / Research / Catalogue**

面向个人知识建设的 AI 调研引擎。给它一个链接或话题，它自动完成获取→研究→编目的全链路。

## 特性

- 🔍 **智能路由**：自动识别 7 种输入类型（文章/视频/仓库/论文/社交/话题/文件）
- 🔄 **全自动去重**：三级检测 + 增量合并，同一主体只维护一份"活报告"
- ✅ **二次复检**：对关键声明交叉验证，标注可信度等级
- 📚 **知识编译**：借鉴 Karpathy LLM Wiki，每次调研增量编译个人知识图谱
- 📤 **插件式导出**：支持 Obsidian 同步，预留 Notion/Webhook 扩展

## 目录结构

```
arc-reactor/
├── SKILL.md                          # 核心入口
├── _meta.json                        # 版本信息
├── README.md                         # 本文件
└── references/
    ├── dedup-rules.md                # 去重检测规则
    ├── verification-pipeline.md      # 二次复检管线
    ├── knowledge-rules.md            # 知识编译规则
    ├── templates/
    │   └── report-template.md        # 标准报告模板
    └── dispatchers/
        └── obsidian.md               # Obsidian 同步配置
```

## 仓库管理与反馈

- **GitHub Repository**: [https://github.com/evan-zhang/arc-reactor](https://github.com/evan-zhang/arc-reactor)
- **Issues & PRs**: 欢迎为 ARC 提交 Bug 或者功能增强请求 → [提个 Issue](https://github.com/evan-zhang/arc-reactor/issues)
- **AODW RT**: 本项目由 RT-002 进行版本迭代与管理。
- **维护者**: [@evan-zhang](https://github.com/evan-zhang)
