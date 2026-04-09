# RT-007: 动态潜意识注入系统 Task Tracker

- [x] 1. 创建探针脚本 `scripts/context-injector.py`
    - [x] 1.1 解析入参：接收用户查询 `--query`
    - [x] 1.2 检测并读取 `wiki/index.md` 寻找命中的实体
    - [x] 1.3 利用正则或关键字提取匹配的 `$Topic`
    - [x] 1.4 如果命中，提取对应的 `wiki/entities/$Topic.md` 全文
    - [x] 1.5 格式化输出为适用于 System Prompt 的 `<ARC_KNOWLEDGE_CONTEXT>` 标签包裹块
- [x] 2. 升级 `SKILL.md` 指令说明书
    - [x] 2.1 增加 `Pre-flight Check` (起飞前置入模式) 工作流说明
    - [x] 2.2 定义该机制如何介入和装载：必须要求具有查询任务的 Agent 首先自跑一遍 injector
- [x] 3. 增强 `arc-reactor-config.yaml`  配置项
    - [x] 3.1 预埋 `context_injection` 及安全拉取阈值 `max_entities_fetch` 等参数
- [x] 4. 测试与验收
    - [x] 4.1 在本地终端模拟传参检验 `context-injector.py` 对真实 `index.md` 的召回精度
    - [x] 4.2 撰写关于 Hook 使用的新说明并打包发布 
