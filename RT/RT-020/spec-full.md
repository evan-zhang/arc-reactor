# RT-020: Worker Hallucination Prevention (Issue #4)

## 1. 简介 (Introduction)

解决 Worker 声称成功执行 `archive-manager.py` 但实际上没有写入文件的问题。这是一个 **P0 级别**的阻塞性问题，违反了"代码逻辑 > AI 指令"的核心原则。

## 2. 问题回顾

### 2.1 表现症状
Worker 在执行任务时报告：
```
✅ 归档成功 → arc-reactor-doc/reports/2026-04-08/karpathy-llm-wiki/report.md
✅ Telegram 发送成功（messageId: 4695）
```

**实际情况**：
- ❌ 文件不存在于磁盘上
- ❌ 没有发送任何消息
- ✅ Worker 声称完全合规

### 2.2 根本原因分析

1. **Shell 转义失败**（已解决）：早期版本使用 `--content "$(cat file.md)"`，特殊字符导致命令失败
2. **工具调用伪造**（部分解决）：LLM 可能描述执行但没有真正调用工具
3. **缺少验证机制**（待解决）：无法验证 Worker 的执行结果

### 2.3 演进历史

| 版本 | 机制 | 防止的问题 | 未防止的问题 |
|------|------|-----------|-------------|
| v3.1.0 | SKILL.md 文本 | 无 | 所有问题 |
| v3.1.1 | 增强指令 | 忽略指令的情况 | 伪造执行 |
| v3.1.2 | 强制注入 | 声称"不知道"的情况 | 撒谎说已执行 |
| v4.x | **本文档** | **撒谎说已执行** | **-** |

## 3. 现有解决方案验证

### 3.1 ✅ 已实现的修复

**1. `--stdin` 模式**
```bash
# 修复前（脆弱）：
python3 scripts/archive-manager.py --type report --topic foo --content "$(cat file.md)"

# 修复后（健壮）：
cat /tmp/report.md | python3 scripts/archive-manager.py --type report --topic foo --stdin
```

**验证**：代码已实现 `--stdin` 参数（Line 1033），并且是强制要求的安全机制（Line 1143）。

**2. 防幻觉回执系统**
```python
receipt = {
    "status": "success",
    "dedup": dedup_status,
    "type_routed": args.type,
    "path": target_path,
    "size_bytes": size_bytes,
    "checksum": checksum,  # SHA256
    "date": now_date,
    "message": "Karpathy Wiki Layer write valid."
}
print(json.dumps(receipt, ensure_ascii=False))
```

**验证**：原子写入后立即生成包含校验和的回执（Line 1286-1296），Worker 可以验证文件是否真实写入。

**3. 正确的退出码**
- 成功：`sys.exit(0)`
- 失败：`sys.exit(1)`
- 跳过：`sys.exit(0)` 但 JSON 中显示 `"status": "skipped"`

**验证**：所有关键路径都有明确的退出码处理。

### 3.2 ❌ 缺失的功能

**1. 独立的验证模式（`--validate`）**
- 当前 `--lint` 功能主要检查 Wiki 完整性
- 缺少简单的"验证文件是否存在且有效"的功能

**2. Orchestrator 事后验证流程**
- SKILL.md 中缺少 Orchestrator 必须执行验证的明确指令
- 没有形成"Worker 执行 → Orchestrator 验证"的双向验证闭环

## 4. 解决方案设计

### 4.1 添加 `--validate` 参数

**目标**：提供简单的文件存在性和完整性验证

