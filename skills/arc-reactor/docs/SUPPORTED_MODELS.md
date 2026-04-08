# 当前支持的大模型

> 统计时间: 2026-02-21
> 总计: 20 个模型

---

## 📊 模型分类

### 🚀 OpenAI Codex (1个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `openai-codex/gpt-5.2-codex` | - | 最强代码和推理模型 |

---

### 🧠 Google (8个)

#### Google Antigravity 系列 (7个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `google-antigravity/claude-opus-4-6-thinking` | - | Opus 4.6 Thinking（默认主模型）|
| `google-antigravity/gemini-3-pro-low` | - | Gemini 3 Pro Low |
| `google-antigravity/gemini-3-pro-high` | - | Gemini 3 Pro High |
| `google-antigravity/gemini-3-flash` | - | Gemini 3 Flash |
| `google-antigravity/claude-sonnet-4-5-thinking` | - | Sonnet 4.5 Thinking |
| `google-antigravity/claude-sonnet-4-5` | - | Sonnet 4.5 |
| `google-antigravity/claude-opus-4-5-thinking` | - | Opus 4.5 Thinking |

#### Google 官方 Gemini (1个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `google/gemini-3-pro-preview` | - | Gemini 3 Pro Preview |
| `google/gemini-3-flash-preview` | - | Gemini 3 Flash Preview |

**备注**: 还有 `google/gemini-3-flash` 和 `google/gemini-3-pro` 等模型，配置的 Gemini 3 系列模型

---

### 🤖 Zai GLM (2个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `zai/glm-4.7` | GLM | GLM-4.7（常用，平衡性能）|
| `zai/glm-5` | - | GLM-5（最新版）|

---

### 🧪 MiniMax (2个)

| 模型 ID | 别名 | Context Window | Max Tokens |
|---------|------|---------------|------------|
| `minimax-portal/MiniMax-M2.1` | minimax-m2.1 | 200,000 | 128,000 |
| `minimax-portal/MiniMax-M2.5` | minimax-m2.5 | 200,000 | 128,000 (Reasoning) |

---

### 🤖 Anthropic Claude (2个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `anthropic/claude-opus-4-6` | - | Claude Opus 4.6 |
| `anthropic/claude-sonnet-4-6` | - | Claude Sonnet 4.6 |

---

### 🌙 Amazon Bedrock (3个)

| 模型 ID | 别名 | 说明 |
|---------|------|------|
| `amazon-bedrock/anthropic.claude-opus-4-6-v1` | - | Claude Opus 4.6 (Bedrock)|
| `amazon-bedrock/global.anthropic.claude-opus-4-6-v1` | - | Claude Opus 4.6 (Global)|
| `amazon-bedrock/moonshotai.kimi-k2.5` | - | Moonshot Kimi K2.5 |

---

## 🎯 按用途分类

### 💻 代码和复杂推理（最强）
- `openai-codex/gpt-5.2-codex` - OpenAI Codex
- `google-antigravity/claude-opus-4-6-thinking` - Opus Thinking（默认主模型）

### ⚡ 快速生成
- `google-antigravity/gemini-3-flash` - Gemini 3 Flash
- `google/gemini-3-flash-preview` - Gemini 3 Flash Preview
- `zai/glm-4.7` - GLM-4.7（常用，平衡）

### 🧠 推理和分析
- `google-antigravity/gemini-3-pro-high` - Gemini 3 Pro High
- `google-antigravity/claude-sonnet-4-5-thinking` - Sonnet Thinking
- `google-antigravity/claude-opus-4-5-thinking` - Opus Thinking
- `minimax-portal/MiniMax-M2.5` - MiniMax M2.5 (Reasoning)

### 💬 对话和通用
- `zai/glm-4.7` - GLM-4.7
- `zai/glm-5` - GLM-5
- `anthropic/claude-sonnet-4-6` - Claude Sonnet 4.6
- `google-antigravity/claude-sonnet-4-5` - Sonnet 4.5

### 🎨 长文本生成
- `minimax-portal/MiniMax-M2.1` - MiniMax M2.1 (128K tokens)
- `minimax-portal/MiniMax-M2.5` - MiniMax M2.5 (128K tokens)
- `zai/glm-5` - GLM-5（推测支持长文本）

---

## 🔧 Agent 模型分配

### Code-Agent
- **主模型**: `zai/glm-4.7`
- **降级**: `openai-codex/gpt-5.2-codex`

### Docs-Agent
- **主模型**: `zai/glm-4.7`
- **降级**: `openai-codex/gpt-5.2-codex`

### AI-News
- **主模型**: `zai/glm-4.7`
- **降级**: `openai-codex/gpt-5.2-codex`

### Stock-Agent
- **主模型**: `zai/glm-4.7`
- **降级**: `zai/glm-4.7` (无降级）

### Trade-Agent
- **主模型**: `openai-codex/gpt-5.2-codex`
- **降级**: `zai/glm-4.7`

### Ops-Agent
- **主模型**: `zai/glm-4.7`
- **降级**: (无降级)

### Assistant-Agent (Nova)
- **主模型**: `google-antigravity/claude-opus-4-6-thinking`
- **降级**: 18 个模型的完整降级链

---

## 📊 模型统计

| 提供商 | 模型数 | 最强模型 | 推荐用途 |
|--------|--------|----------|----------|
| OpenAI Codex | 1 | gpt-5.2-codex | 代码、复杂推理 |
| Google | 8 | claude-opus-4-6-thinking | 多用途（默认主模型）|
| Zai GLM | 2 | GLM-5 | 中文、对话 |
| MiniMax | 2 | MiniMax-M2.5 | 长文本、快速生成 |
| Anthropic | 2 | claude-opus-4-6 | 对话、推理 |
| Amazon Bedrock | 3 | claude-opus-4-6-v1 | 企业级 |
| **总计** | **18** | - | - |

---

## ⚙️ 特殊配置

### MiniMax 模型
- **Context Window**: 200,000 tokens
- **Max Tokens**: 128,000 tokens (已提高)
- **Reasoning**: MiniMax-M2.5 支持

### 默认配置
- **默认主模型**: `google-antigravity/claude-opus-4-6-thinking`
- **降级链**: 18 个模型按优先级排列
- **Thinking 默认**: low

---

## 📝 备注

1. **Google Antigravity**: 系列模型通过 Google Antigravity 平台提供
2. **MiniMax**: M2.1 和 M2.5 的 maxTokens 已从 8192 提高到 128000
3. **Gemini 3**: Google 官方的 Gemini 3 Pro/Flash Preview 模型
4. **降级机制**: 系统支持自动降级到下一个可用模型
5. **模型容灾**: 已实现智能容灾降级系统

---

*最后更新: 2026-02-21*
*模型总数: 20 个（18 个在默认降级链中）*
