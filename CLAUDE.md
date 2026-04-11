# CLAUDE.md — AI Agent 协作规范

本项目有多个 AI Agent 并行开发（Codex、Claude Code、OpenClaw 子 Agent），共用同一 GitHub 账户。

## 开始工作前必读

详见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 核心规则（5 条）

1. **所有改动走 PR**：禁止直接 push main，Branch Protection 已开启
2. **分支名加前缀**：`codex/{number}-描述`、`claude/{number}-描述`、`orchestrator/{number}-描述`
3. **Commit 标注作者**：`feat: xxx (by Codex)` 或 `(by Claude)`
4. **改之前先查 Issue**：`gh issue list` 看有没有人已经在做
5. **PR 合入前确认没丢功能**：`git diff main...HEAD --stat` 检查

## 核心架构概览

### Three-Tier Knowledge Architecture（三层知识架构）

```
Layer 1: Raw（原始素材层）
  reports/YYYY-MM-DD/raw/
  转录稿、截图、PDF — 只读存储

Layer 2: Wiki（知识编译层）
  knowledge/
  ├── entities/     实体页（项目/人物/公司）
  ├── concepts/     概念页（术语/方法论）
  ├── comparisons/  对比页（A vs B）
  └── index.md      知识导航目录

Layer 3: Schema（规则层）
  SKILL.md, references/ — 定义编译行为
```

### Two-Tier Output（双层输出）

- **Display Layer**：≤200 字，结论先行，包含判断（重要性/行动建议/可信度）
- **Archive Layer**：完整的 "4 连击" 归档（Source, Entity, Index, Log）

### Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `archive-manager.py` | 知识归档核心工具 | `--type source/entity/index/log --stdin` |
| `context-injector.py` | 潜知识注入 | `--query "用户问题"` |
| `weekly-reporter.py` | 周报聚合 | `--days 7` |
| `governance-audit.py` | 治理审计（提交前必查） | 直接运行 |
| `media-extractor.py` | 音视频转录 | YouTube URL 或本地文件 |

## 常用开发命令

### 验证与测试
```bash
# 运行完整验证套件（v4.2.0+）
bash verify-v42.sh

# 验证 archive-manager 功能
python3 skills/arc-reactor/scripts/archive-manager.py --help

# 提交前必须运行治理审计
python3 skills/arc-reactor/scripts/governance-audit.py
```

### RT 工作流
```bash
# 查看所有 RT 状态
cat RT/index.yaml

# 创建新 RT（手动编辑 index.yaml 并创建目录）
# RT-XXX/spec-lite.md 或 RT-XXX/spec-full.md

# 查看特定 RT 规范
cat RT/RT-010/spec-full.md
```

### 知识归档示例
```bash
# 4 连击归档（source）
cat << 'EOF' | python3 skills/arc-reactor/scripts/archive-manager.py --type source --topic "标题" --stdin
---
title: 标题
date: 2026-04-11
tags: [tag1, tag2]
---
# 内容
EOF

# 创建实体
cat << 'EOF' | python3 skills/arc-reactor/scripts/archive-manager.py --type entity --topic "实体名" --stdin
# 实体名
描述内容
EOF

# 更新索引
echo "- [[实体名]]: 描述" | python3 skills/arc-reactor/scripts/archive-manager.py --type index --stdin

# 记录日志
echo "操作描述" | python3 skills/arc-reactor/scripts/archive-manager.py --type log --stdin
```

### Ingest 任务派发模式（重要）

当需要摄入 URL 或分析内容时：
1. **禁止** Orchestrator 自己执行 Ingest
2. **必须** spawn sub agent 执行完整的 4 连击
3. **使用** 模板：`skills/arc-reactor/references/spawn-template.md`

## PR 审查清单

- [ ] 改了哪些文件？确认没有误删
- [ ] `python3 skills/arc-reactor/scripts/archive-manager.py --help` 功能完整
- [ ] 运行 `bash verify-v42.sh` 通过
- [ ] 运行 `python3 skills/arc-reactor/scripts/governance-audit.py` 通过
- [ ] 没有跟其他 open PR 冲突：`gh pr list`
- [ ] 如果有冲突：先 rebase 最新 main
- [ ] Commit 消息包含 `(by AgentName)`

## 快速开始

```bash
# 1. 查现有 Issue 和 RT
gh issue list
cat RT/index.yaml

# 2. 拉最新代码建分支
git fetch origin && git checkout -b claude/{issue-number}-{描述} origin/main

# 3. 写代码 + 测试
bash verify-v42.sh  # 如适用

# 4. 提交前审计
python3 skills/arc-reactor/scripts/governance-audit.py
git commit -m "feat: xxx (by Claude)"

# 5. 提 PR
git push origin claude/{issue-number}-{描述}
gh pr create --base main

# 6. 审查 + 合入
gh pr merge
```

## v4.3.0 新功能：Media Extractor

视频/音频转录模块已集成，依赖：
- `mlx-whisper`：本地转录引擎
- `yt-dlp`：视频下载工具

安装依赖：
```bash
pip install -r components/media-extractor/requirements.txt
```

使用方式：
```bash
python3 skills/arc-reactor/scripts/media-extractor.py --url "https://youtube.com/..."
# 或
python3 skills/arc-reactor/scripts/media-extractor.py --file /path/to/video.mp4
```
