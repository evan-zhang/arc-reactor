# EP-CAVEMAN-001：Caveman — AI Token 压缩技能深度解析

> **来源**: https://github.com/JuliusBrussee/caveman
> **核心受众**: AI 开发者、Claude Code/Cursor/Copilot 用户、关注 LLM 成本优化的人群
> **调研日期**: 2026-04-08

---

## 一、项目概述与核心创新点

### 1.1 什么是 Caveman

Caveman 是一款由 19 岁开发者 **Julius Brussee**（Leiden University 数据科学与 AI 专业大一学生）开源的 AI 插件/技能（skill），通过将 Claude 等大模型的输出从冗长自然语言压缩为简洁的" caveman-speak"风格，在**保持信息无损**的前提下大幅降低输出 Token 数量。

核心战绩：
- 3 天内斩获 **4.1k+ GitHub Stars**（HN 热榜）
- 真实 Claude API 测试：**22%–87% Token 节省**，平均 **65%**
- 安装方式：`npx skills add JuliusBrussee/caveman`

### 1.2 核心创新点

| 创新维度 | 具体描述 |
|---|---|
| **方法论** | 纯 Prompt Engineering，非模型微调，无需访问模型权重 |
| **无损压缩** | 保留所有技术内容（代码块、URL、路径、命令、表格、标题、版本号），仅压缩自然语言冗余 |
| **分级控制** | Lite / Full / Ultra 三档压缩强度，用户可控制简洁度 |
| **双向压缩** | Caveman（输出压缩）+ Caveman Compress（输入/记忆文件压缩） |
| **无配置负担** | 无需配置项，开箱即用，触发词自动激活 |

### 1.3 背景故事

项目起源于 Julius Brussee 用 **10 分钟写的"玩笑代码"**。他在学习过程中注意到：大模型的回复往往过于冗长（"当然，我很乐意帮助你..."），浪费大量 Token。于是他写了一个简单的 prompt 约束，结果意外走红。

背后有论文支撑：2026 年论文 *"Brevity Constraints Reverse Performance Hierarchies in Language Models"* 证明，简洁性约束可以提升大模型准确率 **26 个百分点**，并在数学/科学基准测试中逆转模型大小层级关系。

---

## 二、技术架构与实现原理

### 2.1 核心原理：Prompt-Based Behavioral Modification

Caveman **不依赖正则替换或 Token 级别操作**，而是作为一段**精心设计的系统提示**注入对话。当用户触发 caveman 模式，Claude 被指示以"原始人说话方式"回应：

> 移除冠词（the, a）、礼貌用语、犹豫词、冗余铺垫；
> 保留技术术语、代码块、URL、文件路径、命令、标题结构、表格、日期、版本号。

示例对比：
```
# 普通回复（69 tokens）
"Sure! Let me help you fix that React re-render issue. The problem is likely 
caused by creating a new object reference on every render. Here's what I'd do..."

# Caveman 模式（19 tokens）
"React re-render issue. Create new object ref each render. Fix:"
```

### 2.2 压缩模式详解

#### Lite 模式（轻度）
- 移除填充词、犹豫表达
- 保持完整句子和专业书面风格
- 适合需要一定正式感的场景

#### Full 模式（标准）— 默认模式
- 省略部分功能词（连词、介词）
- 允许断句和碎片化表达
- 典型" caveman style"，平衡可读性与压缩率

#### Ultra 模式（极致压缩）
- 激进缩写：DB、auth、config、req、res、fn、impl
- 移除所有连词，用箭头表达因果：`X → Y`
- 优先使用单词而非短语
- 最大 Token 节省，牺牲部分可读性

### 2.3 Caveman Compress（配套输入压缩工具）

独立 companion 工具，用于压缩用户侧的**记忆文件**（如 CLAUDE.md），节省输入 Token 约 **45%**：

| 文件类型 | 原始 Tokens | 压缩后 Tokens | 节省率 |
|---|---|---|---|
| claude-md-preferences.md | 706 | 285 | 59.6% |
| project-notes.md | 1,145 | 535 | 53.3% |
| claude-md-project.md | 1,122 | 687 | 38.8% |
| todo-list.md | 627 | 388 | 38.1% |
| mixed-with-code.md | 888 | 574 | 35.4% |
| **平均** | **898** | **494** | **~45%** |

注意：原始文件仍保持人类可读，压缩版专供 AI 读取。

### 2.4 触发方式

Caveman 通过语义触发词激活，无需手动切换：
- `"caveman mode"`
- `"/caveman"`
- `"talk like caveman"`
- `"use caveman"`
- `"less tokens"`
- `"be brief"`

---

## 三、Benchmark 数据分析

### 3.1 输出 Token 节省（Caveman 核心数据）

| 任务类型 | 原始 Tokens | Caveman Tokens | 节省率 |
|---|---|---|---|
| Docker multi-stage build | 1,042 | 290 | **72%** |
| PostgreSQL race condition 调试 | 1,200 | 232 | **81%** |
| React Error Boundary 实现 | 3,454 | 456 | **87%** |
| React re-render explanation | 1,180 | 159 | **87%** |
| 其他混合任务 | — | — | 22%–87% |
| **平均值** | **~1,214** | **~294** | **~65%** |

### 3.2 重要注意事项

⚠️ **Caveman 仅压缩输出 Token（output tokens）**
- 模型的内部推理/思考 Token（thinking/reasoning tokens）**不受影响**
- 技能本身加载也消耗少量 Token
- 因此端到端总成本节省**略低于**输出 Token 节省率

⚠️ **"87% 节省"是极端案例**
- README 突出展示的 87% 来自特定任务（React Error Boundary）
- 真实平均节省约 **65%**，范围 **22%–87%**

