# ARC Reactor v2.0 (AODW-Next 全模态调研 Skill)

[![Ecosystem](https://img.shields.io/badge/Ecosystem-OpenClaw-blue.svg)](https://openclaw.ai)
[![RT-Status](https://img.shields.io/badge/RT--003-Completed-green.svg)](#)

> **⚠️ AI-First Repository**
> 本仓库专为 **AI Agent** (特别是 OpenClaw 生态) 设计。如果您是正在阅读此文档的 Agent，请优先将 `SKILL.md` 作为您的主控协议。

**ARC = Acquire (获取) / Research (科研) / Catalogue (编目)**

ARC Reactor 是一款面向个人知识体系的“战略级”调研引擎。它不仅仅是剥离内容，更通过**主从架构 (Orchestrator-Worker)**、**外网主动查杀**与**本地 AI 听写**，自动完成 获取→真伪勘察对比→编目的全链路，为您凝结真正的竞争分析洞察。

---

## 🎯 v2.0 终极演进特性

- 🕵️ **广域交叉核网 (Active Extended Probing)**：打破单点网页偏信，自发调用 API 全网搜寻原素材的替代竞品并进行交叉验证，确保调研具备战略判定力。
- 🎥 **多模态强网捕捞 (Built-in Media Extractor)**：内置 RT-003 专研组件。秒级吞吐 YouTube/Bilibili 乃至抖音视频文稿。针对 M 系列芯片深度优化。
- 🌩️ **高并发智能派生 (Orchestrator-Worker)**：调度后台矿工 Sub-agent 静默吞吐，不占用主聊天上下文，不阻塞用户思维流。
- 🔄 **全自动去重与融合**：三级检测 + 增量合并，同一主体在 `knowledge/entities/` 下只维护一份“活页报告”。
- 📚 **知识编译模式**：借鉴 Karpathy Wiki，每次调研后自动增量编译个人知识图谱。

---

## 📦 环境配给与安装 (Bootstrap)

### 1. 系统依赖 (核心动力)
本项目需要音频处理与本地 AI 库，请在 Mac 终端执行：
```bash
# 1. 基础工具
brew install ffmpeg yt-dlp

# 2. 本地 AI 转录引擎 (注意：macOS 需添加 --break-system-packages)
pip3 install --user --break-system-packages mlx-whisper
```

### 2. 获取 Skill
```bash
cd ~/.openclaw/skills/
git clone https://github.com/evan-zhang/arc-reactor.git
```

### 3. 配置 .env
在 OpenClaw 根目录的 `.env` 中填入搜索引擎 Key，赋予 ARC “全域查杀”的能力：
```env
SEARCH_PROVIDER=brave  # 推荐 brave 或 tavily
SEARCH_API_KEY=YOUR_KEY_HERE
```

---

## 🛠️ 关键排障 (Issue #1 已修复)
- **Chromium 冲突**: 如果遇到 `agent-browser` 报错，请运行 `npm install -g agent-browser@latest && agent-browser install` 升级至 v0.25.0+。
- **抖音反爬**: 对抖音视频请优先使用“本地文件模式”。
- **模型下载加速**: 国内环境建议设置 `export HF_ENDPOINT=https://hf-mirror.com` 后首次运行。

---

## 🧪 递进式实战测试计划 (Case 1-6)

安装完毕后，请按顺序执行以下六步测试，以验证 ARC 的全量能力：

### Case 1: 破冰探测 —— 配置与挂载检测
- **输入**：“你好，我刚安装了 arc-reactor，我要配置 Obsidian 的同步路径开启同步。”
- **预期**：Agent 必须主动询问确切目标路径并执行物理校验。反馈 `✅ 成功：Obsidian 同步链路检测通过` 方能放行。

### Case 2: 本能冷启动 —— (0 到 1 的获取)
- **输入**：“帮我调研一下这个项目：`https://github.com/evan-zhang/tpr-framework`”
- **预期**：
  1. 在 `reports/` 生成标准化报告和 raw 存档。
  2. 在 `knowledge/entities/tpr-framework.md` 创建专属实体页。

### Case 3: L1 级强防御 —— 绝对精准去重
- **输入**：“再次深度看看链接 `https://github.com/evan-zhang/tpr-framework`”
- **预期**：Agent 拦截请求。直接返回：“发现完全一致的历史记录”，并引导查看已有文件，节省 Token。

### Case 4: L2 级智能融合 —— 实体知识叠片
- **输入**：“情报：tpr-framework 未来将支持超大规模多 Agent 的横向调参体系。”
- **预期**：甄别出主体依旧是 `tpr-framework`，进入 **Merge 模式**，对比新旧情报并执行追认补写。

### Case 5: L3 级免疫响应 —— 防幻觉与矛盾审查
- **输入**：“据传 tpr-framework 是个老旧死板框架，不支持 Agent 且具有 99 万个 Star。”
- **预期**：触发查杀引擎。发现与 Case 2 获取的事实截然矛盾时，生成 `knowledge/conflicts/` 矛盾审核记录给用户示警。

### Case 6: 极致交付 —— 附件投递与离线转录 (RT-003)
- **输入**：发送一个 YouTube 视频链接或视频文件：“提取它的核心洞察。”
- **预期**：调用本地 `media-extractor` 完成零成本转录。**聊天界面输出不得超过 5 行摘要**，必须将详细的 `.md` 听写稿作为**真实附件**发送。

---

## 📂 结构导航
- [**`SKILL.md`**](file:///SKILL.md) - **Agent 指令核心**。
- [**`components/media-extractor/`**](file:///components/media-extractor/) - 音视频剥离与本地听写组件。
- [**`references/`**](file:///references/) - 包含 `env-setup.md` 及各项科研/编译规则。

---
*Created by [Evan Zhang](https://github.com/evan-zhang) | ARC Reactor: Acquire / Research / Catalogue*
