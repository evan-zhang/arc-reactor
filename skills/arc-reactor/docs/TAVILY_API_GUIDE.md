# Tavily Search API 配置指南

## 📋 Tavily 是什么？

Tavily 是一个专为 AI 和 LLM 设计的搜索 API，提供智能、结构化的搜索结果。

---

## 🎯 主要用途

### 1. AI-News Agent（核心）

**实时新闻聚合**:
- 搜索最新的 AI 相关新闻
- 自动去重和排序
- 提供结构化数据（标题、摘要、URL、来源）
- 支持多语言搜索
- 支持时间过滤（最近 1 小时/1 天/1 周）

**为什么优于普通搜索**:
- ✅ 专为 LLM 设计，返回 JSON 格式
- ✅ 支持深度搜索（不只是关键词匹配）
- ✅ 自动内容提取和摘要生成
- ✅ 支持多轮对话和 follow-up

**示例场景**:
```
搜索："最近 24 小时的 AI 新闻"
→ 返回：[{title, url, snippet, published_date, source}, ...]

搜索："关于 OpenAI GPT-5 的新闻"
→ 返回：相关的、去重的、按时间排序的新闻列表
```

### 2. 其他 Agents

- **Code-Agent**: 搜索技术文档、教程、Stack Overflow
- **Stock-Agent**: 搜索财经新闻、市场分析、公司动态
- **Docs-Agent**: 搜索参考资料、相关文档、写作素材
- **Trade-Agent**: 搜索交易策略、市场趋势、风险管理

---

## 📊 Tavily vs 其他搜索 API

| 功能 | Tavily | Google Custom Search | Brave Search | DuckDuckGo |
|------|--------|---------------------|--------------|-----------|
| AI-optimized | ✅ | ❌ | ❌ | ❌ |
| 结构化 JSON 输出 | ✅ | ⚠️ 需要解析 | ⚠️ 需要解析 | ❌ |
| 实时结果 | ✅ | ✅ | ✅ | ✅ |
| Follow-up 搜索 | ✅ | ❌ | ❌ | ❌ |
| 多语言支持 | ✅ | ✅ | ⚠️ 有限 | ✅ |
| 免费额度 | 1000 次/月 | ❌ 付费 | ✅ 免费 | ✅ 免费 |
| API 简单度 | ✅ 非常简单 | ⚠️ 中等 | ✅ 简单 | ✅ 简单 |

---

## 🔧 配置步骤

### 1. 获取 API Key

如果你已经有 key，跳过这一步。

如果没有：
1. 访问 https://tavily.com/
2. 注册免费账户
3. 在 Dashboard 中获取 API Key

### 2. 配置到 OpenClaw

**方法 1：手动添加到 .env**
```bash
# 打开 .env 文件
nano ~/.openclaw/.env

# 添加以下内容
TAVILY_API_KEY=tvly-你的API密钥

# 保存文件
```

**方法 2：使用命令添加**
```bash
echo "TAVILY_API_KEY=tvly-你的API密钥" >> ~/.openclaw/.env
```

---

## 📝 使用示例

### 搜索新闻

```javascript
// 使用 Tavily 搜索 AI 新闻
const response = await fetch('https://api.tavily.com/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    api_key: process.env.TAVILY_API_KEY,
    query: "artificial intelligence news",
    search_depth: "advanced",  // basic 或 advanced
    max_results: 10,
    include_images: false,
    include_image_descriptions: false,
    include_answer: true,
    include_raw_content: false,
    days: 1  // 最近 1 天
  })
})

const data = await response.json()

// 返回结构化数据
// {
//   answer: "搜索结果摘要",
//   query: "搜索查询",
//   results: [
//     {
//       title: "新闻标题",
//       url: "新闻链接",
//       content: "新闻摘要",
//       score: 相关性评分,
//       published_date: "发布时间"
//     },
//     ...
//   ]
// }
```

### 搜索技术文档

```javascript
const response = await fetch('https://api.tavily.com/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    api_key: process.env.TAVILY_API_KEY,
    query: "Next.js 14 server components tutorial",
    search_depth: "advanced",
    max_results: 5,
    include_answer: true,
    include_domains: ["nextjs.org", "vercel.com", "dev.to"]
  })
})
```

### Follow-up 搜索（基于上下文）

```javascript
// 第一次搜索
const search1 = await tavilySearch("React hooks best practices")

// 基于第一次搜索结果进行 follow-up
const search2 = await tavilySearch({
  query: "如何避免 useEffect 中的无限循环",
  include_raw_content: true,
  search_depth: "advanced"
})
```

---

## 🎓 在 AI-News Agent 中的使用

### 新闻聚合流程

```
1. 获取用户查询（如"最近的 AI 新闻"）
   ↓
2. 使用 Tavily 搜索（time_range: "1d"）
   ↓
3. 解析 JSON 响应
   ↓
4. 去重和排序
   ↓
5. 生成结构化输出
   ↓
6. 发送给用户
```

### 示例输出

```json
{
  "topic": "AI 新闻",
  "time_range": "最近 24 小时",
  "articles": [
    {
      "title": "OpenAI 发布 GPT-5 预览版",
      "url": "https://example.com/article1",
      "summary": "Tavily 自动生成的摘要...",
      "source": "TechCrunch",
      "published_at": "2026-02-21T01:00:00Z",
      "relevance_score": 0.95
    },
    {
      "title": "Google DeepMind 新突破",
      "url": "https://example.com/article2",
      "summary": "...",
      "source": "The Verge",
      "published_at": "2026-02-21T00:30:00Z",
      "relevance_score": 0.92
    }
  ],
  "total": 10
}
```

---

## 💰 免费额度

**Tavily Free Plan**:
- 每月 1,000 次 API 调用
- 支持 basic 和 advanced 搜索
- 无需信用卡
- 适合开发和测试

**升级计划**:
- Researcher: $19/月，10,000 次
- Team: $99/月，60,000 次
- Enterprise: 自定义

---

## ✅ 配置验证

### 测试连接

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "你的API密钥",
    "query": "test search",
    "max_results": 3
  }'
```

### 成功响应示例

```json
{
  "answer": "test search results",
  "query": "test search",
  "results": [...]
}
```

---

## 🚀 立即配置

如果你已经有 API Key，请告诉我，我帮你配置到系统中！

---

*Tavily Search API 配置指南 v1.0.0*  
*最后更新: 2026-02-21*
