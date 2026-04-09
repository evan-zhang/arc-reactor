# RT-007 Spec Full: 动态潜意识注入系统 (Dynamic Context Hook)

## 📌 1. 业务目标
实现真正的 Compilation over Retrieval（编译优于检索）的下半场：**随用随取无缝接入**。
当用户向拥有此挂件的 Agent 发送日常对话时，系统会在千分之一秒内扫描私人字典（`wiki/index.md`），发现命中词汇后，将相关私有 Markdown 实体文本静默贴注在上下文前方，使 LLM 零门槛获得个人知识库加持。

## 🔬 2. 技术路线选型 (决策结果)

**选型评估：**
* **路线 A (网关中间件侵入)**: 修改 OpenClaw 底层源码，拦截每次 Prompt 前置处理。极其重度，不利于生态解耦。
* **路线 B (极简轻量挂件 - 本期采用)**: 在 `arc-reactor` 技能域内，新增一个轻量探针脚本 `scripts/context-injector.py`。
* **决策结论**: 采用路线 B。作为 ARC 技能特有的 Pre-flight Check 工具，完全不破坏 OpenClaw 基建结构。

## 🛠️ 3. 系统架构与修改范围

### 3.1 探针引擎 `scripts/context-injector.py`
开发一个本地关联读取器脚本。
*   **输入**: 被拦截的用户当前聊天 Query 字符串，或环境上下文内容。
*   **处理逻辑**:
    1.  正则定位解析 `arc-reactor-doc/wiki/index.md` 的词条。
    2.  与输入 Query 字符串进行交叉匹配（关键词匹配或分词比中）。
    3.  若命中，利用并发 / 顺序 I/O 读取 `wiki/entities/` 目录下的命中文件全文。
    4.  组装结果并以包裹块输出。
*   **输出控制**: `<ARC_KNOWLEDGE_CONTEXT> ...被命中的实体文件全文... </ARC_KNOWLEDGE_CONTEXT>`

### 3.2 技能说明书大整改 (`SKILL.md`)
更新系统级指令框架：
定义一个新的 **Pre-flight Hook (起飞前置入模式)**。强制规定相关的 Worker Agent 在进行深度任务推理前，必须优先针对用户的输入执行一轮 `context-injector.py --query "[用户输入]"`。

### 3.3 配置文件升级 (`arc-reactor-config.yaml`)
新增对预读取链路的控制参数，防范上下文爆破：
```yaml
features:
  context_injection:
    enabled: true
    max_entities_fetch: 3  # 最多一次连同注入几张卡片，防止打爆 Token
```

## 📜 4. 验证与验收标准
- **环境**: 在 OpenClaw 某具有上下文读取能力的新 Agent 中安装 ARC v4.X。
- **输入**: 向其发出不带背景说明的要求：“参考我们之前关于 SkillsBench 的结论，帮我分析新版库”。
- **验收**: Agent 未触发网络外搜，仅凭 `context-injector.py` 查杀，成功提取到 `entities/` 内部的 Markdown 并做出带有精确引用的回答。

---
最后更新: 2026-04-09
