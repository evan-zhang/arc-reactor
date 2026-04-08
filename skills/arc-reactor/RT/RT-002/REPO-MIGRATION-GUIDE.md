# 跨仓库档案分离与归档完成校验报告

我们已经成功完成了 **TPR Framework (RT-001)** 与 **ARC Reactor (RT-002/003)** 的物权分离。现在两套仓库的“数字档案馆”已各归其位，互不干扰。

## 仓库 1：TPR Framework (RT-001) 主场
**仓库地址**：[evan-zhang/tpr-framework](https://github.com/evan-zhang/tpr-framework.git)  
**本地路径**：`~/tpr-framework-repo`

### 已完成动作
- [x] **档案归位**：将 `RT/RT-001/` 目录从 .openclaw 物理迁移至此。
- [x] **成果上链**：执行 `git push`，确保 GitHub 远端已同步 RT-001 的所有 Changelog、SOP、Spec 和历史版本 Tar 包。
- [x] **代码纯净度**：此仓库现在仅包含 TPR Framework 本身的代码（SKILL, references, scripts）及其对应的 RT 追踪档案。

---

## 仓库 2：ARC Reactor / .openclaw (RT-002/003) 主场
**仓库地址**：[evan-zhang/arc-reactor](https://github.com/evan-zhang/arc-reactor.git)  
**本地路径**：`~/.openclaw`

### 已完成动作
- [x] **冗余清理**：彻底删除了本仓库 master 分支下误入的 `RT/RT-001/` 文件夹。
- [x] **档案留存**：保留并更新了 `RT/RT-002` (Arc Reactor) 和 `RT/RT-003` (Media Extractor) 的档案。
- [x] **主线同步**：已将清理后的状态推送到 GitHub。现在本仓库的“项目看板”仅显示与其直接相关的任务线。

---

## 💡 验证方法
你可以随时在两个仓库的根目录下运行以下命令进行最终确认：

```bash
# 在 tpr-framework-repo 下确认
ls RT/
# 预期输出: RT-001

# 在 .openclaw 下确认
ls RT/
# 预期输出: RT-002  RT-003
```

> [!TIP]
> **关于后续开发**：
> 未来如果你要修改 TPR 框架本身的逻辑或写它的 RT 记录，请在 `tpr-framework-repo` 中进行；
> 如果是开发 ARC Reactor 的新功能或进行调研，请在 `.openclaw` 中进行。

目前档案馆已重新理顺，你的 Skill 及其对应的研发记录已经达到了生产级的整洁度。
