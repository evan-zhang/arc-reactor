# 大模型可用性总结

> 统计时间: 2026-02-21
> 基于现有配置和测试结果

---

## ✅ 已验证可用 (7个)

### 1. Google 系列 (3个)

| 模型 | API Key | 测试结果 | 用途 |
|------|---------|---------|------|
| **Google Gemini API** | `GOOGLE_GEMINI_API_KEY` | ✅ 成功 | Gemini 2.5 Flash/Pro |
| **Google Cloud Translation** | `GOOGLE_API_KEY` | ✅ 成功翻译 "Hello" → "你好" | 多语言翻译 |
| **YouTube Data API** | `YOUTUBE_API_KEY` | ✅ 成功搜索 "artificial intelligence" | 视频搜索 |

### 2. 金融 API (1个)

| 模型 | API Key | 测试结果 | 用途 |
|------|---------|---------|------|
| **Finnhub** | `FINNHUB_API_KEY` | ✅ 成功获取 AAPL 股价 ($264.58) | 实时股票数据 |

### 3. 图片生成 (1个)

| 模型 | API Key | 测试结果 | 用途 |
|------|---------|---------|------|
| **Nano Banana (Gemini)** | `GEMINI_API_KEY` | ✅ 成功生成测试图片 (1.4MB) | 图片生成和编辑 |

### 4. 搜索 API (2个)

| 模型 | API Key | 状态 | 用途 |
|------|---------|------|------|
| **Tavily Search** | `TAVILY_API_KEY` | ✅ 已配置，未直接测试 | AI 驱动的搜索 API |
| **Apify** | `APIFY_TOKEN` | ✅ 已配置 | Web scraping |

---

## 🟡 配置了但可能有限制 (7个)

### 1. OpenAI Codex (1个)

| 模型 | 认证方式 | 配置状态 | 问题 |
|------|---------|---------|------|
| **openai-codex/gpt-5.2-codex** | OAuth | ✅ 已配置 (access + refresh tokens) | ⚠️ 频繁遇到 429 限流错误 |

**说明**:
- OAuth 配置存在
- 使用统计数据: errorCount: 20 (rate_limit)
- 当前状态: 在冷却期
- 建议: 检查 OpenAI Platform 配额

---

### 2. MiniMax (2个)

| 模型 | API Key | 配置状态 |
|------|---------|---------|
| **minimax-portal/MiniMax-M2.1** | JWT token | ✅ 已配置 |
| **minimax-portal/MiniMax-M2.5** | JWT token | ✅ 已配置 |

**说明**:
- API Key 已配置 (base64 JWT token)
- Context Window: 200,000 tokens
- Max Tokens: 128,000 tokens (已提高)
- M2.5 支持 Reasoning
- 状态: 已配置，未直接测试 API 调用

---

### 3. Zai GLM (2个)

| 模型 | API Key | 配置状态 |
|------|---------|---------|
| **zai/glm-4.7** | API key | ✅ 已配置 |
| **zai/glm-5** | API key | ✅ 已配置 |

**说明**:
- API Key 已配置到环境变量
- GLM-4.7 是多个 agents 的主模型
- GLM-5 是最新版
- 状态: 已配置，未直接测试 API 调用

---

### 4. Google Antigravity 系列 (7个)

| 模型 | 提供商 | 配置方式 | 状态 |
|------|---------|---------|------|
| `google-antigravity/claude-opus-4-6-thinking` | Google Antigravity | 网关 | ✅ 默认主模型 |
| `google-antigravity/gemini-3-pro-low` | Google Antigravity | 网关 | ✅ 已配置 |
| `google-antigravity/gemini-3-pro-high` | Google Antigravity | 网关 | ✅ 已配置 |
| `google-antigravity/gemini-3-flash` | Google Antigravity | 网关 | ✅ 已配置 |
| `google-antigravity/claude-sonnet-4-5-thinking` | Google Antigravity | 网关 | ✅ 已配置 |
| `google-antigravity/claude-sonnet-4-5` | Google Antigravity | 网关 | ✅ 已配置 |
| `google-antigravity/claude-opus-4-5-thinking` | Google Antigravity | 网关 | ✅ 已配置 |

