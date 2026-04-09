# ARC Reactor 动力舱与档案室离合方案

## 最终确定的目录结构

### 1. 动力舱 (The Skill Core)
位置：`.../skills/arc-reactor/`
内容：
- `SKILL.md` (Agent 逻辑入口)
- `components/` (采集武器库：media-extractor 等)
- `meta.yaml` (版本元数据)

### 2. 档案室 (The Doc Home)
位置：与动力舱同级或位于目标根目录 `.../arc-reactor-doc/`
内容：
- `references/` (调研规则、打假管线、知识编译宪法)
- `reports/` (历史快照存档)
- `knowledge/` (实体百科 Wiki)

---

## 变更执行逻辑

### A. 物理搬家
- [CREATE] 在指定根目录下创建 `arc-reactor-doc/`。
- [MOVE] 将 `reports/`, `knowledge/`, `references/` 统一移入 `arc-reactor-doc/`。
- [CLEAN] 彻底清除 `.openclaw` 根目录下的所有上述文件夹。

### B. 逻辑自适应
- [MODIFY] **`SKILL.md`**: 
  - 更新所有参考规章的引用路径至 `./arc-reactor-doc/references/`（或动态探测路径）。
  - 明确指令：所有文件落盘必须在 `arc-reactor-doc/storage/` (或直接在 doc 根目录下)。
- [MODIFY] **`extract.py`**: 确保其临时文件 `extractor_temp` 限制在 `arc-reactor/components/media/` 内部。

### C. 环境兼容性
- **全局模式**：`~/.openclaw/arc-reactor-doc/`
- **局部模式**：`~/agent-workspace/arc-reactor-doc/`

---

## 预期效果
1. **命名空间隔离**：`arc-reactor-doc` 这个名字清晰地告诉用户：这是“我的调研文档库”。
2. **零根目录污染**：主根目录下除标准文件夹外，只有一个整洁的文档中心。
3. **备份友好**：用户可以单独 Git 自己的 `arc-reactor-doc` 仓库，而无需携带 Skill 代码。
