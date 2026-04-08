# Media Extractor (Apple Silicon 本地零成本听写组件)

> 专为搭载 Apple Silicon 芯片（M1/M2/M3/M4 系列）的 Mac 电脑打造的流媒体语音转文字管线。  
> 利用 `yt-dlp` 剥离音轨 + Apple 原生 `MLX-Whisper` 框架进行本地离线转录，**零 API 费用、无限次使用**。

---

## 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 芯片 | Apple M1 | M4 Pro / M4 Max |
| 内存 | 8GB 统一内存 | 16GB+ 统一内存 |
| macOS | 13.0 Ventura | 最新稳定版 |
| Python | 3.10+ | 3.12+ |
| 磁盘 | 5GB 可用空间（模型权重缓存） | 10GB+ |

---

## 安装步骤

### 第一步：安装 FFmpeg（音频抽取依赖）

```bash
brew install ffmpeg
```

### 第二步：安装 yt-dlp（流媒体下载器）

```bash
brew install yt-dlp
```

> **⚠️ 关键排雷点：版本冲突**  
> 如果您的系统中曾经通过 `pipx` 安装过旧版 `yt-dlp`，可能会出现**新旧版本共存导致调用旧版**的问题。  
> 请执行以下命令确认当前生效的版本：
> ```bash
> which yt-dlp && yt-dlp --version
> ```
> 如果 `which` 指向的路径是 `~/.local/bin/yt-dlp` 而非 `/opt/homebrew/bin/yt-dlp`，说明 pipx 的旧版优先级更高。  
> 请执行 `pipx upgrade yt-dlp` 将其同步升级到最新版，否则抖音等平台将无法解析。

### 第三步：安装 Python 依赖（MLX-Whisper 核心引擎）

> **⚠️ 关键排雷点：macOS 的 pip 锁定机制**  
> 从 macOS Sonoma 开始，系统 Python 环境被标记为 `externally-managed`，直接使用 `pip install` 会报错。
> 请使用以下命令安装：

```bash
pip3 install --user --break-system-packages mlx-whisper
```

如果上述命令仍然失败，请改用：
```bash
python3 -m pip install --user --break-system-packages mlx-whisper
```

### 第四步：首次运行 — 模型权重下载（仅需一次）

`mlx-whisper` 在首次调用时会自动下载约 **3GB** 的 `Whisper-large-v3` 神经网络权重文件。

> **⚠️ 关键排雷点：国内网络下载极慢**  
> 默认从 Hugging Face 官方源下载，国内网络速度可能仅有几百 KB/s，需要等待 50 分钟以上。  
> **强烈建议**使用国内清华镜像源加速（实测 13MB/s，约 4 分钟完成）：
> ```bash
> export HF_ENDPOINT=https://hf-mirror.com
> ```
> 在首次运行脚本前执行此命令即可。下载完成后，后续所有调用均为**纯离线运行**，无需再次下载。

首次测试运行：
```bash
export HF_ENDPOINT=https://hf-mirror.com && python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "https://youtu.be/任意视频ID"
```

---

## 使用方式

### 方式一：在线视频 URL（YouTube / Bilibili 等）

```bash
python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "https://youtu.be/VIDEO_ID"
```

### 方式二：本地视频/音频文件（万能降维打击模式）

```bash
python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "/Users/you/Downloads/某个视频.mp4"
```

> 此模式绕过所有的网络反爬封锁，直接将本地文件喂入 MLX 神经核进行听写。  
> 支持格式：`.mp4` `.m4a` `.mp3` `.wav` `.webm` 等所有常见的音视频格式。

### 方式三：抖音口令文本（自动提取 URL）

```bash
python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "8.97 c@a.aN ... https://v.douyin.com/xxxxx/ 复制此链接..."
```

> 脚本内置正则引擎，会自动从抖音分享文案中提取纯净 URL。

---

## 抖音专项反爬指南

> **⚠️ 重要：抖音（字节跳动）的反爬封锁是目前所有平台中最为严厉的**

截至 2026 年 4 月，`yt-dlp` 对抖音的在线解析已被字节跳动的动态签名验证（`a_bogus`）全面封堵。**即使提供了真实的浏览器 Cookie，也无法直接通过 URL 在线下载抖音视频。**

### 解决方案：本地文件模式（推荐）

1. 在手机 App 中保存视频到本地（多数视频支持"保存到相册"）
2. 通过 AirDrop / 微信传输 / 数据线等方式传到 Mac
3. 使用本地文件模式执行转录：
```bash
python3 ~/.openclaw/skills/media-extractor/scripts/extract.py "/Users/you/Downloads/抖音视频.mp4"
```

### 备用方案：物理 Cookie 文件

如果未来 `yt-dlp` 修复了抖音的解析器，您可以提前准备好 Cookie 文件来实现全自动在线抓取：

1. 在 Chrome 中安装 [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) 插件
2. 访问 `https://www.douyin.com/` 并随意浏览一个视频
3. 点击插件导出 `cookies.txt`
4. 将文件放置到：`~/.openclaw/media/cookies.txt`

脚本会自动检测并优先使用此文件进行认证。

---

## 性能参考

基于 Mac mini M4 Pro (12核 CPU + 24GB 统一内存) 的实测数据：

| 视频时长 | 音频下载 | MLX 转录 | 总耗时 |
|---------|---------|---------|-------|
| 5 分钟  | ~5 秒   | ~15 秒  | ~20 秒 |
| 20 分钟 | ~15 秒  | ~45 秒  | ~60 秒 |
| 60 分钟 | ~30 秒  | ~2 分钟 | ~3 分钟 |

> 以上时间不包含首次模型下载。首次下载完成后，所有后续运行均为纯离线处理。

---

## 常见问题

### Q: `zsh: command not found: pip`
**A:** macOS 已不再默认提供 `pip` 命令，请使用 `pip3` 代替。

### Q: `error: externally-managed-environment`
**A:** 这是 macOS 的 PEP 668 保护机制。请在安装命令中添加 `--user --break-system-packages` 参数。

### Q: 运行时卡在 `Downloading... 0.00B`
**A:** 模型权重正在从 Hugging Face 下载。如果速度极慢，请设置镜像：`export HF_ENDPOINT=https://hf-mirror.com`。

### Q: 抖音视频在线抓取报错 `Fresh cookies are needed`
**A:** 字节跳动已全面封锁 yt-dlp 的在线解析接口。请改用"本地文件模式"直接传入已下载的视频文件。

### Q: `yt-dlp` 版本太旧导致解析失败
**A:** 请确认使用最新版本。如有多个安装源，优先通过 `pipx upgrade yt-dlp` 或 `brew upgrade yt-dlp` 进行升级。

---

## 技术栈

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — 开源流媒体下载器，支持 1800+ 平台
- **[MLX-Whisper](https://github.com/ml-explore/mlx-examples)** — Apple 官方 MLX 框架优化版 Whisper，原生利用 M 系列芯片的 GPU 和 Neural Engine
- **[Whisper Large-v3](https://huggingface.co/mlx-community/whisper-large-v3-mlx)** — OpenAI 开源的最高精度语音识别模型的 MLX 移植版
