# RT-022: Ingest Delivery Checklist (Issue #51)

## 1. 简介 (Introduction)

为 Orchestrator 建立强制性的 Ingest 交付动作检查清单，确保每次 Ingest 完成后都按照标准流程向用户交付结果。

## 2. 问题描述

**现象**：Orchestrator 完成 Ingest 4 连击后，没有自觉执行以下动作：
1. 按 Display Layer 规范（≤200字、结论先行、「·」列表）回复用户
2. 通过 message tool 发送 source 文件附件
3. 给出判断力评估（重要性/行动建议/可信度）

**根因**：输出规范分散在多处，SKILL.md 主文件没有硬性约束：
- Display Layer 规范在 `references/output-style.md` — Orchestrator 不会自动读取
- 发送文件附件埋在 `references/spawn-template.md` 模板末尾 — 不是 Orchestrator 的检查项
- 判断力输出在 SKILL.md 提到"主动建议"但不够明确 — 容易被忽略

## 3. 解决方案

### 3.1 在 SKILL.md 中添加强制性交付清单

在"铁律"部分之后，"事后验证"部分之前，新增"🔔 Ingest 交付清单"章节：

```markdown
## 🔔 Ingest 交付清单（Orchestrator 必须执行）

4 连击完成后，Orchestrator **必须**按顺序执行以下 4 个动作：

### 1. ✅ Display Layer 回复（≤200字，结论先行，「·」列表）

**规范**：
- 字数限制：≤200 字
- 结构要求：结论先行，用「·」列出要点
- 风格要求：自然对话风格，避免技术细节

**示例**：
```
已完成 {主题} 的知识编译。

核心结论：
· 提取了 {主要实体1}、{主要实体2} 的关键信息
· 建立了 {数量} 个知识节点链接
· 已存入 Wiki 供后续查询使用
```

### 2. ✅ 判断力输出（重要性 / 行动建议 / 可信度评估）

**规范**：
- **重要性**：明确标出该信息对用户的价值
- **行动建议**：下一步建议用户做什么
- **可信度**：根据来源评估信息的真实性

**示例**：
```
**我的判断**：
- 重要性：高（核心技术与当前项目相关）
- 建议行动：立即研究其架构设计，考虑集成到现有系统
- 可信度：高（来自官方技术文档）
```

### 3. ✅ 通过 message tool 发送 source 文件附件给用户

**要求**：
- 必须使用 message tool 发送文件附件
- 附件格式：source 文件（Markdown）
- 发送渠道：根据用户使用的平台（Discord/Telegram/其他）

**注意事项**：
- 不要发送 JSON 回执或其他内部文件
- 只发送用户可读的 Markdown 格式文件

### 4. ✅ 禁止将 JSON 回执完整吐给用户（输出解耦）

**要求**：
- 成功回执静默存储在 Archive 层
- 严禁将 JSON 回执完整吐给用户
- 只向用户展示 Display Layer 格式的中文摘要

**错误示例**：
```
✅ 完成 Ingest 4 连击：
1. {"status": "success", "path": "arc-reactor-doc/wiki/sources/...", "size_bytes": 3394}
2. {"status": "success", ...}
```

---

### 交付流程总结

```
Ingest 4 连击完成
    ↓
Orchestrator 验证结果（Post-Worker Validation）
    ↓
执行交付清单：
    1. Display Layer 回复（≤200字）
    2. 判断力输出（重要性/建议/可信度）
    3. 发送 source 文件附件
    4. 确认无 JSON 回执泄露
    ↓
交付完成
```

### 检查清单快速参考

| 步骤 | 动作 | 状态 | 备注 |
|------|------|------|------|
| 1 | Display Layer 回复（≤200字） | ⬜ | 结论先行，「·」列表 |
| 2 | 判断力输出 | ⬜ | 重要性/建议/可信度 |
| 3 | 发送 source 文件附件 | ⬜ | 使用 message tool |
| 4 | 确认无 JSON 回执泄露 | ⬜ | 输出解耦 |

每次 Ingest 完成后，Orchestrator 必须确认所有 4 个步骤都已完成。
```

## 4. 实施细节

### 4.1 位置安排

- **位置**：在"铁律"（The Iron Rules）之后
- **理由**：
  - 铁律规定了"不能做什么"
  - 交付清单规定了"必须做什么"
  - 两者形成完整的约束体系
  - 放在显眼位置，确保 Orchestrator 不会忽略

### 4.2 规范整合

将分散在不同位置的规范整合到 SKILL.md 主文件：

| 规范内容 | 原位置 | 新位置 |
|---------|--------|--------|
| Display Layer 规范 | `references/output-style.md` | 交付清单步骤 1 |
| 发送文件附件 | `references/spawn-template.md` | 交付清单步骤 3 |
| 判断力输出 | `SKILL.md` 铁律第 6 条 | 交付清单步骤 2（细化） |
| 输出解耦 | `SKILL.md` 铁律第 4 条 | 交付清单步骤 4（重申） |

## 5. 验收标准

- [x] SKILL.md 中添加了"🔔 Ingest 交付清单"章节
- [x] 交付清单包含 4 个强制性步骤
- [x] 每个步骤都有明确的规范和示例
- [x] 提供了检查清单快速参考表
- [x] 交付流程图清晰展示执行顺序
- [x] Governance audit 审计通过

## 6. 风险评估

- **低风险**：仅添加文档规范，不涉及代码逻辑
- **影响范围**：改善用户体验，确保交付一致性
- **缓解措施**：保持向后兼容，只是明确现有要求

## 7. 相关 Issues

- #51: 本 issue
- #54: Worker Display Layer 修复（RT-021，已完成）
- #6: SKILL.md should mandate sending archived file as attachment

## 8. 预期效果

**用户端**：
- 每次收到一致的、结构化的回复
- 自动获得判断力评估，知道信息价值
- 自动收到文件附件，无需额外请求

**系统端**：
- Orchestrator 有明确的执行清单
- 减少"忘记发文件"等遗漏情况
- 提高交付质量和一致性

---
*Created by ClaudeCode (Xiao Long Xia) - 2026-04-12*
