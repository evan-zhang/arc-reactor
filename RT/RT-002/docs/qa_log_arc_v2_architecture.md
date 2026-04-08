# ARC Reactor v2.0 & Media Extractor 架构决议审计日志
> **记录日期**：2026-04-08
> **归属 RT**：RT-002
> **涉及系统**：ARC Reactor (v2.0), Media Extractor (New Skill)

## 1. ARC Reactor v2 核心降维与架构升级

### 1.1 Orchestrator-Worker 双轨抽离
- **原因**：v1 版本单线运行，遇到几万字的长文章和长耗时的网络请求，会导致主控聊天界面阻塞瘫痪。
- **决议**：采用 `Announce-then-act` 与 `Yield-after-spawn` 纪律。主 Agent 只做大意图拦截与并发派工，真正耗时脏活累活丢入独立子窗口让 `ARC-Worker` 完成，实现异步非阻塞交互。

### 1.2 附件化极简交付 (The Ironclad Rules)
- **原因**：全量打印 Markdown 报告会导致移动端、Telegram 客户端体验极差。
- **决议**：所有的最终研究报告物理落盘，强制通过附件形式投递给用户，不占用聊天框超过 5 行字的摘要。

### 1.3 广域网络主动寻的 (Active Extended Probing)
- **原因**：老旧的爬虫往往偏听偏信原链接作者的推广文。
- **决议**：在复查 (R) 阶段，强制挂载 `tavily` 或 `brave` 引擎，针对所提取的主体向外网发散搜索（如寻找 Alternative 竞品、舆论造假等），生成复合型横向对比资料。

---

## 2. Browser Use 与网络基建选型门禁

### 2.1 BootStrap 环境检测机制 (`env-setup.md`)
- **原因**：以上诸多功能全部重度依赖外部 API 和爬虫组件，如果缺失则组件报废。
- **决议**：建立装载门禁指令，第一次挂载需要用户自检网络 API 状态。
- **技术栈入选定级**：
  - `browser-use`: 应对重度反爬 SPA，最高首选框架（基于 LLM + Playwright）。
  - `playwright-mcp`: 轻量级降维视觉工具。
  - `agent-browser`: 专门应对极长旧式网页的 Token 轻量优化引擎。

---

## 3. Media Extractor 流媒体降维剥离机诞生 (M4 专属版)

### 3.1 零开销反网络封锁设计
- **核心痛点**：音视频往往带有严苛封锁水表及厚重的格式，无法喂给普通语言模型。
- **组件定性**：在 `skills/media-extractor/` 建立独立小挂件，专责“输入 URL -> 吐出 .md 字幕与文稿”。
- **架构方案**：
  - **切音频**：使用 `yt-dlp` 代替手搓爬虫，仅切割纯音轨 `.m4a` / `.mp3`，大幅节省硬盘与带宽开销。
  - **白嫖 MLX**：针对用户机器 `Apple M4 Pro + 24G UMA 内存`，彻底废弃 `OpenAI Whisper API` 计费方案，改用苹果原生的神经计算核心加速库 `mlx-whisper`。
  - **零切片**：因 M4 Pro 的恐怖宽容度，无需像旧时代机器那样切小段喂养，直接吃满大时长的听写进程。
