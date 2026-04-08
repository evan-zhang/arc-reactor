# ARC Reactor 环境挂载与凭证鉴权指南 (Environment Setup)

作为新一代跨域全模态采集网闸，ARC 已经不再只依赖大语言模型自身，而是需要外引一系列网络侦察爬虫节点与跨域 Search 鉴权。

> **何时触发**：当这是系统第一次挂载 ARC Reactor，或者当 Orchestrator 要派遣采集器却发现缺少依赖时，**必须第一时间要求用户完成下述参数设置，并在 `.env` 里注册**。如果用户不知道如何获取，请指导他们！

## 1. 广域网络搜索引擎配置 (Web Search API)
> 用于实现 ARC-Worker 突破单点网页盲区，去搜查周边竞品及对性能评定做异源真伪核查用的雷达探测。

| 配置项环境变量 | 类型 | 适用方 | 说明 |
|------------|-------|------|------|
| `SEARCH_PROVIDER` | `string` | 必填 | 首选抓包探针。比如 `brave`, `tavily`, `google_news` |
| `SEARCH_API_KEY` | `string` | 必填 | 对应的鉴权私钥。提示：引导用户从相应的开发者平台获取。 |

## 2. 第三方 Clawhub 反风控挂件绑定 (Scraping Skills)
> 如果遇到了被厚重心墙风控的目标群体（推特、油管字幕、抖音视频等），纯文本嗅探脚本会碰壁。我们必须通过系统指令调用专属的反风控挂机插件。

**配置指引：引导用户打开 Clawhub 或 OpenClaw 的 Market 去分别安装对应媒体的专业捕捞网，确保主 Agent 能访问它们的 tools：**

| 所需挂件 (示例) | 探测媒体类型范围 | ARC 调用时机 |
|-----------------|----------------|-------------|
| `media-extractor` (🔥内置) | 视频/音频流 | 位于 `components/media-extractor/`。详见 [README.md](../README.md) 进行本地安装。 |
| `browser-use` (🔥首推网页) | 复杂动态网页/SPA | 深度自主浏览。推荐作为处理 JS 渲染和弹窗的重型武器。 |
| `agent-browser` | Token 极简抠取引擎 | 极大节省长网页总结时的 Context 计费。 |
| `twitter-mcp` | 文本强社交 | 当目标是 X 平台，获取其底下的回帖与社交反响。 |

---

## 3. agent-browser 安装排障指南

> ⚠️ **已知问题**：`agent-browser` 旧版本 (v0.10.0) 与系统 Playwright 的 Chromium 浏览器内核版本冲突，会导致启动失败。

### 安装检查清单
1. **确认版本 >= 0.25.0**：`agent-browser --version`
2. **安装独立内核**：`agent-browser install`
3. **升级指令**：
   ```bash
   npm install -g agent-browser@latest
   agent-browser install
   ```

---

## 4. Media Extractor 本地转录组件 (Apple Silicon 专用)

> 🔥 **强烈推荐**：如果您的 Mac 搭载 M1/M2/M3/M4 芯片，请务必启用本地 MLX-Whisper，实现零成本无限次视频听写。

### 快速安装
```bash
# 1. 音频处理底层
brew install ffmpeg yt-dlp

# 2. 听写神经引擎 (注意 --break-system-packages)
pip3 install --user --break-system-packages mlx-whisper

# 3. 首次运行建议加速模型下载
export HF_ENDPOINT=https://hf-mirror.com
```

> ⚠️ **抖音说明**：目前抖音在线解析受阻，请先将视频下载到本地，直接喂给地址：
> `python3 components/media-extractor/scripts/extract.py "/path/to/video.mp4"`

---

## 5. 自检协议

装配完毕后，Agent 应该用测试指令试探一下环境是否就绪：
- 搜一下 "今天的天气" 验证搜索引擎 Key。
- 启动指定的 Clawhub 挂件查查它的 `tools` 表判断是否可用。
- 运行 `agent-browser --version` 确认版本 >= 0.25.0。
- 执行一次本地音频的 `extract.py` 测试。

如果失败，向用户报错。
