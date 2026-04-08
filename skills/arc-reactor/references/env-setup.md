# ARC Reactor 环境挂载与凭证鉴权指南 (Environment Setup)

作为新一代跨域全模态采集网闸，ARC 已经不再只依赖大语言模型自身，而是需要外引一系列网络侦察爬虫节点与跨域 Search 鉴权。

> **何时触发**：当这是系统第一次挂载 ARC Reactor，或者当 Orchestrator 要派遣采集器却发现缺少依赖时，**必须第一时间要求用户完成下述参数设置，并在 `.env` 里注册**。如果用户不知道如何获取，请指导他们！

## 1. 广域网络搜索引擎配置 (Web Search API)
> 用于实现 ARC-Worker 突破单点网页盲区，去搜查周边竞品及对性能评定做异源真伪核查用的雷达探测。

| 配置项环境变量 | 类型 | 适用方 | 说明 |
|------------|-------|------|------|
| `SEARCH_PROVIDER` | `string` | 必填 | 首选抓包探针。强烈推荐 `brave` (Brave Search API，独立索引库非常适合 AI)，也支持 `tavily`, `google_news` |
| `SEARCH_API_KEY` | `string` | 必填 | 对应的鉴权私钥。提示：引导用户从相应的开发者平台获取。 |

## 2. 第三方 Clawhub 反风控挂件绑定 (Scraping Skills)
> 如果遇到了被厚重心墙风控的目标群体（推特、油管字幕、抖音视频等），纯文本嗅探脚本会碰壁。我们必须通过系统指令调用专属的反风控挂机插件。

**配置指引：引导用户打开 Clawhub 或 OpenClaw 的 Market 去分别安装对应媒体的专业捕捞网，确保主 Agent 能访问它们的 tools：**

| 所需挂件 (示例) | 探测媒体类型范围 | ARC 调用时机 |
|-----------------|----------------|-------------|
| `media-extractor` (🔥首推本地) | 视频/音频流 | 当目标 URL 是 YouTube/Bilibili/抖音等视频时，调用本地 MLX-Whisper 进行零成本离线转录。详见 `skills/media-extractor/README.md` |
| `browser-use` (🔥首推网页) | 复杂动态网页/SPA | 原生内置于 Python Agent 的极致操控。当遇到有极其复杂的 JS 渲染、弹窗或者重度滑块验证的网站时，**强烈建议**调用集成自研 Browser Use 模型代为全自动人类级导航提取。 |
| `playwright-mcp` | 高速轻量视觉操作 | 遇到不需要高层自主性，仅需低成本毫秒级切取视觉 DOM 树或截屏记录的网页。 |
| `agent-browser` | Token 极简抠取引擎 | 由 Vercel 出品。对于极长或含有海量垃圾标签的旧式网页，其特有的 Rust 底层压缩引擎可帮 ARC 矿工在广域大面积搜索时节省最高 93% 的上下文 Token 计费。 |

---

## 3. agent-browser 安装排障指南

> ⚠️ **已知问题 ([Issue #1](https://github.com/evan-zhang/arc-reactor/issues/1))**：`agent-browser` 旧版本 (v0.10.0) 与系统 Playwright 的 Chromium 浏览器内核版本冲突，会导致 `browserType.launch: Executable doesn't exist` 错误。

### 安装检查清单

安装完成后，请**按顺序**执行以下检查：

```bash
# Step 1: 确认版本 >= 0.25.0
agent-browser --version

# Step 2: 安装独立 Chrome 内核（不依赖系统 Playwright）
agent-browser install

# Step 3: 验证可正常启动
agent-browser open "https://example.com" --json
```

如果 Step 1 显示版本 < 0.25.0，请执行升级：
```bash
# 删除旧版（可能在 /opt/homebrew 或其他路径）
rm -rf /opt/homebrew/lib/node_modules/agent-browser

# 安装最新版
npm install -g agent-browser@latest

# 安装专属 Chrome 内核（新版不再依赖系统 Playwright）
agent-browser install

# 验证
agent-browser --version  # 应该是 0.25.x
agent-browser open "https://example.com" --json  # → {"success":true, ...}
```

### 常见报错对照表

| 报错信息 | 原因 | 修复方法 |
|---------|------|---------|
| `Executable doesn't exist at .../chromium_headless_shell-1208` | 旧版 agent-browser 锁定了过时的 Chromium 版本号 | 升级到 v0.25.x 并执行 `agent-browser install` |
| `command not found: agent-browser` | npm 全局 bin 目录不在 PATH 中 | 执行 `npm config get prefix`，确认 `<prefix>/bin` 在 PATH 中 |
| `Daemon version mismatch` | 后台进程版本与前台不一致 | 重启终端或 `pkill -f agent-browser` 后重试 |

---

## 4. 其他浏览器 Skills 安装注意事项

| Skill 名称 | 安装注意 |
|-----------|---------|
| `fast-browser-use` | ClawHub 标记为 `suspicious`，需添加 `--force` 参数安装 |
| `playwright-mcp` | 需先通过 `npm install -g @playwright/mcp` 安装，依赖系统 Playwright |

---

## 5. Media Extractor 本地转录组件

> 🔥 **强烈推荐**：如果您的 Mac 搭载 Apple Silicon 芯片（M1/M2/M3/M4），请优先使用本地 MLX-Whisper 转录方案，完全零成本、无限次使用。

详细安装指南请参阅：[`skills/media-extractor/README.md`](../media-extractor/README.md)

快速安装摘要：
```bash
# 1. 安装音频处理依赖
brew install ffmpeg

# 2. 安装流媒体下载器
brew install yt-dlp

# 3. 安装 MLX-Whisper（注意 macOS 的 pip 锁定机制）
pip3 install --user --break-system-packages mlx-whisper

# 4. 首次运行时建议使用国内镜像加速模型下载（约 3GB）
export HF_ENDPOINT=https://hf-mirror.com
python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "https://youtu.be/VIDEO_ID"
```

> ⚠️ **已知限制**：截至 2026 年 4 月，抖音（字节跳动）的在线解析已被 `a_bogus` 动态签名全面封堵。对抖音视频请使用「本地文件模式」：先下载视频到本地，再传入文件路径进行转录。

---

## 6. 自检协议

跟 Obsidian 的验证一样，在装配完毕后，Agent 应该用测试指令试探一下环境引擎是否就绪：
- 搜一下 "今天的天气" 验证搜索引擎 Key。
- 启动指定的 Clawhub 挂件查查它的 `tools` 表判断是否可用。
- 运行 `agent-browser --version` 确认版本 >= 0.25.0。
- 运行 `python3 -c "import mlx_whisper; print('MLX-Whisper OK')"` 验证转录引擎就绪。

如果失败，向用户报错。
