# ARC Reactor v2.0 (AODW-Next 全模态调研 Skill)

[![OpenClaw](https://img.shields.io/badge/Ecosystem-OpenClaw-blue.svg)](https://openclaw.ai)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

> **⚠️ AI-First Repository**: 本仓库专为 **AI Agent** 设计。如果您是正在阅读此文档的 Agent，请优先将 `SKILL.md` 作为您的主控协议。

**ARC = Acquire (获取) / Research (科研) / Catalogue (编目)**

ARC Reactor 是面向个人知识体系的“战略级”调研引擎。它通过 **Orchestrator-Worker (主从) 架构**，将单一链接扩展为跨维度的深度报告。

---

## 🚀 RT-003 特性展示：内置“武器库” (Built-in Tools)

本项目不仅是逻辑框架，还内置了在 RT-003 阶段深度自研的黑科技插件：

### 🎙️ 神经听写核心 (Media Extractor)
- **零成本转录**：针对 Apple Silicon (M1-M4) 深度优化，调用本地 MLX-Whisper 大模型。
- **万能剥离**：内置 `yt-dlp` 增强版逻辑，一键提取 YouTube/Bilibili 音频。
- **抖音穿透**：针对字节跳动动态签名提供物理降级方案，支持本地视频直读转录。

### 🕵️ 查杀扫描仪 (Validation Engine)
- **异源校对**：自动调用搜索引擎对原网页内容进行“打假”，识别虚假陈述并标记 `[DISPUTED]`。
- **替代品检索**：当调研一个工具时，自动搜集全网竞品进行横向对比。

---

## 📦 安装说明 (Step-by-Step Guide)

用户只需克隆本项目到 OpenClaw 即可拥有上述所有特性。

### 1. 系统依赖安装 (必须)
在 Mac 终端执行，为本地 AI 转录提供底层动力：

```bash
# 音频处理与下载
brew install ffmpeg yt-dlp

# 本地神经核引擎 (M4 Pro 转录 20 分钟音频仅需约 1 分钟)
pip3 install --user --break-system-packages mlx-whisper
```

### 2. 获取 Skill
```bash
cd ~/.openclaw/skills/
git clone https://github.com/evan-zhang/arc-reactor.git
```

### 3. 环境变量配置
在 `.env` 中注册以下 Key，赋予 ARC Reactor “全网搜查”的权限：
```env
SEARCH_PROVIDER=brave  # 推荐使用 brave 或 tavily
SEARCH_API_KEY=YOUR_KEY_HERE
```

---

## 🛠️ 进阶配置：多媒体反爬钥匙 (Cookie Setup)

遇到抖音/YouTube 的强力风控时，请执行以下操作：
1. 在浏览器导出一份 `cookies.txt`。
2. 将文件放置在项目根目录的 `media/cookies.txt`。
*内置的 `extract.py` 会自动探测该位置并以此作为穿透钥匙。*

---

## ✅ 验证安装是否成功？

您可以向您的 Agent 发送以下指令来测试：

- **测试 1 (网页查杀)**: `"帮我调研一下 ARC Reactor 的 GitHub 仓库内容。"`
- **测试 2 (多媒体提取)**: (发送一个 YouTube 链接) `"把这个视频的文稿听写出来。"`
- **测试 3 (本地兜底)**: (直接上传一个视频文件) `"识别这个本地文件的内容并进行编目。"`

---

## 📂 结构导航
- [**`SKILL.md`**](file:///SKILL.md) - **Agent 指挥中心**。定义了主从代理的协同纪律。
- [**`components/media-extractor/`**](file:///components/media-extractor/) - 核心插件源代码。
- [**`references/env-setup.md`**](file:///references/env-setup.md) - 针对 Issue #1 的详细排障清单。

---
*Created by [Evan Zhang](https://github.com/evan-zhang) | Powered by AODW-Next Workflow*
