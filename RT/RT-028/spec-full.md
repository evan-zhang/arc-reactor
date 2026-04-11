# RT-028 Spec Full: compile-report.py — 强制结构化分析引擎

## 1. 业务目标

将 verification-pipeline.md 的分析框架从「SKILL.md 引导」升级为「脚本强制执行」，确保 Source 文件的内容质量稳定可控。

## 2. 问题诊断

### 2.1 Source 内容质量依赖 Worker 自觉

Spawn Template 里的 `（你的完整 Source 内容）` 是占位符，Worker 可以填入任何内容。没有机制强制 Worker 必须填入经过 verification-pipeline.md 分析后的结果。

### 2.2 SKILL.md 的指引不具备强制力

verification-pipeline.md 写得再好，Worker 也可以选择只做浅度分析。SKILL.md 本质上是一份「给 AI 看的指令文档」，AI 可以选择遵守或变通。

### 2.3 缺乏内容质量标准

output-style.md 规定了 Display Layer 的格式，但没有规定 Source 文件的正文内容质量标准（结构、深度、最小长度等）。

## 3. 解决方案

### 3.1 核心思路：CLI 固化 > SKILL.md 引导

把「分析框架」从 SKILL.md 里移出来，写进 Python 脚本里变成强制执行的代码。

### 3.2 新增脚本：compile-report.py

- **定位**：ARC Reactor 的「分析框架强制执行器」
- **输入**：原始内容（转录文本或抓取内容）+ topic 元数据
- **过程**：强制执行多维分析（背景/原理/实现/评价/竞品/可信度）
- **输出**：符合 JSON Schema 的结构化报告
- **校验**：JSON Schema 验证，不合格则重试（最多3次）

## 4. JSON Schema 设计

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "topic",
    "summary",
    "key_findings",
    "structure",
    "credibility",
    "alternatives",
    "actionable"
  ],
  "properties": {
    "topic": {
      "type": "string",
      "description": "主题名称"
    },
    "summary": {
      "type": "string",
      "maxLength": 100,
      "description": "一句话总结（≤100字）"
    },
    "key_findings": {
      "type": "array",
      "minItems": 3,
      "items": {"type": "string"},
      "description": "关键发现（至少3条）"
    },
    "structure": {
      "type": "object",
      "required": ["background", "principle", "implementation", "evaluation"],
      "properties": {
        "background": {
          "type": "string",
          "maxLength": 300,
          "description": "背景（≤300字）"
        },
        "principle": {
          "type": "string",
          "maxLength": 500,
          "description": "原理/机制（≤500字）"
        },
        "implementation": {
          "type": "string",
          "maxLength": 800,
          "description": "实现方式（≤800字）"
        },
        "evaluation": {
          "type": "string",
          "maxLength": 500,
          "description": "优缺点评价（≤500字）"
        }
      }
    },
    "credibility": {
      "type": "object",
      "required": ["rating", "verified", "disputed", "unverified"],
      "properties": {
        "rating": {
          "type": "string",
          "enum": ["HIGH", "MEDIUM", "LOW"],
          "description": "可信度评级"
        },
        "verified": {
          "type": "array",
          "items": {"type": "string"},
          "description": "已核实的数据点"
        },
        "disputed": {
          "type": "array",
          "items": {"type": "string"},
          "description": "存疑的数据点"
        },
        "unverified": {
          "type": "array",
          "items": {"type": "string"},
          "description": "未核实的主观判断"
        }
      }
    },
    "alternatives": {
      "type": "array",
      "minItems": 1,
      "items": {"type": "string"},
      "description": "替代方案（至少1个）"
    },
    "actionable": {
      "type": "string",
      "maxLength": 60,
      "description": "可操作建议（≤60字）"
    }
  }
}
```

## 5. Prompt 设计

```
## 角色
你是一个专业的技术调研分析师。你的任务是对给定的原始内容进行深度分析，并按照规定的 JSON Schema 输出结构化报告。

## 强制要求
1. 你必须为所有字段提供内容，禁止省略任何字段
2. summary 必须 ≤100字，用一句话概括核心内容
3. key_findings 至少3条，每条要有信息增量（不是重复摘要）
4. structure 的四个子字段都必须有实质内容
5. alternatives 至少列出1个替代方案
6. actionable 必须给出可操作的建议（不是泛泛而谈）
7. 所有字数限制是硬限制，必须遵守

## 分析维度指导

### background（背景）
- 这是什么项目/技术？
- 解决了什么痛点？
- 背景是什么（谁做的？为什么做？）

### principle（原理/机制）
- 核心技术原理是什么？
- 关键机制是怎样的？
- 和传统方案有什么本质区别？

### implementation（实现方式）
- 如何落地的？
- 核心代码/架构是怎样的？
- 技术栈是什么？

### evaluation（优缺点评价）
- 优点：至少2点，要有具体数据或案例支撑
- 缺点：至少2点，要客观
- 局限性：边界在哪里？

### alternatives（替代方案）
- 同类竞品有哪些？
- 各有什么优劣？
- 为什么选这个而不是其他的？

### credibility（可信度评级）
- HIGH：数据有官方/第三方佐证
- MEDIUM：部分数据可验证，部分来自作者声称
- LOW：数据主要来自作者声称，无第三方验证

## 输出格式
你必须输出一个有效的 JSON 对象，符合上述 Schema。
不要输出任何其他内容，只输出 JSON。
```

## 6. 系统架构与修改范围

### 6.1 新增文件

- `skills/arc-reactor/scripts/compile-report.py`

### 6.2 修改文件

- `skills/arc-reactor/references/spawn-template.md` — 集成 compile-report.py 到 Ingest 流程
- `skills/arc-reactor/references/output-style.md` — Display Layer 字数弹性规则

### 6.3 RT/index.yaml 更新

新增 RT-028 条目（状态：进行中）

## 7. 验收标准

1. `python3 skills/arc-reactor/scripts/compile-report.py --help` 正常输出帮助信息
2. 给定原始文本，输出符合 JSON Schema 的结构化报告
3. 所有 required fields 必须存在，不允许省略
4. 不合格输出自动重试，最多3次
5. 改造后的 spawn template 通过 `bash verify-v42.sh` 测试
6. `python3 skills/arc-reactor/scripts/governance-audit.py` 通过

---

最后更新：2026-04-11