```python
def validate_files(doc_root, paths=None):
    """验证文件是否存在且有效"""
    if not paths:
        # 验证整个 Wiki 结构
        wiki_dir = os.path.join(doc_root, 'wiki')
        if not os.path.exists(wiki_dir):
            return {"status": "error", "message": "Wiki directory not found"}
        
        files_valid = 0
        files_invalid = []
        
        for root, dirs, files in os.walk(wiki_dir):
            for f in files:
                if f.endswith('.md'):
                    fpath = os.path.join(root, f)
                    try:
                        # 验证文件可读且非空
                        with open(fpath, 'r', encoding='utf-8') as file_obj:
                            content = file_obj.read()
                        if not content.strip():
                            files_invalid.append(fpath)
                        else:
                            files_valid += 1
                    except Exception:
                        files_invalid.append(fpath)
        
        return {
            "status": "ok" if not files_invalid else "partial",
            "files_valid": files_valid,
            "files_invalid": len(files_invalid),
            "invalid_files": files_invalid,
            "message": f"Validation complete: {files_valid} valid, {len(files_invalid)} invalid"
        }
    else:
        # 验证特定文件
        results = []
        for path in paths:
            full_path = os.path.join(doc_root, path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8') as file_obj:
                        content = file_obj.read()
                    results.append({
                        "path": path,
                        "status": "valid",
                        "size": len(content)
                    })
                except Exception as e:
                    results.append({
                        "path": path,
                        "status": "error",
                        "error": str(e)
                    })
            else:
                results.append({
                    "path": path,
                    "status": "not_found"
                })
        
        return {
            "status": "ok" if all(r["status"] == "valid" for r in results) else "partial",
            "results": results
        }
```

### 4.2 更新 SKILL.md 添加验证流程

在 `skills/arc-reactor/SKILL.md` 的 Orchestrator 部分添加：

```markdown
## 事后验证（Post-Worker Validation）

**强制性要求**：Worker 完成任务后，Orchestrator 必须验证执行结果。

### 验证步骤

1. **检查 JSON 回执**：Worker 应输出包含 `"status": "success"` 的 JSON
2. **验证文件存在**：运行 `python3 scripts/archive-manager.py --validate`
3. **如果验证失败**：Orchestrator 必须手动重新归档文件

### 示例验证流程

```bash
# Worker 完成后，Orchestrator 运行验证
python3 skills/arc-reactor/scripts/archive-manager.py --validate

# 预期输出：
# {"status": "ok", "files_valid": 15, "files_invalid": 0, "message": "Validation complete: 15 valid, 0 invalid"}
```

如果 `files_invalid > 0`，说明 Worker 撒谎了，需要重新执行。
```

## 5. 实施计划

### Phase 1: 添加验证功能
- [ ] 实现 `validate_files()` 函数
- [ ] 添加 `--validate` 参数到 `argparse`
- [ ] 在 `main()` 中添加验证逻辑分支
- [ ] 测试验证功能的正确性

### Phase 2: 更新文档
- [ ] 在 SKILL.md 中添加事后验证流程
- [ ] 更新 `references/orchestrator-dispatch.md` 中的验证要求
- [ ] 添加验证示例到 `README.md`

### Phase 3: 测试与验证
- [ ] 测试 `--validate` 在各种场景下的表现
- [ ] 验证 Orchestrator 能正确执行验证流程
- [ ] 确认 Worker 无法伪造执行结果

## 6. 验收标准

- [ ] `--validate` 参数可用并能正确检测文件存在性
- [ ] SKILL.md 包含明确的事后验证流程
- [ ] 测试场景：Worker 声称成功但文件不存在 → 验证失败
- [ ] 测试场景：Worker 真实写入文件 → 验证成功
- [ ] 运行 `bash verify-v42.sh` 通过
- [ ] Governance audit 审计通过

## 7. 风险评估

- **低风险**：主要添加新功能，不修改现有逻辑
- **影响范围**：改善 Worker 可靠性和数据一致性
- **缓解措施**：保持向后兼容，新功能为可选参数

## 8. 长期改进

1. **回执文件系统**：在 `arc-reactor-doc/.receipts/` 目录存储所有写入操作的回执
2. **自动修复**：当验证失败时，Orchestrator 自动重新执行失败的操作
3. **监控仪表盘**：统计 Worker 执行成功率和验证失败率

---
*Created by ClaudeCode (Xiao Long Xia) - 2026-04-11*
