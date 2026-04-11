# RT-021: Worker Display Layer Fix (Issue #54)

## 1. 简介 (Introduction)

修复 Worker 子代理将 JSON 回执直接暴露给用户的问题，确保遵守 SKILL.md 铁律第4条：输出解耦 (Two-Tier Output)。

## 2. 问题描述

**违反规则**：Worker 完成任务后，将内部 JSON 回执（含 `status`、`path`、`size_bytes` 等字段）直接作为用户消息发送到 Telegram 群聊，暴露了内部实现细节。

**预期行为**：Worker 应按照 `references/output-style.md` 的 Display Layer 规范输出中文摘要（≤200字），而不是暴露内部技术细节。

## 3. 根因分析

**直接原因**：
- `references/spawn-template.md` Template 1 的"最终交付"部分要求："汇报所有 4 次 JSON 回执"
- 这条指令与 SKILL.md 铁律第4条直接矛盾

**根本原因**：
- 模板没有明确要求 Worker 将回执转换为 Display Layer 格式
- 铁律写在 SKILL.md 主文件里，但 Worker spawn 时拿到的模板指令没有内联这个约束

## 4. 解决方案

### 4.1 修复 spawn-template.md

**修改前（第60-64行）**：
```markdown
### 最终交付
4 连击全部完成后：
1. 汇报所有 4 次 JSON 回执
2. 通过 message tool (channel=telegram, target={USER_ID}) 将 source 文件作为附件发送给用户
```

**修改后**：
```markdown
### 最终交付
4 连击全部完成后：
1. **按 Display Layer 规范输出**（见 `references/output-style.md`）：
   - 中文摘要，≤200字
   - 结论先行，用「·」列出要点
   - 自然对话风格，避免技术细节
2. **禁止向用户展示**：JSON 回执、status、path、size_bytes 等内部字段
3. **发送附件**：通过 message tool (channel=telegram, target={USER_ID}) 将 source 文件发送给用户

**Display Layer 示例**：
```
已完成 {TOPIC_TITLE} 的知识编译。

核心结论：
· 提取了 {主要实体1}、{主要实体2} 的关键信息
· 建立了 {数量} 个知识节点链接
· 已存入 Wiki 供后续查询使用
```
```

### 4.2 增强模板约束

在模板开头添加硬性提醒：

```markdown
⚠️ MANDATORY: Use `cat << 'EOF' | python3 skills/arc-reactor/scripts/archive-manager.py --type [TYPE] --topic [NAME] --stdin` for ALL outputs. Execute 4-combo (source, entity, index, log) for Ingest! Do not write flat files. You MUST verify JSON receipt contains "status": "success" after each operation. Run all commands from workspace root: {WORKSPACE_ROOT}

⚠️ OUTPUT CONSTRAINT: All user-facing output MUST follow Display Layer规范 (≤200字中文摘要)，禁止暴露JSON回执、status、path、size_bytes等内部字段。详见 `references/output-style.md`。
```

## 5. Display Layer 规范速查

| 属性 | 要求 | 示例 |
|------|------|------|
| **字数** | ≤200字 | 一段简短总结 |
| **风格** | 模拟人类对话 | 自然、口语化 |
| **结构** | 结论先行 | 先说结果，再列要点 |
| **格式** | 「·」列表 | 不要用表格 |
| **禁止** | 技术细节 | 不提JSON、路径、大小 |

**正确示例**：
```
已完成 Hermes Agent 的知识编译。

核心结论：
· 提取了架构设计、性能数据的关键信息
· 建立了与 OpenClaw 的知识关联
· 已存入 Wiki 供后续查询使用
```

**错误示例**：
```
✅ 完成 Ingest 4 连击：
1. {"status": "success", "path": "arc-reactor-doc/wiki/sources/...", "size_bytes": 3394}
2. {"status": "success", "path": "arc-reactor-doc/wiki/entities/...", "size_bytes": 1250}
...
```

## 6. 验收标准

- [x] spawn-template.md 中"最终交付"部分已修复
- [x] 模板开头添加了输出约束提醒
- [x] 修复后的模板要求遵守 Display Layer 规范
- [x] 明确禁止暴露 JSON 回执等内部字段
- [x] 提供了正确的 Display Layer 输出示例
- [x] Governance audit 审计通过

## 7. 风险评估

- **低风险**：仅修改模板文本，不涉及代码逻辑
- **影响范围**：改善用户体验，符合铁律要求
- **缓解措施**：保持向后兼容，只是改变输出格式

## 8. 相关 Issues

- #54: 本 issue
- #51: Ingest 完成后的交付动作缺少强制性检查清单（后续处理）

---
*Created by ClaudeCode (Xiao Long Xia) - 2026-04-12*