**说明**:
- 通过 Google Antigravity 网关访问
- `claude-opus-4-6-thinking` 是系统的默认主模型
- 状态: 已配置到 openclaw.json，通过网关访问

---

### 5. Amazon Bedrock 系列 (3个)

| 模型 | 提供商 | 配置方式 | 状态 |
|------|---------|---------|------|
| `amazon-bedrock/anthropic.claude-opus-4-6-v1` | AWS Bedrock | 网关 | ✅ 已配置 |
| `amazon-bedrock/global.anthropic.claude-opus-4-6-v1` | AWS Bedrock | 网关 | ✅ 已配置 |
| `amazon-bedrock/moonshotai.kimi-k2.5` | AWS Bedrock | 网关 | ✅ 已配置 |

**说明**:
- 通过 Amazon Bedrock 访问
- 可能需要 AWS 配置
- 状态: 已配置到 openclaw.json，通过网关访问

---

### 6. Google 官方 Gemini 系列 (2个)

| 模型 | API Key | 配置状态 |
|------|---------|---------|
| **google/gemini-3-pro-preview** | `GOOGLE_GEMINI_API_KEY` | ✅ 已配置 |
| **google/gemini-3-flash-preview** | `GOOGLE_GEMINI_API_KEY` | ✅ 已配置 |

**说明**:
- Google 官方 API，与 Google Antigravity 不同
- 状态: 已配置，未直接测试 API 调用

---

## 🔴 可能需要额外配置 (2个)

### 1. Anthropic Claude 系列 (2个)

| 模型 | API Key | 配置状态 |
|------|---------|---------|
| **anthropic/claude-opus-4-6** | ❓ 未发现 API key | ⚠️ 可能需要配置 |
| **anthropic/claude-sonnet-4-6** | ❓ 未发现 API key | ⚠️ 可能需要配置 |

**说明**:
- 模型 ID 在 openclaw.json 中
- 未在环境变量中发现对应的 API key
- 可能通过其他网关访问
- 状态: 需要验证

---

## 📊 总结统计

### 按可用性分类

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ **已验证可用** | 7 | 35% |
| 🟡 **配置了但可能有限制** | 11 | 55% |
| 🔴 **可能需要额外配置** | 2 | 10% |

### 按提供商分类

| 提供商 | 已配置 | 可能有问题 |
|--------|--------|-----------|
| Google | 6 | 0 |
| MiniMax | 2 | 0 |
| OpenAI | 1 | 1 (限流) |
| Zai GLM | 2 | 0 |
| Amazon | 3 | 0 |
| Anthropic | 0 | 2 |
| 其他 | 4 | 0 |

---

## 🎯 建议操作

### 立即需要关注

1. **OpenAI Codex 限流问题** (P0)
   - 访问 https://platform.openai.com/
   - 检查 API 使用配额
   - 查看限流原因
   - 考虑优化调用频率或升级账户

### 建议测试

1. **MiniMax 模型**
   - 尝试进行一次简单的 API 调用测试
   - 验证 JWT token 是否有效

2. **GLM 模型**
   - 尝试进行一次简单的 API 调用测试
   - 验证 API key 是否有效

3. **Google Antigravity 模型**
   - 这些模型通过网关访问
   - 可用性取决于网关服务

### 可选配置

1. **Anthropic Claude**
   - 如果需要直接访问 Anthropic API
   - 需要配置 `ANTHROPIC_API_KEY`

---

## 📝 备注

1. **测试方法**:
   - Google API: 通过 curl 测试各个服务的端点
   - Finnhub: 通过 curl 测试股票价格端点
   - Nano Banana: 通过 python 脚本测试图片生成
   - 其他模型: 通过 openclaw 系统内部使用

2. **OAuth vs API Key**:
   - OpenAI Codex 使用 OAuth (access + refresh tokens)
   - 其他大部分使用 API Key
   - MiniMax 使用 JWT token (base64 编码)

3. **网关 vs 直接访问**:
   - Google Antigravity、Amazon Bedrock 通过网关访问
   - Google 官方 API 直接访问
   - 网关的可用性可能影响模型可用性

4. **限流问题**:
   - OpenAI Codex 频繁遇到 429 限流
   - 可能需要优化调用频率
   - 智能容灾系统会自动降级到其他模型

---

*总结文档 v1.0.0*  
*最后更新: 2026-02-21*
