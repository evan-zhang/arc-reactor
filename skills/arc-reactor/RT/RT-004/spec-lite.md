# RT-004 Spec-Lite: Archive Manager Implementation (Python 管道替代方案)

## 📌 1. 业务痛点
原有的 `SKILL.md` 中，我们使用 Bash 中的 `sed` 和 `awk` 对流式文本进行硬拼接来生成调查报告。这种方式极其脆弱，一旦遇到 Markdown 正文里出现转义字符或特殊标点，系统直接语法崩溃。

## 🎯 2. 解决方案
开发纯 Python 版本的存储引擎模块 `archive-manager.py`。
- **放弃 Shell 拼接**：改用 `--stdin` (HereDoc) 透传完整数据流，使用 Python 进行 I/O 处理。
- **引入路由机制**：在当时（V3 阶段）添加基础的参数 `--topic`，能自动检测是否重名，并将报告与原始数据存放于分离的 `./reports/` 以及 `./raw/`。

*(注：该脚本基础底座已随后被用于对接后续 RT-006 的 Karpathy Wiki 全面升级，本 RT 已作为底座完备并合入主线。)*
