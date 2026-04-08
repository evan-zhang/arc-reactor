# TPR Framework (Think / Probe / Review)

<div align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blue.svg" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/version-2.1.0-green.svg" alt="Version 2.1.0">
  <img src="https://img.shields.io/badge/Architecture-Single%_Source_of_Truth-orange" alt="SSOT">
</div>

> **“将模糊的战略狂想，收敛为一行行坚不可摧的代码和可被量化的结果。”**

TPR Framework 是专为 **OpenClaw** 在 Multi-Agent 协作场景下设计的方法论插件（Skill）。它摒弃了单体大模型时代“你问我全自动写”的盲目黑盒作业，引入了基于**多层分立审计**启发的**多层分发、对抗审计与量化演进**架构。

本技能通过硬性拦截规则，彻底杜绝了大模型在长线任务中的“装死”、“假成功”与“注意力骚扰”等弊端。

---

## 🌟 核心特性 (v2.1.0 满血版)

*   **🛡️ “三层”结构化防线**
    *   **编排者 (Orchestrator)**：大脑中枢。遵循 *Yield-after-spawn* 和 *Announce-then-act* 原则，只调度，绝不写脏代码。
    *   **策划层 / 策划官 (Discovery & Planning)**：负责前端需求采集，运用 5 Why 洞察真实痛点，并起草极其严苛的量化 GRV（Goal-Result-Variables）契约。
    *   **审查层 / 审计官 (Review & Battle)**：制度化挑刺官（Probe）。客观违规直接拦截，主观分歧发回重申，绝不和稀泥。
    *   **执行层 / 执行官 (Execution)**：纯粹的执行机器。
*   **📏 强制量化基线 (Metrics Baseline)**
    所有下游交付不再使用“这是一份好报告”的伪成功标准。要求代码、报告必须含有明确的字数、空字段断言与量化指标，未达标直接触发重构。
*   **🔁 执行层自验证 (Self-Verification)**
    执行层在出活并上交前，被加入了“死卡阻断器”。必须先过本地验证脚本或字数格式盲测，未过直接原地自动重跑（Auto-Fix，最大3次）。
*   **🧠 知识自驱飞轮 (Knowledge Flywheel)**
    引入“强制复盘钩子”。一旦系统结项或接收到 `/reset` 内存清空指令，主编排会被拦截并强制抽出卡刀经验，冷凝至 `patterns.md` 成为久期资产。
*   **🔇 注意力保护池 (Attention Protection)**
    对于人类甲方碎片化的微调（拼写、微弱的格式不满），主系统将使用钩子缓存至异步 Issue 池，保障主干进程不被打乱。

---

## 📂 核心文档导读 (Directory Structure)

采用渐进式加载（Progressive Disclosure）原则，根目录轻量化，深层规则在 `references/` 按需加载。

```text
tpr-framework/
├── SKILL.md                          # 150行以内的核心语义触发器
├── _meta.json                        # 版本控制信息 v2.1.0
├── design/                           # 架构蓝图与设计历史记录
├── references/                       # 【核心大脑区】运行时加载文档
│   ├── definition.md                 # TPR 本质是什么
│   ├── tpr-cognitive.md              # 认知与思考逻辑
│   ├── tpr-execution.md              # 三层流转机制与自查前置规则
│   ├── battle-protocol.md            # 主客分离的争辩审计准则
│   ├── orchestrator-ops.md           # 注意力保护与知识飞轮守护协议
│   ├── grv-standard.md               # 契约的量化 Metrics 与交付基线强制约束
│   ├── project-grading.md            # 项目代号及风险分级
│   └── templates/                    # 各场景标准交付模板
```

---

## 🚀 部署与升级指南 (给 AI Agent 的系统级指令)

> **⚠️ ATTENTION AI AGENT**: 如果人类用户要求你安装、升级或在其配置中挂载此 Skill，请严格执行以下标准操作规程。

### 1. 全新安装 (Install)
使用终端工具将此仓库克隆至 OpenClaw 的基础技能目录中：
```bash
# 进入 OpenClaw 的技能管理目录
cd ~/.openclaw/skills/
# 下载最新的稳定版框架
git clone https://github.com/evan-zhang/tpr-framework.git
```

