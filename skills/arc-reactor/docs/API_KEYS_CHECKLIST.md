# OpenClaw API Keys 配置清单

> 统一的 API Key 管理文档
> 最后更新：2026-02-20

---

## 📊 当前配置状态

### ✅ 已配置的 API Keys

| 服务 | 环境变量 | 状态 | 用途 |
|------|---------|------|------|
| **OpenAI Codex** | OAuth (auth-profiles.json) | ✅ 已配置 | openai-codex/gpt-5.2-codex 模型 |
| **GLM (Zai)** | `ZAI_API_KEY` | ✅ 已配置 | GLM-4.7 模型 |
| **SGAI** | `SGAI_API_KEY` | ✅ 已配置 | SGAI 模型 |
| **MiniMax** | `MINIMAX_API_KEY` | ✅ 已配置 | MiniMax M2.1/M2.5 模型 |
| **Longbridge** | `LONGPORT_APP_KEY` | ✅ 已配置 | 证券交易 API |
| **Longbridge** | `LONGBOARD_APP_SECRET` | ✅ 已配置 | 证券交易 API |
| **Longbridge** | `LONGPORT_ACCESS_TOKEN` | ✅ 已配置 | 证券交易 API |
| **Apify** | `APIFY_TOKEN` | ✅ 已配置 | Web scraping API |
| **Pexels** | `PEXELS_API_KEY` | ✅ 已配置 | 图片搜索 API |
| **Browser Use** | `BROWSER_USE_API_KEY` | ✅ 已配置 | 浏览器自动化 API |
| **Discord** | `DISCORD_BOT_TOKEN` | ✅ 已配置 | Discord Bot |
| **Google Gemini** | `GOOGLE_GEMINI_API_KEY` | ✅ 已配置 | Gemini 2.5 Flash/Pro |
| **Google** | `GOOGLE_API_KEY` | ✅ 已配置 | 通用 Google API Key |
| **YouTube** | `YOUTUBE_API_KEY` | ✅ 已配置 | YouTube Data API |
| **Finnhub** | `FINNHUB_API_KEY` | ✅ 已配置 | 实时股票数据 |
| **Gemini (Nano Banana)** | `GEMINI_API_KEY` | ✅ 已配置 | 图片生成 API |
| **Tavily Search** | `TAVILY_API_KEY` | ✅ 已配置 | AI 驱动的搜索 API |

---

## 🟡 需要关注的问题

### 1. OpenAI Codex 频繁限流

**状态**: ✅ 已配置 (OAuth)
**问题**: 最近遇到 20 次限流错误 (429)
**当前状态**: 在冷却期

**影响**:
- ⚠️ openai-codex/gpt-5.2-codex 模型暂时不可用
- ⚠️ code-agent, stock-agent, trade-agent, ops-agent 自动降级到其他模型
- ✅ 智能容灾系统自动切换到降级模型

**可能原因**:
- API 配额不足
- 调用频率过高
- 达到速率限制

**建议**:
1. 登录 OpenAI Platform: https://platform.openai.com/
2. 检查 API 使用配额
3. 查看限流原因
4. 考虑升级账户或优化调用频率

---

### 2. Google APIs（推荐配置）

#### 2.1 通用 Google API Key

**用途**: 所有已启用的 Google Cloud 服务

**配置的 API Key**:
```bash
GOOGLE_API_KEY=AIzaSyDlELloBuK4bNHVy1kfrPrDIz2ZBqoSOAI
```

**已验证可用的服务**:
- ✅ **YouTube Data API** - 视频搜索和信息获取
- ✅ **Google Cloud Translation API** - 多语言翻译

**可能可用的服务** (取决于已启用的服务):
- Google Custom Search JSON API (需要 CSE ID)
- Google Maps API (需要启用)
- 其他 Google Cloud 服务

**如何使用**:
- YouTube 搜索：`GOOGLE_API_KEY`
- Google 翻译：`GOOGLE_API_KEY`
- 其他服务：`GOOGLE_API_KEY` + 相应的参数

---

#### 2.2 Google Gemini API

**用途**: Google Gemini 2.5 Flash/Pro 模型

