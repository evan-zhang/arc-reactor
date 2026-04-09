# RT-009: 冲突对撞机 (Conflict Collider) Task Tracker

- [ ] 1. 开发探测核心 `scripts/conflict-collider.py`
    - [ ] 1.1 输入拦截：获取 Ingest 流和对应目录下的旧实体文件
    - [ ] 1.2 构造 Critic Prompt：定义对撞审查的对比维度
    - [ ] 1.3 冲突预警格式化：定义 `[CONFLICT_ALERT]` 的结构化输出
- [ ] 2. 深度集成
    - [ ] 2.1 修改 `archive-manager.py` 在写入前执行对撞预检
    - [ ] 2.2 在 `SKILL.md` 中增加冲突响应的 SOP 指令
- [ ] 3. 测试与验证
    - [ ] 3.1 编写对撞单元测试用例
