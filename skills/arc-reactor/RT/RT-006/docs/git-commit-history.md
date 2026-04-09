# RT-006 提交记录与代码追溯 (Git Commit History)

本文件用于补齐 RT-006 (Karpathy LLM Wiki Architecture) 实施过程中的物理变更日志，映射该大范式跃迁落地了哪些具体的 Repo 提交。

## 📅 关联 Commit Log 日志与文件溯源

本次 V4 大重构的核心理念将过去“阅后即焚”的单一 Markdown 报告，拉伸为了网状、附带双轨记账的私库。

### 1. 核心骨架搭建与架构重塑
*   **Commit ID**: `2121f46`
*   **Message**: `feat(v4.0.3): upgrade to Karpathy Wiki architecture, add dual-track date logic, remove RT from release package`
*   **主要波及文件**:
    *   `arc-reactor-config.yaml`: **[新增]** 将配置引擎抽离，设置 Ingest/Lint 多模型分派。
    *   `SKILL.md`: 将技能描述转译为 **Karpathy 编译器指导原则**，增加了4连击规范（Source/Index/Entity/Log）。
    *   `README.md`: 大幅抹去 `v2` 历史描述，更新 `wiki/` 目录树架构规范和测试大纲。
*   **说明**: 这是 RT-006 真正的主权标志性提交。在这个单次推送中落地了所有 Wiki 范式的改动。

### 2. 测试场景与说明扩容
*   **Commit ID**: `c39f58e`
*   **Message**: `docs: expand README with advanced Query, Analysis and Extraction cases`
*   **主要波及文件**:
    *   `README.md`: 新增了深度的商业化使用 Case (知识图谱游走、时序对比、大扫除等)。
*   **说明**: 呼应 RT-006 设计目的中的“方便二次 Query 查询提取”，通过文档层面定调该系统的玩法上限。

### 3. 反向幻觉约束加强 (配合 RT-004 的脚本底座)
*   **Commit ID**: `a3d6b67` 还有其后的 `1fb1a52` 系列探针式修复
*   **主要波及文件**: 
    *   `scripts/archive-manager.py` 和 `SKILL.md`
*   **说明**: 提出了“附件必达”政策以防系统虚空造纸，并通过强制 Frontmatter (`date:`注入) 为 RT-006 要求的多维时间快照补上最后一块盲区拼图。

---
*追溯提示：RT-006 与 RT-004 (脚本承载层) 是高度藕合互生的，所以它们的 Git Commits 互相交织，但最终共同撑起了一个稳健、可追溯的 ARC Reactor v4 代生态结构。*
