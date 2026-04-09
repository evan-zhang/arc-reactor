# ARC Reactor 验收测试方案 v1

> **使用方法**：逐步复制 `📝 发给 Agent` 下的指令，发送给 OpenClaw Agent 执行。
> 每步执行完后检查 `✅ 预期结果`，通过则进入下一步。

---

## 前置条件

- Agent 正在运行，Telegram 会话正常
- 工作区：`/Users/evan/.openclaw/gateways/life/domains/testtpr/workspace`

---

## Phase 1: 安装更新

### Step 1.1: 从 GitHub 拉取最新版本

📝 发给 Agent：
```
请从 https://github.com/evan-zhang/arc-reactor 拉取最新代码，安装到 workspace/skills/arc-reactor/。只安装 skill 核心文件（SKILL.md, scripts/, references/, RT/, _meta.json, README.md, arc-reactor-config.yaml），不要带 .git/ .aodw-next/ .cursor/ components/ 等杂项。安装完告诉我版本号。
```

✅ 预期结果：
- Agent 报告版本号（如 v4.0.5 或更新）
- 无报错

### Step 1.2: 提交到工作区

📝 发给 Agent：
```
git add 并 commit 这次安装更新。
```

### Step 1.3: 重启加载新版本

📝 发给 Agent：
```
重启会话，确保加载新版本 SKILL.md。
```

✅ 预期结果：
- Agent 重启后打招呼
- 新会话已加载最新 skill

---

## Phase 2: 健康检查 (--lint)

### Step 2.1: 运行 Lint 检查

📝 发给 Agent：
```
运行 archive-manager.py --lint，汇报 Wiki 健康状况。告诉我总文件数、实体数、发现问题数。
```

✅ 预期结果：
- 输出 JSON 格式的 lint 报告
- 包含 total_files, total_entities, issues_found 等字段
- 无脚本语法错误

### Step 2.2: 自动修复（可选）

📝 发给 Agent：
```
运行 archive-manager.py --lint --fix，自动修复可修复的问题。修复完汇报修复了什么。
```

✅ 预期结果：
- 报告 fixed 数量
- 孤岛链接对应的 stub 实体文件已创建

---

## Phase 3: 真实 Ingest 测试

### Step 3.1: 发送一条真实链接

📝 发给 Agent：
```
【这里贴一条你感兴趣的科技新闻链接】
```

✅ 预期结果：
- Agent 回复"已派遣 ARC 矿工"
- 矿工在 3 分钟内完成

### Step 3.2: 验证交付

📝 发给 Agent：
```
请验证刚才的 Ingest 结果：
1. 确认 4 个 JSON 回执全部 status: "success"
2. 确认 source 文件包含 date frontmatter
3. 确认文件路径在 arc-reactor-doc/wiki/ 下（不是 skills/arc-reactor/arc-reactor-doc/）
4. 确认 Telegram 附件已发送且用户收到了文件
5. 汇报完整结果
```

✅ 预期结果：
- 5 项全部 ✅
- 用户在 Telegram 收到了 .md 文件附件

### Step 3.3: 验证文件内容

📝 发给 Agent：
```
读出刚才归档的 source 文件前 10 行，确认有 date 字段且内容非空。
```

✅ 预期结果：
- 显示文件内容
- 包含 `date: YYYY-MM-DD`
- 内容是完整的知识编译报告，不是空白或占位符

---

## Phase 4: 去重验证 (--dedup)

### Step 4.1: 重复 Ingest 测试 (skip)

📝 发给 Agent：
```
用 --dedup skip 对刚才同一个 topic 再跑一次 entity 归档，验证是否正确跳过。把命令执行结果告诉我。
```

✅ 预期结果：
- 返回 `"status": "skipped", "dedup": "skipped"`
- 原有文件未被修改

### Step 4.2: 增量追加测试 (merge)

📝 发给 Agent：
```
用 --dedup merge 对刚才的 entity 追加一条新信息："测试追加 - 验证 merge 功能正常"，验证增量合并。把执行结果告诉我。
```

✅ 预期结果：
- 返回 `"status": "success", "dedup": "merged"`
- 文件大小增长

---

## Phase 5: Spawn 模板验证

### Step 5.1: 再发一条链接，观察 token 用量

📝 发给 Agent：
```
【再贴一条新闻链接】
```

✅ 预期结果：
- 如果 spawn 模板已集成到 SKILL.md，Agent 应该引用模板而非手写大段指令
- 矿工正常完成 4 连击

---

## 验收标准汇总

| 阶段 | 检查项 | Pass/Fail |
|------|--------|-----------|
| P1 安装 | 从 GitHub 拉取无报错 | ☐ |
| P1 安装 | 版本号正确 | ☐ |
| P2 Lint | --lint 输出 JSON 无报错 | ☐ |
| P2 Lint | --lint --fix 创建 stub 实体 | ☐ |
| P3 Ingest | 4 连击全部 success | ☐ |
| P3 Ingest | source 有 date frontmatter | ☐ |
| P3 Ingest | 文件路径在正确目录 | ☐ |
| P3 Ingest | 用户收到 Telegram 附件 | ☐ |
| P4 Dedup | skip 正确跳过 | ☐ |
| P4 Dedup | merge 正确追加 | ☐ |

**全部 Pass → 版本可发布。**

---

## 记录

| 日期 | 版本 | 测试人 | 结果 |
|------|------|--------|------|
| 2026-04-08 | v4.0.4 | Agent 自测 | Lint ✅ Dedup ✅ |
| | | | 待用户验收 |