### 3.3 Caveman Compress Benchmark

配套工具 Caveman Compress 测试 5 个真实记忆文件：
- 平均输入 Token 节省：**~45%**
- 范围：35.4%（含大量代码的混合文件）到 59.6%（纯偏好设置文件）

---

## 四、适用场景与局限性

### 4.1 最佳适用场景

| 场景 | 推荐模式 | 预期效果 |
|---|---|---|
| 日常代码调试 / bug 修复 | Full | 节省 65–80% 输出 tokens |
| 需要快速迭代的高频 API 调用 | Ultra | 极致压缩，速度优先 |
| 文档生成 / PR 描述 | Lite | 保持专业可读性 |
| 长对话链（多轮调试） | Full + Compress | 输入输出双向压缩 |
| 资源受限 / 成本敏感场景 | Full | 平衡节省与可读性 |

### 4.2 局限性

| 局限类型 | 具体说明 |
|---|---|
| **推理 Token 不变** | Caveman 只压缩输出，无法减少模型思考过程的 Token 消耗 |
| **技能加载开销** | 每次会话加载技能本身消耗少量 Token |
| **Ultra 模式可读性差** | 极度缩写可能导致人类审查困难 |
| **不适合创意写作** | 小说、散文等创意内容会被严重破坏 |
| **不适合复杂解释** | 需要详细推理过程的技术分析，压缩后可能丢失上下文线索 |
| **无配置项** | 纯开关设计，无法微调压缩行为 |

---

## 五、竞品对比

### 5.1 同类 Token 压缩方案概览

| 方案 | 类型 | 压缩方式 | 节省率 | 特点 |
|---|---|---|---|---|
| **Caveman** | Prompt Engineering | 系统提示约束 | 22–87%（输出） | 开源、无损、三档可调 |
| **caveman-distillate** | 模型蒸馏 | 微调蒸馏 | 较高 | 基于 Caveman 理念的蒸馏模型 |
| **Shortened LLM Outputs** | 后处理 | 文本后处理规则 | 中等 | 规则驱动，依赖后处理 |
| **Claude 原生压缩** | API 层 | API 参数 | 视情况 | 官方支持，但控制粒度粗 |

### 5.2 Caveman 的差异化优势

1. **零门槛集成**：`npx skills add` 一行安装，无需修改代码
2. **信息无损保证**：技术内容（代码/URL/路径）完全不改动
3. **分级控制**：Lite/Full/Ultra 覆盖不同用户偏好
4. **双向压缩**：输出压缩 + 输入压缩组合使用
5. **技能生态兼容**：Cursor、Copilot、Windsurf、Claude Code 通用

### 5.3 潜在竞品动态

- `wilpel/caveman-compression`：探索类似语义压缩用于 context 优化
- `dlepold/caveman-distillate`：基于 Caveman 思想的蒸馏模型尝试

---

## 六、安装与使用指南

### 6.1 安装命令

```bash
# 通用安装（Skills 兼容环境）
npx skills add JuliusBrussee/caveman

# Cursor
npx skills add JuliusBrussee/caveman -a cursor

# Copilot
npx skills add JuliusBrussee/caveman -a copilot

# Windsurf
npx skills add JuliusBrussee/caveman -a windsurf

# Claude Code（插件方式）
claude plugin marketplace add JuliusBrussee/caveman
claude plugin install caveman@caveman
```

### 6.2 快速使用

1. 安装完成后，在对话中直接说：
   ```
   Use caveman mode for this task
   ```
2. Claude 将自动切换至压缩输出模式
3. 可通过以下方式切换模式：
   - `/caveman` — Full 模式
   - `caveman ultra` — Ultra 模式
   - `caveman lite` — Lite 模式

### 6.3 配合 Caveman Compress 使用

```bash
# 安装配套工具
npx skills add JuliusBrussee/caveman-compress

# 压缩你的 CLAUDE.md 或其他记忆文件
caveman-compress compress ./CLAUDE.md
```

---

## 七、关键发现与行动建议

| 关键发现 | 建议操作 | 优先级 |
|---|---|---|
| Caveman 可节省 65% 输出 Token，无损保留技术内容 | 在高频代码调试流程中启用 Full 模式 | 🔴 高 |
| 技能加载有少量开销，适合长对话而非单次查询 | 避免对短查询（<5 分钟）单独开启 | 🟡 中 |
| Caveman Compress 可压缩记忆文件 45%，适合长程项目 | 将项目 CLAUDE.md 预压缩后使用 | 🔴 高 |
| Ultra 模式压缩率最高但可读性差 | 仅用于内部自动化流程，不用于需要 Review 的输出 | 🟡 中 |
| 推理 Token 不受影响，无法降低模型计算成本 | 结合模型选择策略（如小模型处理简单任务） | 🟡 中 |
| Caveman 是 Prompt Engineering 思路，零成本实验 | 先用 Lite 模式测试，接受度高的场景升级 Full | 🟢 低 |

---

## 八、参考链接

| 资源 | 链接 |
|---|---|
| GitHub 主仓库 | https://github.com/JuliusBrussee/caveman |
| SkillsLLM 技能页面 | https://skillsllm.com/skill/caveman |
| Hacker News 讨论 | https://news.ycombinator.com/item?id=47647455 |
| QbitAI 中文报道 | https://www.qbitai.com/2026/04/397733.html |
| Caveman Compress | https://github.com/wilpel/caveman-compression |
| caveman-distillate | https://github.com/dlepold/caveman-distillate |

---

*生成于 ARC Reactor v2.3 | 源码与配置深度内化档案*
*EP-CAVEMAN-001 | 2026-04-08*
