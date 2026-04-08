# RT-003: Media Extractor 开发全链路重构审计
> **日期**：2026-04-08
> **背景**：在 RT-002 中，为满足 ARC Reactor 主动获取外界情报的需求，亟需一个全能的视频解析剥离挂件。

## 1. 初步方案与妥协 (API Cloud Draft)
- **初始设想**：使用 `yt-dlp` 把视频 URL 切成音频后，调用 OpenAI 的 Whisper API 做听写发报。
- **弊端**：网络链路耗时，切片音频极容易在大于 25MB 时出错，且严重浪费算力和资金。

## 2. 突变与环境嗅探决议 (The MLX Shift)
- **环境嗅探**：通过 `system_profiler` 核查得知本机宿主装备有顶级 `Apple M4 Pro 12-core + 24GB Unified Memory` 巨兽级芯片。
- **果断重构**：完全抛弃外部 API 的弱者思维，将系统改挂至苹果本地底层加速库 `mlx-whisper`。
  1. 一方面，零成本无限白嫖听写；
  2. 其次，利用 24G 的恐怖显存吞吐，跳过任何音频切片动作，直接单线程光速干到底。
- **落地产物**：
  - `skills/media-extractor/scripts/extract.py`：作为挂件心脏，全管线整合。
  - `requirements.txt`：强制依赖 `mlx-whisper`。

## 3. 部署形态
作为 OpenClaw 生态的独立 Component 挂件存在（不耦合在 `arc-reactor` 库内），遵循通过独立 `SKILL.md` 向前台大模型分发使用指南。目前全系统环境均已初始化提交于 `feature/RT-003-media-extractor` 分支。
