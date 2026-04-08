# Plan-Lite: RT-001 - TPR Framework 架构归档与制度化

## 1. 修改点（Change Points）
- `/RT/RT-001/`：建立完整的 AODW 文档体系。
- `.openclaw` 根目录：清理散落的发行包。
- `.aodw-next/01-core/aodw-constitution.md`：写入强制归档铁律。

## 2. 方案描述（Solution Outline）
本项目旨在“补课”，将 `tpr-framework` 的开发心智、发布记录以及后续维护流程正式纳入 AODW-Next 管理。

### 2.1 编排者（Orchestrator）核心定义
- 明确编排者是“大脑中枢”，负责全局调度。
- 遵循 *Yield-after-spawn*（不亲自写脏活）与 *Announce-then-act*（行动前必通报）原则。
- 负责维护注意力保护池与知识进化飞轮。

### 2.2 资源重构
- 建立 `releases/` 和 `docs/` 子目录。
- 物理收编 `v2.0.0` 和 `v2.1.0` 的 tarball 产物。

## 3. 规划原件落盘制度
- 本文档即为 `implementation_plan.md` 的物理映射。
- 确立未来所有 RT 必须执行：`Platform Plan -> RT Plan` 的 1:1 转写。

## 4. 风险与注意事项（Risks & Caveats）
- 确保路径迁移不破坏已有的引用（已确认 Skill 运行时是通过解压后的目录引用，而非 tarball）。
- 需确保 AODW 规范的修改不影响其他既有流程（修正仅为增强描述性）。
