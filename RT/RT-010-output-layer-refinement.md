# RT-010: Output Layer Refinement & UX Improvements

## 1. 简介 (Introduction)
为了提升 ARC Reactor 的用户交互体验，本项目旨在优化输出层（Output Layer）的逻辑。核心理念是将系统内部的长链条操作（Archive Layer）与用户可见的精简总结（Display Layer）进行解耦，并引入具有“灵魂”的判断逻辑。

## 2. 核心架构：输出分层 (Two-Tier Output)

### 2.1 Display Layer (展示层)
- **目标**：为用户提供第一直觉的洞察。
- **规范**：
    - 长度控制在 200 字左右。
    - 语气模拟人类对话（像是在群聊中汇报）。
    - 结论先行，关键信息以 `·` 列表展示。
    - **必须包含判断 (Judgement)**：
        - **重要性/优先级**：明确标出该信息对用户的价值。
        - **行动建议**：下一步建议用户做什么。
        - **可信度**：根据来源评估信息的真实性。
- **示例**：
    > 刚才帮你看了这篇关于 Claude Code 的文章，非常值得关注。
    > 核心结论：
    > · 性能大幅提升：在推理任务上比上一代快 30%。
    > · 价格持平：虽然能力强了，但 Token 成本没变。
    > 
    > **我的判断**：这是一个高价值的信息。建议你立刻在下一个项目里试用一下。可信度高（来自官方声明）。
    > (详情已归档至 wiki/sources)

### 2.2 Archive Layer (分层日志)
- **目标**：保证知识的永续累积和可追溯性。
- **操作**：继续执行“Ingest 4 连击”（Source, Entity, Index, Log）。
- **展示方式**：这些操作的回执（JSON）应当尽量精简或放在回复的末尾，不干扰 Display Layer 的阅读。

## 3. 交互优化 (UX Improvements)

### 3.1 自然语言触发 (Natural Triggers)
不再强求用户输入复杂的 `archive-manager.py` 命令。Agent 应能识别以下自然触发词：
- "帮我摄入"、"看下这个"、"帮我存一下" -> 执行 Ingest 4 连击。
- "总结一下"、"之前关于...怎么说的" -> 执行 Query 流程。

### 3.2 渠道自适应 (Channel Adaptation)
- **Discord/Telegram**：避免使用 Markdown 表格，分段要极短，关键点放最前面。
- **Browser/Desktop**：允许更丰富的排版。

## 4. 验收标准 (Acceptance Criteria)
- [ ] Agent 输出符合 Display Layer 的字数和风格要求。
- [ ] 每一条摄入成功的回复都包含 **Judgement (判断)** 部分。
- [ ] Ingest 过程中的回执信息对用户透明，不再展示冗长的 JSON 片段（除非任务失败）。
- [ ] 能识别自然语言链接并自动进行 4 连击归档。
