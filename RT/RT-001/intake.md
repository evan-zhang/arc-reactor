# RT-001: TPR Framework 统一管理 (Intake)

## 原始描述
建立 TPR Framework（Think / Probe / Review）这一核心 Skill 的统一管理阵地。本 RT 是该 Skill 的全生命周期归档中心，涵盖架构设计记录、版本发布追踪、持续维护演进等全部工作。

## 目标
1. 将 TPR Framework 的设计心智（三省六部制、编排者核心定位、量化基线等）以正规 AODW 文档体系固化。
2. 集中管理所有发行版本产物（tarball），避免散落在工作区根目录造成污染。
3. 作为后续任何与 TPR Framework 相关的修复、增强、重构的唯一入口。

## 概要估算
- **需求类型**: Enhancement / Maintenance
- **开发范围**: Skill 级别，主要涉及 `skills/tpr-framework/` 与本 RT 目录
- **风险等级**: 低风险
- **影响模块**: `tpr-framework`
- **开发类型**: Spec-Lite
- **远程仓库**: `https://github.com/evan-zhang/tpr-framework.git`
