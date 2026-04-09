# RT-004 提交记录与代码追溯 (Git Commit History)

本文件用于补齐 RT-004 (Archive Manager Implementation) 期间核心代码 `archive-manager.py` 的物理变更追溯，确保架构规划与实际代码提交相符。

## 📅 关联 Commit Log 日志

### 1. 引擎初次加载与基础重构整合
*   **Commit ID**: `2121f46` (此 Commit 为 V4.0 大版本的汇总提交，涵盖了 RT-006 内容以及 RT-004 的引擎)
*   **Message**: `feat(v4.0.3): upgrade to Karpathy Wiki architecture, add dual-track date logic, remove RT from release package`
*   **变更文件**: 
    *   `scripts/archive-manager.py` (+150 insertions)
*   **说明**: 此节点彻底用 Python 的 `os.path.join` 和 `argparse` 取代了旧版 Bash `sed/awk`，建立了基础的文件读写安全阀（采用 `--stdin`）和原子落盘。

### 2. Issue 8 补丁强化（Date 注入强制化）
*   **Commit ID**: `1fb1a52` 
*   **Message**: `fix(archive): Issue #8 - absolutely enforce date injection in frontmatter & JSON receipt`
*   **变更文件**: 
    *   `scripts/archive-manager.py` | 24 +++++++++++++++---------
*   **说明**: 核心维护了脚本写前探测能力，即便没有 YAML 格式的纯文本也会被暴力注入 `date:` 头。

### 3. Issue 9 补丁强化（参数防空转）
*   **Commit ID**: `254dab0`
*   **Message**: `fix(archive): Issue #9 handle None value for args.date fallback`
*   **变更文件**: 
    *   `scripts/archive-manager.py` | 4 +++-
*   **说明**: 修复了 `--date` 参数获取为 `None` 时导致的 `wiki/sources/None/` 路径生成故障。

---
*注：由于代码编写与功能合并采取了一次性冲刺打包推送（Run Command 批量执行），因此具体的 commit log 大部分汇聚在 v4 整体补丁的头上，但这些提交实打实地落地了 RT-004 设定的所有 Python 化 I/O 隔离管线要求。*
