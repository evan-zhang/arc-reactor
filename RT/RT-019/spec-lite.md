# RT-019: Archive Manager Path Fix Verification (Issue #7)

## 1. 简介 (Introduction)

验证和确认 `archive-manager.py` 的路径修复功能，确保从任何目录调用脚本都能正确写入到 workspace root 的 `arc-reactor-doc/` 目录，而不是写入到 skill 目录内部。

## 2. 问题回顾

Issue #7 描述的问题：
- 当 worker `cd` 进入 `skills/arc-reactor/` 目录后调用脚本
- 文件会被写入到 `skills/arc-reactor/arc-reactor-doc/`（错误位置）
- 而不是 `workspace/arc-reactor-doc/`（正确位置）
- 这会导致"split-brain"知识库问题

## 3. 现有解决方案验证

经过代码审查和实际测试，确认 **Issue #7 已经被修复**：

### 3.1 现有的 `find_doc_root()` 函数

```python
def find_doc_root(start_path, root_name='arc-reactor-doc'):
    """Walk up from start_path to find the workspace root."""
    curr_dir = start_path
    while curr_dir and curr_dir != '/':
        if os.path.exists(os.path.join(curr_dir, root_name)):
            return os.path.join(curr_dir, root_name)
        if os.path.exists(os.path.join(curr_dir, '.git')):
            return os.path.join(curr_dir, root_name)
        curr_dir = os.path.dirname(curr_dir)
    return os.path.join(start_path, root_name)
```

这个函数实现了 **Option B（自动检测 workspace root）** 的方案，会向上查找包含：
- `arc-reactor-doc/` 目录，或
- `.git/` 目录

### 3.2 正确使用 `find_doc_root()` 的位置

在 `main()` 函数中，所有需要路径的地方都正确使用了 `find_doc_root()`：

```python
# Line 1082: export_entity
cwd = os.getcwd()
doc_root = find_doc_root(cwd, args.root)

# Line 1095: lint mode
cwd = os.getcwd()
doc_root = find_doc_root(cwd, args.root)

# Line 1152: normal archive mode
cwd = os.getcwd()
doc_root = find_doc_root(cwd, args.root)
```

## 4. 实际验证测试

### 测试 1：从 workspace root 调用
```bash
cd /Users/evan/arc-reactor/arc-reactor
echo "测试内容" | python3 skills/arc-reactor/scripts/archive-manager.py \
  --type source --topic "test-path-fix" --root "arc-reactor-doc" --stdin
```

**结果**：✅ 文件写入到 `/Users/evan/arc-reactor/arc-reactor/arc-reactor-doc/wiki/sources/2026-04-11/test-path-fix.md`

### 测试 2：从 skill 目录调用
```bash
cd skills/arc-reactor
echo "测试内容" | python3 scripts/archive-manager.py \
  --type source --topic "test-from-skill-dir" --root "arc-reactor-doc" --stdin
```

**结果**：✅ 文件同样写入到 `/Users/evan/arc-reactor/arc-reactor/arc-reactor-doc/wiki/sources/2026-04-11/test-from-skill-dir.md`

### 测试 3：确认没有错误位置的文件
```bash
find skills/arc-reactor -name "test-path-fix.md" -o -name "test-from-skill-dir.md"
```

**结果**：✅ 没有在 skill 目录内找到任何文件

## 5. 验收标准

- [x] 确认 `find_doc_root()` 函数已实现并正常工作
- [x] 确认所有调用点正确使用了 `find_doc_root()`
- [x] 从 workspace root 调用脚本，文件写入正确位置
- [x] 从 skill 目录调用脚本，文件仍写入正确位置
- [x] 确认没有文件被错误写入到 skill 目录内部
- [x] 运行 `bash verify-v42.sh` 验证功能完整

## 6. 结论

**Issue #7 已在之前的版本中被修复**，修复方案采用了建议的 **Option B（自动检测 workspace root）**。

该修复使得 `archive-manager.py` 变成了**位置无关**的脚本——无论从哪个目录调用，都能自动找到正确的 workspace root 并将文件写入到正确的 `arc-reactor-doc/` 目录。

这完全避免了"split-brain"知识库的问题，确保所有知识文件都统一存储在 workspace root。

## 7. 后续建议

虽然问题已修复，但建议在 `SKILL.md` 中明确说明：
- Worker 不需要 `cd` 到 skill 目录
- 可以直接从 workspace root 调用脚本
- 脚本会自动检测正确的 workspace root

这样可以进一步减少潜在的混淆。

---
*Verified by ClaudeCode (Xiao Long Xia) - 2026-04-11*
