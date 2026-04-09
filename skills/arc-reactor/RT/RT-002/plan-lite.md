# Plan-Lite: RT-002 - ARC Reactor Skill 抽离

## 1. 修改点（Change Points）
- `skills/arc-reactor/`：新建独立 Skill
- `gateways/life/state/workspace-life/AGENTS.md`：删除嵌入式 SOP，替换为 Skill 引用
- `RT/RT-002/`：自包含档案

## 2. 方案描述（Solution Outline）

### 2.1 新建 Skill 结构
```
skills/arc-reactor/
├── SKILL.md                    # 核心触发器（A/R/C 三阶段定义）
├── _meta.json                  # 版本信息
├── references/
│   ├── workflow.md             # 完整执行流程
│   ├── report-template.md      # 标准化报告模板（逆向提炼自现有报告）
│   └── archive-rules.md        # 归档规则（Obsidian 同步、目录规范）
└── README.md                   # 开源说明
```

### 2.2 AGENTS.md 瘦身
- 移除第 210-229 行的嵌入式 SOP
- 替换为：`> ARC 调研能力详见 Skill：skills/arc-reactor/`

### 2.3 RT-002 自包含档案
- intake.md ✅（已创建）
- plan-lite.md ✅（本文件）
- spec-lite.md / changelog.md / repos.md / SOP.md（执行中创建）

## 3. ARC 三阶段定义
- **Acquire**：接收 URL → 查重 → 抓取内容 → 创建调研实例
- **Research**：结构化分析 → 提炼关键信息 → 交叉引用
- **Catalogue**：标准格式报告 → 发送频道 → 同步 Obsidian → git commit

## 4. 风险与注意事项
- AGENTS.md 瘦身后需确认 Agent 能正确挂载新 Skill
- 报告模板需从现有高质量报告（如 DeerFlow 报告）逆向提炼
