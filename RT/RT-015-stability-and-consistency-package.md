# RT-015: Stability & Consistency Package (Audit Remediation)

## 1. 简介 (Introduction)
本项目在多 Agent 协作审计中被识别出多项 P0-P5 级的稳定性与一致性缺陷。本规约旨在系统性修复这些问题，确保项目在发布、开发和知识归档维度的健康。

## 2. 修复项 (Remediation Items)

### 2.1 版本与发布 (P4)
- **动作**：将 `skills/arc-reactor/_meta.json` 里的版本号更新为 `4.2.0`。
- **目标**：解决打包 ZIP 文件与实际开发版本的不匹配问题。

### 2.2 索引与治理一致性 (P1, P2)
- **动作 1**：补齐 `RT/index.yaml` 中缺失的 `RT-003` 条目，并更新 `RT-009` 的完成状态。
- **动作 2**：统一 `CONTRIBUTING.md` 中的分支策略。明确 AI Agent 必须使用 **“主分支原子化提交 (Strict-Main)”** 模式，废弃 feature branch 以防止状态漂移。

### 2.3 归档工具路径加固 (P5)
- **动作**：在 `archive-manager.py` 的动态导入逻辑中，显式将脚本所在目录加入 `sys.path`。
- **目标**：确保在工作空间根目录运行脚本时不会触发 `ImportError`。

### 2.4 知识库清理 (P0, P3)
- **动作 1**：清理 `log.md` 中的链接误报（包裹在代码块中）。
- **动作 2**：扫描并移除已知的空文件/异常素材。

## 3. 验证计划 (Verification Plan)
- [x] 执行 `git add .` 后运行 `python3 skills/arc-reactor/scripts/governance-audit.py`。
- [x] 执行 `bash verify-v42.sh` 确保核心流程不受影响。

---
*Verified and enforced by Antigravity (Senior Architect)*
