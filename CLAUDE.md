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

## PR 审查清单

- [ ] 改了哪些文件？确认没有误删
- [ ] `python3 skills/arc-reactor/scripts/archive-manager.py --help` 功能完整
- [ ] 没有跟其他 open PR 冲突：`gh pr list`
- [ ] 如果有冲突：先 rebase 最新 main

## 快速开始

```bash
# 1. 查现有 Issue
gh issue list

# 2. 拉最新代码建分支
git fetch origin && git checkout -b claude/{issue-number}-{描述} origin/main

# 3. 写代码 + 测试 + 提交
git commit -m "feat: xxx (by Claude)"

# 4. 提 PR
git push origin claude/{issue-number}-{描述}
gh pr create --base main

# 5. 审查 + 合入
gh pr merge
```
