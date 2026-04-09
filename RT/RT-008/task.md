# RT-008: 自动化知识周报系统 Task Tracker

- [x] 1. 开发聚合脚本 `scripts/weekly-reporter.py`
    - [x] 1.1 时间窗筛选：支持 `--days` 参数，过滤 `wiki/sources/YYYY-MM-DD`
    - [x] 1.2 文本聚合：批量读取命中文件的 Frontmatter 和正文摘要
    - [x] 1.3 LLM 协同：构建周报生成 Prompt，根据汇总素材产生洞察
    - [x] 1.4 回执输出：生成包含聚合详情的 JSON 审计回执
- [x] 2. 更新 `SKILL.md` 指令
    - [x] 2.1 增加 `Weekly` 命令引导示例
- [x] 3. 增强 `arc-reactor-config.yaml`  配置项
    - [x] 3.1 预埋周报生成使用的模型配置 `weekly_generator`
- [x] 4. 测试与验证
    - [x] 4.1 模拟不同时间跨度的文件，验证聚合逻辑的鲁棒性
    - [x] 4.2 验证无内容时的优雅提示逻辑
