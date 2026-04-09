# Issue: ARC Reactor 工作流在实际使用中的问题汇总

## 概述

在连续两次使用 ARC Reactor 处理 YouTube 视频摄入时，遇到了工作流层面的问题。这些问题不是依赖兼容性（已有 #40），而是 **ARC 规范本身在实际执行中的模糊地带和缺失环节**。

---

## 问题列表

### 问题 1 [P0]: Display Layer 与"附件必达"规则存在矛盾

**现象:**
- SKILL.md 要求 Display Layer（≤200字）发给用户，同时要求"附件必达"把编译报告发给用户
- 实际执行时，两者只发其一的情况很常见（Agent 只发了聊天文字结论，没发文件附件）
- 没有明确优先级：Display Layer 是给用户的主要输出，还是补充说明？

**建议:**
- 明确 Display Layer 的定位：它是"结论摘要 + 文件附件"的组合，还是独立的？
- 如果要求两者都发，应明确为"结论先行，附件紧随"
- 建议增加 `send_to_user: both` 选项，明确告知 Agent 两者都要发送

---

### 问题 2 [P0]: Injection 工作流从未被执行

**现象:**
- SKILL.md 定义了 Injection 工作流，要求每次回答用户前静默运行 `context-injector.py --query "[用户提问]"`
- 连续两次使用中，Injection 工作流完全未被执行
- Agent 没有主动检查知识库中与用户问题相关的实体

**根因分析:**
- SKILL.md 对 Injection 的描述是"触发：Orchestrator 在处理任何用户提问前静默执行"，但 Orchestrator（也就是 Agent 自己）并不知道要这样做
- 没有显式的触发条件说明，Agent 容易忽略这个步骤
- 建议将 Injection 改为 Agent 每次响应用户前的**显式检查步骤**，而非"静默执行"

---

### 问题 3 [P1]: 长任务（Whisper 转写）无进度反馈

**现象:**
- 29分钟视频转写耗时 7+ 分钟（模型已缓存），期间没有任何进度反馈
- 用户看到的是"正在转写..."然后长时间无响应，容易误以为任务卡住
- 当前 workaround 是用 nohup 后台运行，但后台运行后 Agent 也无法感知进度

**建议:**
- 增加进度回调机制：脚本定期输出进度（如每 30 秒打印百分比）
- 或者提供 `--watch` 选项，实时 tail 进度
- 或者分离"下载音频"和"转写"两个独立步骤，让 Agent 可以在下载完成后、开始转写前向用户报告进度

---

### 问题 4 [P1]: 文件发送时机不明确

**现象:**
- 两次视频处理都是：结论文字先发 → 用户问"怎么没发文件" → 补发文件
- 用户体验断裂：先看到一堆文字结论，后面才来文件

**根因:**
- SKILL.md 没有规定文件附件的发送时机
- "附件必达"规则只说了要发，但没说先发还是后发

**建议:**
- 明确规定：Source 编译报告文件应**先于或同步于** Display Layer 文字发送
- Display Layer 可以是文件发送后的简短摘要，不应替代文件本身

---

### 问题 5 [P2]: 4连击流程中 index 更新时机滞后

**现象:**
- 两次摄入都是先存 source，结论文字已经发给用户了，entity 和 index 还在"待更新"状态
- 用户如果问"这个视频讲了什么"，Agent 还没读完 index，给出的回答可能不完整

**建议:**
- 明确规定：4连击必须在 Display Layer 输出**之前**全部完成
- 即：source → entity → index → log → Display Layer → 发给用户

---

## 建议的优先级排序

| 优先级 | 问题 | 建议 |
|--------|------|------|
| P0 | Injection 工作流被忽略 | 改为显式检查步骤，而非静默执行 |
| P0 | Display Layer 与附件矛盾 | 明确两者关系，规定发送顺序 |
| P1 | Whisper 无进度反馈 | 增加进度回调或分离步骤 |
| P1 | 文件发送时机不明确 | 规定文件先于文字发送 |
| P2 | index 更新滞后 | 规定4连击在 Display Layer 前完成 |

---

## 相关文件

- `skills/arc-reactor/SKILL.md`（特别是 Injection 工作流和 Display Layer 部分）
- `RT/RT-002/spec-lite.md`（ARC 规范原始设计）
- `RT/RT-ISSUE-media-extractor-problems.md`（#40，依赖兼容性问题）

---

*Issue 由 OpenClaw Agent 在连续两次使用 ARC Reactor 时创建*