**配置的 API Key**:
```bash
GOOGLE_GEMINI_API_KEY=AIzaSyDi_vmFpXnNPgL8FlQggwZwN114BS_JTy8
```

**可用模型**:
- Gemini 2.5 Flash - 轻量级，速度快，1M tokens
- Gemini 2.5 Pro - 高级版，1M tokens

---

#### 2.3 Google Custom Search JSON API (需要 CSE ID)

**用途**: Google 搜索结果

**需要的配置**:
```bash
GOOGLE_API_KEY=AIzaSyDlELloBuK4bNHVy1kfrPrDIz2ZBqoSOAI
GOOGLE_CSE_ID=...  # 需要在 Google CSE 中创建
```

**影响**:
- ⚠️ 需要额外的 CSE ID 才能使用
- ❌ 没有 CSE ID 无法使用搜索功能

**如何获取 CSE ID**:
1. 访问 https://programmablesearchengine.google.com/
2. 创建搜索引擎
3. 选择搜索范围（整个网络或特定网站）
4. 获取 CSE ID
5. 添加到 `~/.openclaw/.env`

---

#### 2.4 Google Maps API

**用途**: 地理位置、路线规划

**状态**: ❌ 未启用

**需要的操作**:
1. 访问 https://console.cloud.google.com/
2. 启用 Maps JavaScript API
3. API Key 已配置，但服务未启用

---

#### 2.5 YouTube Data API

**用途**: YouTube 视频搜索和信息获取

**需要的配置**:
```bash
YOUTUBE_API_KEY=...
```

**影响**:
- ❌ 无法搜索 YouTube 视频
- ⚠️ 无法获取视频详细信息

**如何获取**:
1. 访问 https://console.cloud.google.com/
2. 创建项目并启用 YouTube Data API v3
3. 创建 API Key
4. 添加到 `~/.openclaw/.env`

---

### 3. 金融数据 API（Stock Agent 需要）

#### 3.1 Finnhub

**用途**: 实时股票数据、财务报表、新闻

**需要的配置**:
```bash
FINNHUB_API_KEY=...
```

**影响**:
- ❌ stock-agent 无法获取实时股价
- ❌ 无法访问财务报表
- ❌ 无法获取相关新闻

**如何获取**:
1. 访问 https://finnhub.io/
2. 注册免费账户
3. 获取 API Key
4. 添加到 `~/.openclaw/.env`

---

#### 3.2 Alpha Vantage（备选）

**用途**: 股票数据、技术指标、外汇

**需要的配置**:
```bash
ALPHA_VANTAGE_API_KEY=...
```

**如何获取**:
1. 访问 https://www.alphavantage.co/support/#api-key
2. 注册免费账户
3. 获取 API Key
4. 添加到 `~/.openclaw/.env`

---

---

### 5. 其他推荐配置

#### 5.1 Google Drive API（可选）

**用途**: Google Drive 文件操作（补充桌面客户端）

**需要的配置**:
```bash
GOOGLE_DRIVE_CREDENTIALS_FILE=/path/to/credentials.json
GOOGLE_DRIVE_TOKEN_FILE=/path/to/token.json
```

**注意**: Google Drive 桌面客户端已配置同步，此 API 为可选，用于额外的程序化操作。

---

#### 5.2 Google Maps API（可选）

**用途**: 地理位置、路线规划

**需要的配置**:
```bash
GOOGLE_MAPS_API_KEY=...
```

---

#### 5.3 ElevenLabs TTS（可选）

**用途**: 高质量文本转语音

**需要的配置**:
```bash
ELEVENLABS_API_KEY=...
```

---

## 📋 优先级排序

### 🔴 P0 - 需要关注（立即检查）

1. **OpenAI Codex 限流问题**
   - 问题：频繁遇到 429 限流错误
   - 影响：最强模型暂时不可用，自动降级
   - 优先级：最高
   - 预计时间：5 分钟检查
   - 行动：检查 OpenAI Platform 配额

---

### ✅ 已配置（无需再配置）

1. **Google Gemini API**
   - 状态：✅ 已配置并验证
   - 可用模型：Gemini 2.5 Flash, Gemini 2.5 Pro
   - 用途：额外的模型选择
   - 优势：1M tokens，thinking 支持

