# RT-016: Media Extractor Module (Issue #47)

## 1. 简介 (Introduction)
本项目在 v4.3.0 版本中集成了音视频转录模块 `media-extractor.py`。本规范用于记录该功能的实现细节与集成路径。

## 2. 核心功能
- **多模态输入**：支持 YouTube URL 和本地 mp4/mp3 文件。
- **转录引擎**：集成 `yt-dlp` 进行视频提取，配合 `whisper` 进行本地转录。
- **Wiki 集成**：转录后的内容会自动进入 Ingest 流程，转换为 Source 文档。

## 3. 协作记录
- **实现人**：ClaudeCode (Xiao Long Xia)
- **合入方式**：PR #47
- **治理补正**：Antigravity (补充 RT 记录与审计)

---
*Verified and released in v4.3.0*
