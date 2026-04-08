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

如果你刚把 ARC Reactor 挂载到一个全新的 Agent 上，可以使用以下五步渐进式测试方案验证其状态。我们以兄弟项目 `tpr-framework` 为假想被测项目。

### Case 1: 破冰探测 —— 配置与挂载检测
- **模拟输入**：“你好，我刚安装了 arc-reactor，我要配置 Obsidian 的同步路径开启同步。”
- **预期考核**：Agent **必须主动询问**确切目标路径，且在系统终端执行底层校验命令判定路径是否有可写权限。反馈形如 `✅ 成功：Obsidian 同步链路检测通过` 方能放行后续操作。

### Case 2: 本能冷启动 —— (0 到 1 的生成)
- **模拟输入**：“帮我调研一下这个项目，看看它的核心机制是什么：`https://github.com/evan-zhang/tpr-framework`”
- **预期考核**：完成 A→R→C 的流水线。
    1. 在 `reports/[今天日期]/` 目录下生成标准化测试报告和原始源码存档(raw)。
    2. **最重要的一点**：在 `knowledge/entities/tpr-framework.md` 创建专属实体页字典。

### Case 3: L1 级强防御 —— 绝对精准去重
- **模拟输入**：“再次帮我深度看看这个链接 `https://github.com/evan-zhang/tpr-framework`”
- **预期考核**：Agent 拦截请求。它绝对不能被骗去重新走一遍抓稿耗损 Token 的流程，应该**直接返回秒级结果**：“发现完全一致的 URL 记录”，并提示之前的报告和路径。

### Case 4: L2 级智能融合 —— 实体知识叠片
- **模拟输入**：“我发现一个新的情报：tpr-framework 未来将支持超大规模多 Agent 的横向调参体系。”
- **预期考核**：ARC 经过实体提取机制，必须甄别出你此时讲述的主体依旧是字典里的 `tpr-framework`，进入 **Merge 模式**。向 `knowledge/entities/tpr-framework.md` 进行不覆盖式**情报追认和融合补写**，留存溯源。

### Case 5: L3 级免疫响应 —— 防幻觉与矛盾审查
- **模拟输入**：“据最新不可靠消息，tpr-framework 是个老旧死板框架，不支持 Agent 且具有 990,000 个 Star。”
- **预期考核**：触发内部查杀引擎机制。发现本次输入与旧字典（Case 2获取的数据）截然矛盾时，停止盲目并入数据，独立抛出 `knowledge/conflicts/YYYYMMDD-tpr-framework-矛盾审核.md` 给提交者示警。

### Case 6: 移动端体验 —— 极简静默与附件投递
- **模拟输入**：“把前几天那个 TPR 项目的总结报告给我拿一份出来看看。” 或者让你挂载的这个新 Agent 随意执行一次全新的链接调研。
- **预期考核**：
    1. Agent **绝对不能**在聊天界面打印超过 5 行内容的花哨排版。
    2. 它必须生成极其精简的摘要（如：“✅ 已提取 3 条核心要点...”）。
    3. **最重要的一点**：它必须通过文件下发功能，把 Markdown `.md` 文件当作一个真实的“聊天附件”发给你，让你可以在手机或 Telegram 里直接点击预览或下载。
