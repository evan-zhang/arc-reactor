# ARC Reactor v4.0 (Karpathy LLM Wiki Edition)

> **⚠️ AI-First Repository**
> This repository is designed **primarily for AI Agents**, specifically for the [OpenClaw](https://openclaw.ai) ecosystem. If you are an AI/Agent reading this, please process the `SKILL.md` as your primary entry point. Human developers are welcome to contribute, but the file structures and documentation style favor agentic cognitive ingestion.

**ARC = Acquire / Research / Compile**

全面拥抱 Andrej Karpathy 提出的 **Compilation over Retrieval (编译优于检索)** 理念。这不再是一个只会抓取链接并遗忘的搜索爬虫，而是一个全自动的、拥有永续记忆层的**私人 LLM Wiki 编译器**。

## 🎯 v4.0 终极演进特性

- 📚 **Karpathy LLM Wiki 架构**：彻底废弃流水账报告，改用 `raw/` (生肉), `sources/` (解读), `entities/` (实体卡片) 和 `index.md` (总索引) 构筑真正意义上的知识网络！
- ⏰ **双轨记账 (Time-Dimension Tracker)**：Sources 文件自带 `YYYY-MM-DD` 目录切片，且自动查杀并注入 YAML Frontmatter Date，兼顾知识的长期结晶与时间快照查询。
- 🌩️ **高并发智能调度 (Orchestrator-Worker)**：引入 `arc-reactor-config.yaml`。Ingest / Query / Lint 工作流可分别调度 `GPT-4o`、`Claude-3.5` 和 `Gemini-Flash` 等不同梯队的大脑，完美平衡智商与 Token 成本。
- 🛡️ **底层反幻觉防线**：全面启用 `--stdin` 管道数据传输脱离 Shell 限制；具备 Workspace 向上自动探测防错抓取；执行终局“附件必达”强制文件投递。

## 📦 环境配给与安装升级 (Installation & Bootstrap)

ARC Reactor 是强依赖外部基建配置的重型骨干插件。为了达成它最核心的能力，在第一次安装运行后，你可以让 Agent 为你进行**“基建环境核验”**，它会提示你准备下列组件：
1. **Google/AI 搜索引擎 Key** (用于提供给 R 阶段执行自主查杀核实) 
2. **专属第三方 Clawhub 平台防串线网络技能** (挂接获取音视频轨的底层工具)

详细引导参见：`references/env-setup.md`

### 新装 (New Installation)
在 OpenClaw 的终端或通过宿主机器直接执行克隆：

```bash
# 1. 导航至你的 Agent skills 挂载区
cd ~/.openclaw/skills/

# 2. 克隆仓库
git clone https://github.com/evan-zhang/arc-reactor.git

# 3. 让 Agent 重新加载技能
# (向你的 Agent 发信： "请重新加载你的 skills 目录，你现在拥有了 arc-reactor")
```

### 更新升级 (Upgrade)
当项目发布新版本需要拉取修复时：

```bash
cd ~/.openclaw/skills/arc-reactor
git pull origin main
```
> **注意**：如果有针对某个具体版本号的需求，可以使用 `git checkout vX.X.X`。

---

## 🗄️ 核心原理：Compilation over Retrieval

当你给 Agent 发送一条网页链接并要求 `Ingest`（深度归档入库）时，ARC 不是输出一份一次性的回答，而是会在后台执行**“四连击（4-combo）”**，将知识化整为零并永久沉淀在你的 Workspace 中：

```text
workspace/arc-reactor-doc/wiki/
├── sources/
│   └── YYYY-MM-DD/
│       └── [topic_slug].md  ← 第一击：保存特定时间的阅读摘要备忘
├── entities/
│   └── [topic].md           ← 第二击：抽取名词概念卡片，在旧卡片上做增量合并
├── index.md                 ← 第三击：立刻更新全库大门总目录
└── log.md                   ← 第四击：留下执行审计记录
```
任何后续的问题（**Query**），大模型都会主动阅读 `index.md` 选择相关卡片作答，真正做到“基于您的私域百科全书”说话。

## 目录结构

```text
arc-reactor/
├── SKILL.md                          # 核心执行引导入口 (Agent 第一级读取指令)
├── _meta.json                        # 内部版本管控参数
├── README.md                         # (You are here)
└── references/
    ├── dedup-rules.md                # 三级强制去重检测与增量合并原则
    ├── verification-pipeline.md      # 事实可信度的二次防伪和穿透管线 (验证网络)
    ├── knowledge-rules.md            # “报告快照”向“活体实体知识”升级的编译指导
    ├── templates/
    │   └── report-template.md        # MD 文档统一强制排版标准
    └── dispatchers/
        └── obsidian.md               # 云端节点（如 Obsidian）自动同步挂载协议和检查机制脚本
```

## 仓库管理与反馈

- **GitHub Repository**: [https://github.com/evan-zhang/arc-reactor](https://github.com/evan-zhang/arc-reactor)
- **Issues & PRs**: 欢迎为 ARC 提交 Bug 或者功能增强请求 → [提个 Issue](https://github.com/evan-zhang/arc-reactor/issues)
- **AODW RT**: 本项目由 RT-002 进行版本迭代与管理。
- **维护者**: [@evan-zhang](https://github.com/evan-zhang)

---

## 🧪 实战测试用例指南 (Test Cases)

如果你刚把 ARC Reactor 挂载到一个全新的 Agent 上，可以使用以下测试方案验证这台“私人知识库”是否火力全开。我们以一篇关于大模型架构的文章为例进行实战演练。

### Case 1: Ingest 深度摄入与四连击归档
- **模拟输入**：“请 Ingest 这篇文章，关于 OpenClaw 的架构设计：`[URL]`”
- **预期考核**：
    1. Agent 不得手工拼凑文件，必须通过内置管道执行写入。
    2. **精准触发4大动作**：
       - `sources/YYYY-MM-DD/openclaw.md` 产生摘要快照。
       - `entities/openclaw.md` 抽取实体名片。
       - `index.md` 追加目录记录。
       - `log.md` 写入审计日志。

### Case 2: 双轨记账与时间回溯
- **模拟输入**：“昨天我让你收录的那篇涉及 OpenClaw 的文章，能在我的日历系统里找出来发给我吗？”
- **预期考核**：
    Agent **不得去 `entities/`** 下搜索增量混编内容，它应当能准确地走到 `sources/YYYY-MM-DD/` 根据昨天的时间戳将阅读原本直接抽调出来供你查阅。

### Case 3: 知识图谱游走查询 (Concept Network Query)
- **模拟输入**：“基于目前的私人知识库，帮我总结一下前几次收录情报中，关于 OpenClaw 和 RAG 有哪些千丝万缕的底层联系？”
- **预期考核**：
    1. Agent 绝不能立刻联网盲搜。
    2. 它必须第一步先读大门黑板：`wiki/index.md`。
    3. 找到相关的 `[[双向链接]]` 词语（如 OpenClaw, RAG）后，打开细分实体卡片，融会贯通后作出回答。

### Case 4: 时间切片对比分析 (Time-Sliced Analysis)
- **模拟输入**：“对比一下半年前收录的旧知识与上周最新收录的架构报告，关于 Agent 自我提升 (RSI) 的认知发生了哪些根本性变化？”
- **预期考核**：
    Agent 需要利用我们设置的 **双轨记账** 机制，深入 `sources/YYYY-MM-DD/` 查阅不同年代的快照，从纯净的时间维度提取出观点的演进历程，而非一味相信实体库里被覆盖后的最终结论。

### Case 5: 深度实体穿透取数 (Deep Entity Extraction)
- **模拟输入**：“从我的库里，把所有关于‘多模型分派’配置参数的 YAML 样例全部提取出来，给我一个干净的代码清单。”
- **预期考核**：
    Agent 不做主观发散，它定位到相关的技术实体后，精准提取出该页面下曾经摘录的所有核心数据块（如代码片段、数字统计等），并将高密度的信息组装成表格或清单输出，充当“超级检索手”。

### Case 6: 认知缺口探测 (Gap Detection & Recommendation)
- **模拟输入**：“通过扫描我的知识库目录，帮我分析目前我在‘架构设计’领域的知识点还有哪些严重缺失？建议我去查阅哪类文章？”
- **预期考核**：
    Agent 分析 `index.md` 中各个领域的比重，找出只有一两个提及但在行业中很重要的“关联孤岛概念”，并为您提供下一份补齐版图的阅读/检索清单。

### Case 7: 周末大扫除 (Lint 整理机制)
- **模拟输入**：“请对当前的 arc-reactor-doc/wiki 执行一次整体 Lint，看看有没有断开的链接或空包档案。”
- **预期考核**：
    这是它作为管理员的职责，它应当去读取 `index.md` 交叉比对 `entities/` 下的文件，看看是否有的链接在文章里提到了，却没有真实的物理卡片。若有，向你报告清理策略。

### Case 8: 落盘幻觉免疫测试 (附件必达铁律)
- **模拟输入**：“（发送任意链接）帮我研究这个并整理一份摘要不保存系统，看完发我就行。”
- **预期考核**：
    受到系统的最高约束，只要执行了知识摄入，不管有没有存入本地，最后一步必须通过 `message` 系统的附加文档功能向您真实的移动端发送最终的 Markdown 实效文件。若只发文本路径敷衍您，即判定幻觉失败。
