# ARC Reactor Changelog

## [1.0.0] - 2026-04-08
### Added
- 初始化 ARC Reactor Skill
- 引入 Acquire / Research / Catalogue 三阶段核心管线
- 新增去重检测机制（三级匹配）与自动合并模式
- 新增二次复检管线，包含声明分类与可信度交叉验证
- 新增知识编译引擎（借鉴 Karpathy LLM Wiki，实现实体/概念提取与增量式演进）
- 新增 Markdown 调研报告统一模板
- 新增 Obsidian 导出调度器配置

### Changed
- 从 `chat-main-agent` 的 `AGENTS.md` 抽离并删除硬编码的调研 SOP，替换为对 ARC Skill 的引用
