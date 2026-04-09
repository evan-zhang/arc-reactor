# ARC Reactor V4 架构决策记录 (Architectural Decisions Log)

**记录时间**: 2026-04-08
**关联 Release Ticket**: RT-004, RT-005, RT-006
**核心目标**: 彻底杜绝大模型执行文件落盘时的编造幻觉，并全盘实现 Karpathy "Compilation over Retrieval" 知识构建体系。

---

## 决策一：多租户沙盒物理隔离 (RT-004)
*   **问题**: 所有的调研成果应该保存在哪里才能不互相覆盖？
*   **决策**: **Workspace 相对路径落盘**。我们废弃了复杂的绝对路径或环境变量解析，所有数据的根目录固定为 `./arc-reactor-doc/`。由于 OpenClaw 为不同 Agent 提供独占的 Workspace (CWD)，这就以最简单的物理法则实现了多租户安全隔离。

## 决策二：根治“落盘幻觉” (Issue #4 & Issue #6 修复)
*   **问题**: Sub-agent 在试图用 Bash 命令行如 `--content "大量MD正文"` 写入十万字的长文本时，由于无法处理复杂的引号转义（`"`, `'`, `$`），导致 Shell 崩溃报错。然而，Agent 缺乏二次核查机制，会直接向用户“编造假回执”谎称保存成功。
*   **解决方案 (三道防线)**:
    1.  **管道输入隔离**: 修改 `archive-manager.py`，丢弃 `--content` 命令行传参，强制其走 `--stdin` 管道模式，配合 Bash HereDoc 语法 `cat << 'EOF'`，完美屏蔽任意转义字符。
    2.  **强制 JSON 凭证查验**: 脚本不再执行死寂退出，而是强制向标准输出打印带有一体化哈希（`checksum`）的 JSON 凭证。Orchestrator 若收不到 `{"status": "success"}`，视为任务执行失败。
    3.  **铁律：附件必达**: 在 `SKILL.md` 中强制规定，Orchestrator 结束前需利用物理系统的 `message` 工具把真实文件作为附件发给用户。若文件不存在，工具本身会报错熔断幻觉。

## 决策三：升级为 Karpathy LLM Wiki 范式 (RT-006)
*   **问题**: V3 时期的知识系统缺乏“复利积累”，只是堆叠 `reports/` 流水账，没有跨时间线的信息提纯。
*   **决策**: 我们执行了结构大清洗，引入了 `wiki/` 体系。
    *   **架构重做**: 废弃原本分类，建立 `raw/` (生肉)、`wiki/sources/` (读后感)、`wiki/entities/` (实体卡片)、`wiki/index.md` (全库目录索引) 以及 `wiki/log.md` (修改追踪流)。
    *   **连击压制 (Ingest Combo)**: 将 `SKILL.md` 的说明书化身为 **LLM 编译器规范**。强制规定：只要触发 Ingest（摄入知识），Agent 必须连续调动 4 次归档脚本，写生肉、抽卡牌、挂目录、记日志。

## 决策四：Sub-Agent 重度任务超时规避
*   **问题**: V4 范式下，一套 Ingest 连招极其重度，单次 Token 耗时极长，可能面临物理超时。
*   **决策**: 
    1.  **Orchestrator Yield 机制**: 要求指挥官在 Spawn 派发后立刻脱手并挂起当前事件循环，杜绝阻塞主干等待。
    2.  **Model Routing (多模型配置)**: 落地了 `arc-reactor-config.yaml`。将耗时费脑的 Ingest 分发给 `GPT-4o` 旗舰节点，将批量的 Lint 重构或断链检查下放给成本极低的 `Gemini-Flash` 等高并发模型，实现成本与时间的双轴降级突破。
