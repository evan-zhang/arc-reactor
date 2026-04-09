# ARC Reactor v4.2.0: 全流程手动验收测试 (Master Test Suite)

本手册专为 **用户执行** 联调而设计。请按照以下步骤一个一个发给您的 Agent，并核对输出。

---

## 阶段一：数据摄入 (Ingest & 4-Combo)

### 测试目标
验证系统能否从外部信息（网页/视频）中提取知识，并完美执行“四连击”落盘，绝不产生路径幻觉。

### 1. 提交摄入命令
**向 Agent 发送指令：**
> “请帮我深入研究并 Ingest 这篇文章：`https://karpathy.github.io/2024/01/03/chatgpt-is-blazing/`。
> 要求：严格执行 Ingest 4连击逻辑（Source, Entity, Index, Log）。完成后告诉我生成的实体名和日期目录。”

### 2. 人工校验（物理检查）
当 Agent 报告完成后，请您在本地终端输入以下命令查看成果：
```bash
# 检查日期目录是否生成 (假设您的库根目录名为 arc-reactor-doc)
ls skills/arc-reactor/arc-reactor-doc/wiki/sources/$(date +%Y-%m-%d)
# 检查实体卡片是否生成
ls skills/arc-reactor/arc-reactor-doc/wiki/entities/
# 检查索引是否记录
cat skills/arc-reactor/arc-reactor-doc/wiki/index.md
```
**[判定准则]**：必须看到 `sources` 下有对应的 `.md` 文件，且内容包含 YAML Frontmatter。

---

## 阶段二：潜意识唤醒 (Subconscious Injection)

### 测试目标
验证 Agent 在没有任何提示的情况下，是否能由于“肌肉记忆”自动联想到刚才存入的知识。

### 1. 提交触发命令
**向 Agent 发送指令（确保是一个全新的对话或清除上下文）：**
> “帮我总结一下 Andrej Karpathy 对 ChatGPT 运行成本的看法。”

### 2. 人工校验（逻辑检查）
**[判定准则]**：
- 观察 Agent 的响应。如果它在回答前输出了类似 `<ARC_KNOWLEDGE_CONTEXT>` 的块，说明 **Injection 探针生效**了。
- 观察内容：它应当提到了刚才那篇文章里的具体观点（比如 $700,000/day 的成本），而不是在网上现搜。

---

## 阶段三：跨维周报 (Weekly Brief)

### 测试目标
验证系统能否将不同时间的知识点进行横向切片，并生成洞察。

### 1. 提交周报命令
**向 Agent 发送指令：**
> “生成一份本周的知识周报。”

### 2. 人工校验（聚合检查）
**[判定准则]**：
- Agent 应当输出一份 Markdown 报表。
- 报表中必须包含您刚刚存入的那个主题。
- 报表末尾应当有关于“本周知识集群”的 AI 洞察分析。

---

## 阶段四：极端情况测试 (Robustness)

### 1. 重复存入 (De-dup)
**向 Agent 发送指令：**
> “再次 Ingest 刚才那篇文章。”
**[判定准则]**：Agent 脚本应当返回 `merged` 或 `skipped` 状态，而不是产生两个重名的 `chatgpt-is-blazing-1.md` 文件。

---

## 🎯 验收结论
如果您以上四步都跑通了，说明您的 **ARC Reactor v4.2.0** 已经完全具备了**私人知识编译器**的实战能力！