2. **YouTube Data API**
   - 状态：✅ 已配置并验证
   - 用途：YouTube 视频搜索和信息获取
   - 功能：搜索视频、获取视频详情、频道信息
   - 测试：成功搜索 "artificial intelligence"

3. **Google Cloud Translation API**
   - 状态：✅ 已配置并验证
   - API Key：GOOGLE_API_KEY (通用 key)
   - 测试结果：✅ 成功翻译 "Hello" → "你好"
   - 功能：多语言翻译

4. **Finnhub API**
   - 状态：✅ 已配置并验证
   - 用途：实时股票数据、财务报表、新闻
   - 功能：
     - 实时股价
     - 财务报表
     - 公司新闻
     - 技术指标
   - 测试结果：✅ 成功获取 AAPL 股价 ($264.58)
   - 免费额度：60 次 API 调用/分钟

---

### 🟡 P1 - 强烈推荐（本周配置）

1. **Google Custom Search API** (需要 CSE ID)

---

### 🟢 P3 - 可选（按需配置）

1. **Alpha Vantage API** - Finnhub 的备选
2. **Google Maps API** - 地理相关功能
3. **ElevenLabs TTS** - 高质量语音
4. **Google Drive API** - 额外的 Drive 操作

---

## 🔧 配置步骤

### 1. 编辑 .env 文件

```bash
# 打开 .env 文件
nano ~/.openclaw/.env

# 或使用其他编辑器
code ~/.openclaw/.env
```

### 2. 添加新的 API Keys

```bash
# 示例：添加 OpenAI API Key
OPENAI_API_KEY=sk-proj-xxxxxx

# 示例：添加 Google API Keys
GOOGLE_API_KEY=AIzaSy...
GOOGLE_CSE_ID=xxxxxxxxx

# 示例：添加 Finnhub API Key
FINNHUB_API_KEY=xxxxx
```

### 3. 保存文件

保存后，新的 API Keys 立即生效。

---

## ✅ 验证配置

### 测试 OpenAI API

```bash
# 测试 OpenAI 连接
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 测试 Google API

```bash
# 测试 Google Custom Search API
curl "https://www.googleapis.com/customsearch/v1?key=$GOOGLE_API_KEY&cx=$GOOGLE_CSE_ID&q=test"
```

### 测试 Finnhub API

```bash
# 测试 Finnhub API
curl https://finnhub.io/api/v1/stock/symbol?exchange=US&token=$FINNHUB_API_KEY
```

---

## 📊 配置完成度

| 类别 | 已配置 | 总计 | 完成度 |
|------|--------|------|--------|
| **模型 API** | 5 (OpenAI Codex, GLM, SGAI, MiniMax, Google Gemini) | 5 | 100% |
| **Google API** | 3 (Google Gemini, YouTube, Google Cloud Translation) | 4 | 75% |
| **金融 API** | 2 (Longbridge, Finnhub) | 3 | 67% |
| **搜索 API** | 2 (Apify, Tavily) | 2 | 100% |
| **其他 API** | 3 (Pexels, Browser Use, Discord) | 3 | 100% |
| **总计** | 14 | 16 | 88% |

---

## 🎯 下一步行动

### 立即检查

1. [ ] 检查 OpenAI Platform 配额 (P0)
   - 访问 https://platform.openai.com/
   - 检查 API 使用配额
   - 查看限流原因
   - 考虑优化调用频率或升级账户

### 本周行动

2. [ ] 配置 Google Custom Search API (P1)

### 本月行动

4. [ ] 配置 YouTube Data API (P2)
5. [ ] 配置 Tavily Search API (P2)
6. [ ] 配置 Google Translation API (P2)

---

## 📞 需要帮助？

如果需要帮助配置任何 API Key，请告诉我：
- 你需要配置哪个服务？
- 是否需要我帮你测试连接？
- 是否需要我帮你生成配置脚本？

---

*API Keys 配置清单 v1.5.0*  
*最后更新: 2026-02-21*  
*更新内容：新增 Finnhub API 配置，stock-agent 现在可以访问实时股票数据*
