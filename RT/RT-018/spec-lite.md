# RT-018: Branch Unification (Issue #2)

## 1. 简介 (Introduction)

解决 `main` 和 `master` 分支不一致导致用户混淆的问题。根据实际调查，当前状态与 Issue #2 描述相反：
- **main**（默认分支）：最新，领先 master 33 个 commits
- **master**：落后，停留在旧提交

## 2. 现状分析

```bash
# 当前状态（2026-04-11）
origin/main    → bb2584b (最新，含 v4.3.0、RT 整理等)
origin/master  → bae53b6 (落后 33 个 commits)
```

**问题根源：**
1. GitHub 默认分支设置为 `main` ✅
2. 但 `master` 分支仍然存在且落后，可能造成用户混淆
3. 部分 PR 可能被合并到错误的分支
4. ClawHub 等工具可能基于错误分支

## 3. 解决方案

### 方案 A（推荐）：删除 master 分支
```bash
# 1. 确认 main 是最新且正确的
git checkout main
git pull origin main

# 2. 删除远程 master 分支
git push origin --delete master

# 3. 删除本地 master 分支引用
git branch -d master  # 或 git branch -D master 强制删除
```

### 方案 B：将 master 同步到 main（保留向后兼容）
```bash
# 1. 同步 master 到 main 的最新状态
git checkout master
git reset --hard main
git push origin master --force
```

**推荐方案 A**，因为：
- GitHub 默认分支已经是 `main`
- 删除冗余分支可以避免混淆
- 符合现代 Git 最佳实践

## 4. 验收标准

- [ ] 确认 `main` 分支包含所有最新的功能和修复
- [ ] 远程 `master` 分支已删除
- [ ] 本地 `master` 分支引用已清理
- [ ] README 中不再提及 `master` 分支
- [ ] 验证用户 `git clone` 默认获取 `main` 分支
- [ ] 运行 `bash verify-v42.sh` 验证功能完整

## 5. 风险评估

- **低风险**：master 分支已落后且非默认分支
- **影响范围**：主要影响那些显式 checkout master 的用户
- **缓解措施**：在 Issue #2 中更新说明，告知用户使用 main 分支

---
*Created by ClaudeCode (Xiao Long Xia) - 2026-04-11*
