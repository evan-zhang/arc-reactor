# ARC Reactor v2.0 (AODW-Next Skill)

> **⚠️ AI-First Repository**
> This repository is designed **primarily for AI Agents**, specifically for the [OpenClaw](https://openclaw.ai) ecosystem. If you are an AI/Agent reading this, please process the `SKILL.md` as your primary entry point. Human developers are welcome to contribute, but the file structures and documentation style favor agentic cognitive ingestion.

**ARC = Acquire / Research / Catalogue**

面向个人知识建设的 AI 调研引擎。给它一个链接或话题，它不仅仅能剥离内容，更会**挂载多路爬虫组件与外联搜索**自动完成 获取→真伪勘察对比→编目的全链路，为你凝结真正的竞争分析洞察。

## 🎯 v2.0 终极演进特性

- 🕵️ **广域交叉核网 (Active Extended Probing)**：打破只看原链接的偏信束缚，自发调用 API 全网搜寻原素材的“替代竞品”且进行交叉打假，让调研不仅是排版，更具备战略判定！
- 🎥 **多模态强网捕捞 (Media Scraper Hooks)**：全面支持接入 Clawhub 的第三方反扒挂件，轻松吞吐 YouTube 或抖音等视频切片，甚至是 Twitter 等社交私域信息并做音频转录。
- 🌩️ **高并发智能派生 (Orchestrator-Worker 架构)**：接收需求时绝不阻塞主聊天，使用原生指令静默唤醒多只 ARC 矿工 Sub-agent 在后台极速吞吐采集。
- 🔄 **全自动去重**：三级检测 + 增量合并，同一主体只维护一份"活报告"
- 📚 **知识编译**：借鉴 Karpathy LLM Wiki，每次调研增量编译个人知识图谱
- 📤 **插件式极简投递**：严禁占用用户的聊天框长篇大论，所有大批次文档严格做物理切片，直投附件包裹给 Telegram/移动客户机端。

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

## 🗄️ 输出与存储形式

当你给 Agent 发送一条带调研任务的链接时，ARC 抓取完数据后并不只是抛出一篇一次性的回答，而是会沉淀出一个 **“双轨制”** 静态资料库系统：

### 维度 1: 流水账大厅 (历史快照)
**物理路径举例**：`workspace/reports/YYYY-MM-DD/`

这是单次调研的固定切片，代表它在某一天的定格模样。结构包含：
- **`[主题名]-调研报告.md`**：自动生成标准化排版的文档，含基本信息、核心事实、结论和关联溯源表。
- **`raw/` 文件夹**：存放抓取该文档时一并拉取的音视频原转录稿、网页快照和图像原卷。

### 维度 2: 知识编译中心 (Karpathy 活字典模式)
**物理路径举例**：`workspace/knowledge/`

这是 ARC Reactor 的**真正威力核心**。报告一旦生成，会触发背后的“知识编译器”进行处理：
- 抽取**实体页** (`entities/[实体].md`)：如同剥洋葱，多次涉及“OpenAI”的新老报告会被无缝挂载、补充至此实体的独立卡片下，而不是生成一堆散乱文档。
- 抽取**概念网络** (`concepts/[方法论].md`) 和 **冲突自检** (`conflicts/`)：对于老资料与新报告之间的参数和定性打架，全自动生成矛盾审查记录给用户过目。
- 后端最终会通过自带的 `dispatchers/obsidian.md` 调度器直接推送到你自己的 iCloud Obsidian 等客户端下。

---

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
