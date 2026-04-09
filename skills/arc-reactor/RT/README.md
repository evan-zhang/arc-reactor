# OpenClaw RT (Research Ticket) 治理规范

本目录是所有研发任务（RT）的指挥与档案中心。

## 📂 核心存储原则：独立 RT = 独立仓库

为了保证每一个 Skill 的纯粹性与其开源生命周期，我们遵循以下归档原则：

1. **过程归档**：在 RT 进行期间，所有的计划库、交付文档、验收细则应存储在对应 RT 编号的文件夹下（如 `RT/RT-001/`）。
2. **仓库对齐**：当一个 RT 任务完成后，其对应的 `RT/RT-NNN` 档案应**物理迁移**至该项目对应的独立仓库中，并打上 `done-RT-NNN` 的标签。
   - **TPR Framework (RT-001)** -> 归属于 [tpr-framework](https://github.com/evan-zhang/tpr-framework.git)
   - **ARC Reactor (RT-002)** -> 归属于 [arc-reactor](https://github.com/evan-zhang/arc-reactor.git)
3. **主控保留**：`.openclaw` 作为本地主控环境，仅保留与其直接相关的（如 `arc-reactor`）或正在进行中的 RT 档案。

## 📄 参考指南
具体的跨仓库迁移与清理操作，请参考各 RT 目录下的 `REPO-MIGRATION-GUIDE.md`。
