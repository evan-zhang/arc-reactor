# ARC Reactor

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

## 管理
- **RT**: RT-002
- **维护者**: evan