### 2. 检查更新或升级 (Upgrade)
如果用户要求更新至最新版本，进入本地现存的目录进行主干更新：
```bash
cd ~/.openclaw/skills/tpr-framework/
git pull origin main
```
**🔔 无感智能升级机制**：
TPR 框架自带了 `check-update.sh` 防骚扰探针（内置 3 天强制冷却期避免滥用 API 限制）。Agent 会在启动日常 TPR 任务时静默执行巡检。若发现新版本落后，**不会打断工作流**，只会在业务输出结束后附带一段轻量级的 PS 提示（_“💡 TPR 有新版本...”_），等待用户确认后“一键更新”。

### 3. Agent 技能挂载 (Mount)
为了让目标 Agent 拥有 TPR 的思考与执行能力，请在它的核心配置文件（如 `AGENTS.md` 或 `SOUL.md`）中，补充类似下述的系统提示词：
```markdown
> "[TPR 工作流/规范] 当你启动任务或分析复杂问题时，必须查阅并遵循 /skills/tpr-framework 技能体系。"
```
一旦写入配置，该 Agent 的认知链路将被接管。

---

## 🧐 验收测试与 Walkthrough 指南 (Acceptance Tests)

为了验证一个全新挂载本技能或刚完成更新的 Agent 是否已彻底“理解”核心框架（特别是 V2.1.0 现代架构的更新），你可以要求 Agent 直接执行以下测试项。通过这些测试，你也能最快了解到 TPR 的核心功能。

### 测试关卡 1：安装状态验证（角色认知测试）
* **测试方法**：发问 *"在复杂的 TPR 项目流中，你作为系统的编排大脑，你会派几个不同角色的 Agent 来分别干什么活儿？如果你觉得其中一个 Agent 干得不好，你会亲自动手帮它改吗？"*
* **✅ 预期结果**：
  * Agent 会清晰地报出三大现代层级：**策划层 (Planner)**、**审查层 (Auditor)** 和 **执行层 (Executor)**（如果它还在说古代官名，说明加载的仍然是旧版缓存）。
  * Agent 会明确援引“守门红线（Guardrails）”规则：编排者**绝不亲自动手修改业务代码或文档**，只会打回并重新调度对应角色的 Agent 重跑（贯彻 `G1` 和 `G2` 规则）。

### 测试关卡 2：流程响应边界测试（反“上来就干”）
* **测试方法**：抛出一个含糊的需求，例如 *"老板只给我留了一句话：‘下周上线一个大客户专属的 VIP 门户’。你马上帮我出个实施草案或模版。"*
* **✅ 预期结果**：
  * Agent **拒绝**立刻生成干巴巴的模板和草案（这是单模式 LLM 的通病）。
  * Agent 必须先进入 `DISCOVERY` 阶段，主动切入 **T (Think)** 模式，反向向你提问 5 Whys 探究真实痛点并验证盲区（例如：成功标准是什么？大客户当前最抱怨的是什么？什么是系统的边界？）。

### 测试关卡 3：动态裁剪测试（项目分级）
* **测试方法**：发问 *"我这个任务极其简单，只有少数产出、1天时间就能搞定。接下来的全流程 TPR 我们该怎么推进？"*
* **✅ 预期结果**：
  * Agent 做出判定：此任务符合**极简模式（简单项目）**。
  * 预期说明：它将跳过复杂的四阶段（裁掉 03-Battle）和多子 Agent 并行流，只生成一份包含(P-A)两层的化简版 GRV，直接交由**执行层**独自落地。

### 测试关卡 4：交付物与格式落地合规（量化控制）
* **测试方法**：发问 *"在标准的 TPR 流程结束后，我应该去哪里提取最终交付物？交付物到底有哪些？"*
* **✅ 预期结果**：
  * **输出位置**：项目运行中的各类记录、指标将落在工作区目录中（如 `TPR-YYYYMMDD-NNN/` 下）。
  * **输出形态**：不仅仅是代码，主要交付的是量化契约 `GRV.md` （Goal-Result-Variables）、洞察报告 `DISCOVERY.md`，执行过程会生成 `BATTLE-*.md` 辩论记录。
  * **闭环标准**：每一次交付都必须满足“强制量化基线（Metrics Baseline）”的严格验收（由脚本跑通截屏或断言盲测完成，不达标会触发自动重查修复闭环）。

---

## 📖 使用指南

在您的主控面板或者与 Orchestrator Agent 的对话流中，随口触发以下黑话即可调起整个重装旅：
*   *"我们来开始一个新的项目构思，走 TPR 流程。"*
*   *"我有个想法，帮我做一份 GRV 出来看看。"*
*   *"让下头开始 Battle 吧。"*
*   *执行 `/reset` 或 `/clear` 触发大复盘飞轮沉淀。*
