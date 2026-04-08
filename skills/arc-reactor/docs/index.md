# OpenClaw 文档中心

> 统一的文档管理和索引系统
> 最后更新：2026/2/21

---

## 📊 统计

- **总文档数**: 6
- **涉及 Agents**: 1
- **主题分类**: 5
- **总大小**: 57KB

---

## 📂 按主题分类

### Model Management

#### 智能模型容灾降级系统

**文档 ID**: `model-disaster-recovery-system`
**Agent**: assistant-agent
**状态**: ✅ 已完成
**标签**: model, fallback, disaster-recovery, agent-integration

**概述**:
完整的模型容灾降级系统，支持智能错误分类、差异化降级策略、自动恢复机制。包含 7 个 agents 的完整集成。

**文件**:
1. `MODEL_MANAGER.md`
   - 详细设计文档，包含错误分类、降级逻辑、状态管理
2. `README-MODEL-SYSTEM.md`
   - 系统用户指南，包含快速开始和监控命令
3. `INTEGRATION-GUIDE.md`
   - Agent 集成指南，如何将系统集成到各个 agent
4. `AGENT_INTEGRATION_COMPLETE.md`
   - 集成完成报告，所有 agents 的配置状态
5. `INTEGRATION_REPORT.md`
   - 集成工作报告，包含完成情况和使用方法

**位置**: `agents/assistant-agent/model-disaster-recovery/`
**更新时间**: 2026/2/21

---

### Discord Operations

#### Discord 文件发送经验总结

**文档 ID**: `discord-file-sending-lessons`
**Agent**: assistant-agent
**状态**: ✅ 已完成
**标签**: discord, file-sending, best-practices, lessons

**概述**:
在 Discord 中通过 OpenClaw message 工具发送文件的经验总结，包含正确的 target 格式、文件路径设置、media 参数使用等关键经验。

**文件**:
1. `discord-file-sending-lessons.md`
   - Discord 文件发送最佳实践，包含问题原因、解决方案、最佳实践模板

**位置**: `lessons/discord-file-sending-lessons.md`
**更新时间**: 2026/2/21

---

### Configuration

#### API Keys 配置清单

**文档 ID**: `api-keys-checklist`
**Agent**: assistant-agent
**状态**: ✅ 已完成
**标签**: api-keys, configuration, checklist, setup

**概述**:
OpenClaw 系统所需的 API Keys 完整清单，包括当前已配置的 API Keys、缺少的关键 API Keys、优先级排序、配置步骤和验证方法。

**文件**:
1. `API_KEYS_CHECKLIST.md`
   - 统一的 API Key 管理清单，包含当前配置状态和需要配置的 API Keys

**位置**: `API_KEYS_CHECKLIST.md`
**更新时间**: 2026/2/21

---

### Models

#### 当前支持的大模型

**文档 ID**: `supported-models`
**Agent**: assistant-agent
**状态**: ✅ 已完成
**标签**: models, llm, availability, testing

**概述**:
当前系统支持的 20 个大模型的完整列表，包括模型 ID、提供商、用途分类、Agent 分配和特殊配置。

**文件**:
1. `SUPPORTED_MODELS.md`
   - 当前系统支持的所有大模型列表，按提供商、用途分类

**位置**: `SUPPORTED_MODELS.md`
**更新时间**: 2026/2/21

---

#### 大模型可用性总结

**文档 ID**: `model-availability-summary`
**Agent**: assistant-agent
**状态**: ✅ 已完成
**标签**: models, availability, testing, summary

**概述**:
基于现有配置和测试结果的大模型可用性总结，区分已验证可用（7个）、配置了但可能有限制（7个）、可能需要额外配置（2个）的模型。包含 OpenAI Codex、MiniMax、GLM、Google、Amazon Bedrock 等提供商的模型。

**文件**:
1. `MODEL_AVAILABILITY_SUMMARY.md`
   - 大模型可用性总结，基于现有配置和测试结果，区分已验证可用、配置了但有限制、可能需要额外配置的模型

**位置**: `MODEL_AVAILABILITY_SUMMARY.md`
**更新时间**: 2026/2/21

---

