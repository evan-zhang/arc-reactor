# Issue: media-extractor 组件在 macOS 新环境首次使用时遇到多个兼容性问题

## 概述

在 macOS 新环境（Apple Silicon M4 Pro）首次使用 media-extractor 组件提取 YouTube 视频时，遇到了多个依赖和环境兼容性问题，导致无法按预期流程完成提取。

---

## 问题列表

### 问题 1: yt-dlp 通过 pip 安装与 brew 安装冲突，导致 YouTube 下载失败

**环境:**
- macOS（系统 Python 3.9 → 后升级到 brew Python 3.14）
- yt-dlp 通过 `pip3 install yt-dlp` 安装到了系统 Python 3.9 环境

**现象:**
```
[ERROR] 所有的反爬穿透策略 (包括本机浏览器伪造) 均遭遇字节跳动强力拦截关卡失效！
```

**根因:**
1. pip 安装的 yt-dlp 版本过旧（Python 3.9 compatible version）
2. 系统同时存在多个 Python 版本（3.9 / 3.14），pip 装的包和 brew python 运行时不对应
3. 缺少 FFmpeg（音频抽取依赖）

**解决:**
```bash
brew install yt-dlp ffmpeg
```

安装后 `yt-dlp --version` 显示 `2026.03.17`，YouTube 音频下载恢复正常。

---

### 问题 2: mlx-whisper 安装到了错误的 Python 环境

**现象:**
```
[ERROR] mlx_whisper is not installed. Please run: pip3 install mlx-whisper yt-dlp
```

**根因:**
- `pip3 install mlx-whisper` 把包安装到了 `/Users/xgjk/Library/Python/3.9/lib/python/site-packages/`
- 但运行时 `python3 --version` 指向的是 brew 安装的 Python 3.14
- 两个环境不互通

**解决:**
```bash
python3 -m pip install --user --break-system-packages mlx-whisper
```
（使用 python3.14 的 pip 安装）

---

### 问题 3: 首次运行需要下载 ~3GB 模型权重，国内网络极慢

**现象:**
- MLX-Whisper 首次运行需要下载 `whisper-large-v3` 模型（约 3GB）
- 默认从 HuggingFace 官方源下载，速度几百 KB/s，需要 50 分钟以上

**解决:**
```bash
export HF_ENDPOINT=https://hf-mirror.com
```
使用清华镜像后速度提升到约 2MB/s，约 25 分钟完成下载。

---

### 问题 4: media-extractor 脚本的错误信息具有误导性

**现象:**
YouTube 视频提取失败时，脚本输出：
```
[FATAL ERROR] 所有的反爬穿透策略 (包括本机浏览器伪造) 均遭遇字节跳动强力拦截关卡失效！
[ACTION REQUIRED] 必须使用终极物理钥匙：
1. 请在您的电脑浏览器打开一次 https://www.douyin.com/
2. 使用 Chrome 插件 'Get cookies.txt LOCALLY' 导出一份 cookies.txt 文件
```

**问题:**
- 这个错误信息是 Douyin（字节跳动）的专项反爬处理，但用户传入的是 YouTube 视频
- 错误信息完全误导用户，让人以为需要在抖音登录

**建议:**
- 区分 YouTube 和 Douyin 的错误处理信息
- YouTube 失败时给出不同的排查建议（检查 yt-dlp 版本、FFmpeg 是否安装等）

---

### 问题 5: 脚本超时机制导致长任务（模型下载 + 转写）被 SIGTERM 杀死

**现象:**
- 模型下载（约 3GB）需要 20+ 分钟
- OpenClaw exec 工具有 600 秒超时限制
- 进程被 `SIGTERM` 强制终止

**当前 workaround:**
使用 `nohup ... &` 在后台独立运行，不受超时限制。

**规范解决方案（建议）:**
- 文档中明确说明首次使用需要下载大模型，建议用户耐心等待
- 或者提供 `--no-download-model` 选项，允许跳过已下载模型的检查
- 或者在脚本内部处理模型下载，不依赖 exec 超时机制

---

## 环境信息

- **芯片:** Apple Silicon (arm64)
- **OS:** macOS
- **Python:** 3.14.4 (brew), 3.9 (系统)
- **yt-dlp:** 2026.03.17 (brew)
- **FFmpeg:** 8.1 (brew)
- **mlx-whisper:** 0.4.3

---

## 建议的修复优先级

| 优先级 | 问题 | 建议 |
|--------|------|------|
| P0 | 错误信息误导 | 区分 YouTube/Douyin 错误提示 |
| P1 | Python 环境混乱 | 文档中明确指定使用哪个 python/pip |
| P2 | 超时杀死长任务 | 提供模型预下载脚本或 --no-download 选项 |
| P3 | FFmpeg 依赖缺失 | 在脚本执行前增加 FFmpeg 检测并给出明确安装指引 |

---

## 相关文档

- media-extractor/SKILL.md
- media-extractor/scripts/extract.py
- RT/RT-002/spec-lite.md（VIDEO 管道设计）
