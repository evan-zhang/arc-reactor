# Obsidian 同步调度器

## 配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `vault_path` | `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/` | Obsidian 仓库根目录 |
| `target_dir` | `github分享/AI调研/{date}/` | 按日期归档目录 |
| `auto_sync` | `true` | 报告完成后自动同步 |

## 同步规则

1. 报告完成后，自动复制到 Obsidian 目标目录
2. `{date}` 替换为实际日期 `YYYY-MM-DD`
3. 确保目标目录存在（不存在则自动创建）
4. 同步后在报告末尾追加 `同步状态: ✅ Obsidian`

## 扩展接口

未来新增存储目标只需在 `dispatchers/` 下新建配置文件，实现：
- `dispatch(report_path, config)` → 将报告发送到目标位置
