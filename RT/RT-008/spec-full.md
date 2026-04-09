# RT-008 Spec Full: 自动化知识周报系统 (Weekly Executive Brief)

## 📌 1. 业务愿景
将 ARC Reactor 从一个“按需检索”的百科全书，进化为一个**“主动推送洞察”**的私人智库。通过对过去 7 天的 `Ingest` 产出进行聚合分析，生成高维度的周报，帮助主人快速掌握近期关注点的演进。

## 🎯 2. 技术规格

### 2.1 聚合引擎 `scripts/weekly-reporter.py`
一个新的 Python 组件，专门负责横向切片。
- **扫描逻辑**：读取 `arc-reactor-doc/wiki/sources/`，根据目录名（YYYY-MM-DD）筛选出最近 N 天（默认 7 天）的文件。
- **元数据提取**：从每个 `.md` 文件的 Frontmatter 中提取 `title`, `date`, `tags` 和 `sources`。
- **内容精炼**：提取每篇 Source 的核心摘要或前 200 字作为素材池。
- **工作流分派**：通过 `arc-reactor-config.yaml` 调取 `query_medium` 模型（如 Claude-3.5-Sonnet）进行交叉总结。

### 2.2 输出模板规范
周报应包含以下章节：
1. **[本周地图]**：列出本周收录的所有话题清单。
2. **[核心趋势分析]**：Agent 自行发现不同文章间的关联，提出本周的研究趋势。
3. **[实体库增量]**：本周新增或重点更新了哪些 Entity 卡片。
4. **[行动建议]**：基于库中现状，建议主人下周关注哪个缺失的领域。

## 🛠️ 3. 修改范围
- **[NEW]** `scripts/weekly-reporter.py`
- **[MODIFY]** `SKILL.md`: 增加 `Weekly` 命令引导。
- **[MODIFY]** `arc-reactor-config.yaml`: 增加 `weekly_report` 配置段。

## 📜 4. 验证标准
- **输入**：`python3 scripts/weekly-reporter.py --days 7`
- **输出**：在终端打印出格式完美的 Markdown 周报，且生成的 JSON 审计回执包含 `content_aggregated_count` 字段。
- **异常处理**：若过去 7 天没有任何更新，脚本应优雅地提示“本周暂无新增，休息一下吧”。

---
最后更新: 2026-04-09
