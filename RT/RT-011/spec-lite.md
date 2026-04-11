# RT-011: Entity Export Feature

## 1. 简介 (Introduction)
为了方便知识分享和便携式查阅，本项目增加“实体导出”功能。该功能可将单个实体（Entity/Concept）与其关联的原始素材（Sources）及相关实体（Related Entities）打包成一个独立的、自包含的 Markdown 文档。

## 2. 功能规范 (Functional Specification)

### 2.1 CLI 接口
- **命令**：`python3 scripts/archive-manager.py --export-entity [TOPIC]`
- **参数**：
    - `--export-entity`: 指定要导出的实体名或 Topic。
    - `--include-related`: (可选) 是否包含关联实体，默认为 true。
    - `--output-dir`: (可选) 导出文件的存放目录，默认为 `exports/`。

### 2.2 导出逻辑 (Processing Logic)
1. **实体解析**：在 `wiki/entities/` 或 `wiki/concepts/` 中定位目标 Markdown 文件。
2. **连接发现**：
    - **关联实体**：解析正文中的所有 `[[wiki-links]]`。
    - **关联素材**：
        - 读取 Frontmatter 中的 `sources` 列表并定位文件。
        - 使用 `grep` 扫描 `wiki/sources/` 目录，找出所有出现过 `[[Topic]]` 的文件作为反向链接来源。
3. **内容聚合**：
    - 生成统一的 Header（含导出时间、Wiki 标识）。
    - 嵌入实体正文。
    - 嵌入所有关联实体的详细内容。
    - 嵌入所有关联素材的全文。

### 2.3 导出格式
输出文件为单一 Markdown，结构如下：
- # [Topic] — Knowledge Export
- ## Overview (Entity Content)
- ## Connections (Related Entities)
- ## Origins (Source Materials)

## 3. 约束 (Constraints)
- **递归深度**：仅导出 Level-1 的关联项，防止过度膨胀。
- **环境要求**：支持 BSD/GNU `grep` 以进行快速反向搜索。
- **依赖性**：仅使用 Python 标准库实现文件合并。
