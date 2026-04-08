# RT-001 工作指引 (SOP)
> 本文档是 TPR Framework 维护的标准操作规程。任何 Agent 在首次或重新接手本 RT 时，必须先阅读本文件。

---

## 0. 你在哪、你是谁、你要干什么

- **本 RT 管什么**：TPR Framework —— 一个基于"三省六部制"的 Multi-Agent 协作 Skill。
- **你的角色**：维护工程师。负责修复 Bug、增强能力、发布新版本。
- **绝对铁律**：任何修改都必须走完下面的完整流程，禁止"偷偷改完就跑"。

---

## 1. 接手检查清单 (Resume Checklist)

每次重新打开本 RT 时，请按顺序执行：

- [ ] **阅读本 SOP**（你正在做的事）
- [ ] **阅读 `repos.md`**：确认远程仓库地址与本地三条路径映射
- [ ] **阅读 `spec-lite.md`**：回忆 TPR 的核心设计哲学（编排者、三省、飞轮）
- [ ] **阅读 `changelog.md`**：了解上次改了什么、版本停在哪
- [ ] **检查分支**：`git branch` 确认当前在 master，尚无遗留的 feature 分支
- [ ] **检查同步**：对比 `skills/tpr-framework/` 与 `~/tpr-framework-repo/tpr-framework/` 是否一致

---

## 2. 日常维护流程 (Standard Workflow)

```
用户提需求 → 建分支 → 改代码 → 本地验证 → 提交 → 同步 GitHub → 固化
```

### Step 1: 建立保护分支
```bash
cd ~/.openclaw
git checkout -b feature/RT-001-<简短描述>
```

### Step 2: 修改 Skill 源码
- **唯一编辑位置**：`~/.openclaw/skills/tpr-framework/`
- 修改后在本 RT 的 `changelog.md` 中追加记录

### Step 3: 本地提交
```bash
git add skills/tpr-framework/ RT/RT-001/changelog.md
git commit -m "<type>(tpr): <描述>

Refs: RT-001"
```

### Step 4: 同步到 GitHub 镜像
```bash
cd ~/tpr-framework-repo
rsync -av --delete --exclude='.git' ~/.openclaw/skills/tpr-framework/ ./tpr-framework/
git add -A
git commit -m "<type>: <描述>  Refs: RT-001"
git push origin main
```

### Step 5: 合并回主干并固化
```bash
cd ~/.openclaw
git checkout master
git merge --no-ff feature/RT-001-<简短描述>
git branch -d feature/RT-001-<简短描述>
```

---

## 3. 发版流程 (Release Workflow)

当积累了足够的改动需要发新版时：

1. 更新 `skills/tpr-framework/_meta.json` 中的版本号
2. 打包：`tar -czf RT/RT-001/releases/tpr-framework-v<X.Y.Z>.tar.gz -C ~/.openclaw/skills tpr-framework`
3. 同步推送到 GitHub（按 Step 4）
4. 在 `changelog.md` 中写入版本发布记录
5. 在 `.openclaw` 仓库打标签：`git tag tpr-v<X.Y.Z>`

---

## 4. 关键路径速查表

| 资源 | 路径 |
|------|------|
| Skill 运行时源 | `~/.openclaw/skills/tpr-framework/` |
| GitHub 本地镜像 | `~/tpr-framework-repo/` |
| RT 管理档案 | `~/.openclaw/RT/RT-001/` |
| 发行包存储 | `~/.openclaw/RT/RT-001/releases/` |
| 远程仓库 | `https://github.com/evan-zhang/tpr-framework.git` |

---

## 5. 禁忌清单 (Anti-Patterns)

| ❌ 禁止行为 | ✅ 正确做法 |
|------------|------------|
| 直接在 master 上改代码 | 必须先建 feature 分支 |
| 只改本地不推 GitHub | 每次提交后必须同步推送 |
| 把发行包丢在根目录 | 统一存入 `RT/RT-001/releases/` |
| 规划文档只留在对话里 | 必须落盘到 RT 目录下的 plan 文件 |
| 改完代码不更新 changelog | 每次修改必须追加 changelog 条目 |
