# RT-001: 仓库关联清单 (Repository Map)

本文件记录与 RT-001（TPR Framework）关联的所有仓库与路径，确保任何 Agent 在接手维护时能一目了然地知道"代码在哪、推到哪"。

## 1. 远程仓库 (Remote Repository)
| 字段 | 值 |
|------|---|
| **平台** | GitHub |
| **地址** | https://github.com/evan-zhang/tpr-framework.git |
| **默认分支** | main |
| **类型** | 独立仓库（Polyrepo），专门承载 tpr-framework 这一个 Skill |

## 2. 本地路径映射 (Local Path Map)

| 用途 | 路径 | 说明 |
|------|------|------|
| **Skill 运行时源** | `~/.openclaw/skills/tpr-framework/` | 全局 SSOT，所有 Agent 运行时引用此目录 |
| **GitHub 本地镜像** | `~/tpr-framework-repo/` | 用于向 GitHub 推送的独立 Git 仓库 |
| **RT 管理档案** | `~/.openclaw/RT/RT-001/` | AODW 管理区，存放设计文档与发行包 |
| **发行包存储** | `~/.openclaw/RT/RT-001/releases/` | 所有 tarball 版本的物理归档 |

## 3. 同步规则
- **修改代码** → 在 `skills/tpr-framework/` 中进行。
- **打包发布** → 压缩后存入 `RT/RT-001/releases/`。
- **推送 GitHub** → 将最新代码同步到 `~/tpr-framework-repo/` 后执行 `git push`。
- **注意**：三个位置的代码必须保持一致，任何修改后应立即同步。
