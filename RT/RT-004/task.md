# RT-004: Archive Manager Implementation

- [x] 1. 设计 Python 命令行传参结构 (`argparse`)
- [x] 2. 接收 standard input (管道流) 防止特殊字符引发 Shell 崩溃
- [x] 3. 制定 `reports/` 和 `raw/` 的写文件路由逻辑
- [x] 4. 添加重复校验防范（如果目标 Topic 已存在该如何追加）
- [x] 5. 在 `SKILL.md` 中更新调用指令，全面弃用 Bash 命令写文件

> **状态更新**：全项打平完成，作为 ARC 的核心基础能力稳定服役。
