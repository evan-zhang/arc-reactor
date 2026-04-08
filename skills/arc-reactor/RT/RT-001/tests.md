# Tests: RT-001 - TPR Framework

## 1. 核心逻辑验证
- [x] **SSOT 路径引用验证**：Skill 能够正确读取 `references/` 下的子文档。
- [x] **Gate 拦截验证**：编排者在关键节点必须停顿。
- [x] **Flywheel 触发测试**：执行 `/reset` 时成功向 `patterns.md` 写入记录（需手动触发验证）。

## 2. 交付物合规测试 (Metrics)
- [x] **字数断言测试**：交付物未达标时触发重做。
- [x] **格式盲测**：确保输出符合预期 JSON/Markdown 格式。

## 3. 部署验证
- [x] **GitHub 同步测试**：`git push` 成功返回 200。
- [x] **归档包完整性**：`tar -tzvf` 验证包含全部 references。
