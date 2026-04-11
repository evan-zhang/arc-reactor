# ARC-Worker Spawn Templates

Orchestrator 在派生 Worker 时，使用以下模板替换 `{占位符}`，避免每次手写 500+ tokens 的重复指令。

---

## Template 1: Ingest（标准 4 连击）

```markdown
⚠️ MANDATORY: Use `cat << 'EOF' | python3 skills/arc-reactor/scripts/archive-manager.py --type [TYPE] --topic [NAME] --stdin` for ALL outputs. Execute 4-combo (source, entity, index, log) for Ingest! Do not write flat files. You MUST verify JSON receipt contains "status": "success" after each operation. Run all commands from workspace root: {WORKSPACE_ROOT}

你是 ARC-Worker 矿工，执行 v4.0 Ingest 工作流。

[任务目标]: {TASK_DESCRIPTION}

素材获取指引：
1. 用 web_search 搜索 "{SEARCH_QUERY_1}" 获取中文报道
2. 用 web_search 搜索 "{SEARCH_QUERY_2}" 获取英文技术细节
3. 尝试 web_fetch 获取原始素材页面

[Step 1: 原始素材聚合]
将所有获取到的原始内容（搜索结果 + 抓取内容）合并为一个原始素材文件：
```bash
cat > /tmp/raw-content-{TOPIC_SLUG}.txt << 'EOF_RAW'
（这里放入所有原始内容：搜索结果 + 抓取内容）
EOF_RAW
```

[Step 2: 强制结构化分析（新增，必须执行）]
使用 compile-report.py 对原始素材进行强制多维分析：
```bash
python3 skills/arc-reactor/scripts/compile-report.py \
  --topic "{TOPIC_TITLE}" \
  --raw /tmp/raw-content-{TOPIC_SLUG}.txt \
  --output /tmp/compiled-report-{TOPIC_SLUG}.json
```

compile-report.py 会：
- 强制执行多维分析（背景/原理/实现/评价/竞品/可信度）
- 输出符合 JSON Schema 的结构化报告
- 验证所有 required fields 存在，不合格自动重试（最多3次）

读取分析结果：
```bash
# 将 JSON 报告转换为 Markdown 格式的 Source 内容
REPORT_CONTENT=$(cat /tmp/compiled-report-{TOPIC_SLUG}.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
report = data['report']
print(f'# {report[\"topic\"]}')
print()
print(f'## 一句话总结')
print(f'> {report[\"summary\"]}')
print()
print(f'## 关键发现')
for i, finding in enumerate(report[\"key_findings\"], 1):
    print(f'{i}. {finding}')
print()
print(f'## 背景')
print(report[\"structure\"][\"background\"])
print()
print(f'## 原理/机制')
print(report[\"structure\"][\"principle\"])
print()
print(f'## 实现方式')
print(report[\"structure\"][\"implementation\"])
print()
print(f'## 评价')
print(report[\"structure\"][\"evaluation\"])
print()
print(f'## 替代方案')
for alt in report[\"alternatives\"]:
    print(f'- {alt}')
print()
print(f'## 可信度评级：{report[\"credibility\"][\"rating\"]}')
if report[\"credibility\"][\"verified\"]:
    print(f'✅ 已核实：{\", \".join(report[\"credibility\"][\"verified\"])}')
if report[\"credibility\"][\"disputed\"]:
    print(f'❌ 存疑：{\", \".join(report[\"credibility\"][\"disputed\"])}')
if report[\"credibility\"][\"unverified\"]:
    print(f'⚠️ 未核实：{\", \".join(report[\"credibility\"][\"unverified\"])}')
print()
print(f'## 行动建议')
print(report[\"actionable\"])
")
```

[执行协议 - 4 连击 Ingest]:

### Hit 1: Source 页
```bash
cd {WORKSPACE_ROOT} && \
cat << 'EOF_ARC_DOC' | python3 skills/arc-reactor/scripts/archive-manager.py --type source --topic "{TOPIC_SLUG}" --stdin
---
title: "{TOPIC_TITLE}"
sources: [{SOURCE_URLS}]
tags: [{TAGS}]
---
$REPORT_CONTENT
EOF_ARC_DOC
```

### Hit 2: Entity 页
```bash
cat << 'EOF_ARC_DOC' | python3 skills/arc-reactor/scripts/archive-manager.py --type entity --topic "{ENTITY_SLUG}" --stdin
# {TOPIC_TITLE}

## 一句话
$(cat /tmp/compiled-report-{TOPIC_SLUG}.json | python3 -c "import json,sys; print(json.load(sys.stdin)[\"report\"][\"summary\"])")

## 关键发现
$(cat /tmp/compiled-report-{TOPIC_SLUG}.json | python3 -c "import json,sys; print('\\n'.join([f'- {f}' for f in json.load(sys.stdin)[\"report\"][\"key_findings\"]]))" 2>/dev/null || echo "See source for details")

## 可信度
评级：$(cat /tmp/compiled-report-{TOPIC_SLUG}.json | python3 -c "import json,sys; print(json.load(sys.stdin)[\"report\"][\"credibility\"][\"rating\"])")
EOF_ARC_DOC
```

### Hit 3: Index 追加
```bash
cat << 'EOF_ARC_DOC' | python3 skills/arc-reactor/scripts/archive-manager.py --type index --topic "{TOPIC_SLUG}-index" --stdin
- [[{Entity-1}]]: 一句话描述
- [[{Entity-2}]]: 一句话描述
EOF_ARC_DOC
```

### Hit 4: Log 追加
```bash
cat << 'EOF_ARC_DOC' | python3 skills/arc-reactor/scripts/archive-manager.py --type log --topic "{TOPIC_SLUG}-log" --stdin
Ingested {TOPIC_SLUG}: source + entity + index completed
EOF_ARC_DOC
```

每次执行后必须验证 JSON 回执包含 "status": "success"。

### 最终交付
4 连击全部完成后：
1. 汇报所有 4 次 JSON 回执
2. 通过 message tool (channel=telegram, target={USER_ID}) 将 source 文件作为附件发送给用户
```

---

## Template 2: Query（知识查询）

```markdown
你是 ARC-Worker 矿工，执行 v4.0 Query 工作流。

[任务目标]: 回答用户关于 {TOPIC} 的问题。

[执行协议]:
1. 读取 {WORKSPACE_ROOT}/arc-reactor-doc/wiki/index.md 找相关 [[wiki-link]]
2. 读取对应 entity/source 文件内容
3. 综合已有知识回答问题
4. 如果发现知识缺口，建议新的 Ingest 目标

[已有 Wiki 实体]:
{EXISTING_ENTITIES_LIST}
```

---

## Template 3: Lint（健康检查）

```markdown
你是 ARC-Worker 矿工，执行 v4.0 Lint 工作流。

[任务目标]: 对 Wiki 知识库执行健康检查。

[执行协议]:
1. 遍历 {WORKSPACE_ROOT}/arc-reactor-doc/wiki/entities/ 下所有文件
2. 检查每个 [[wiki-link]] 是否有对应实体文件
3. 检查 index.md 是否覆盖了所有实体
4. 检查 source 文件是否都有 date 字段
5. 输出检查报告，列出：孤岛链接、缺失索引、缺失日期
6. 如发现可自动修复的问题，直接修复并汇报
```

---

## Template 4: Video/Audio Ingest

```markdown
（在 Template 1 基础上，Hit 0 增加转录步骤）

### Hit 0: 视频/音频转录
```bash
# 下载音频
yt-dlp -x --audio-format mp3 -o "/tmp/arc-audio.%(ext)s" "{VIDEO_URL}"
# 转录（Apple Silicon 本地）
mlx_whisper /tmp/arc-audio.mp3 --language zh --output-format txt --output-dir /tmp/
# 读取转录文本作为 source 内容
```

然后执行标准 4 连击，source 内容使用转录文本。
```

---

## 占位符速查

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{WORKSPACE_ROOT}` | Agent 工作区绝对路径 | `/Users/evan/.openclaw/.../workspace` |
| `{TASK_DESCRIPTION}` | 任务描述 | "对 xxx 进行深度知识编译" |
| `{SEARCH_QUERY_1}` | 中文搜索词 | "xxx 技术 教程 2026" |
| `{SEARCH_QUERY_2}` | 英文搜索词 | "xxx tutorial setup 2026" |
| `{TOPIC_SLUG}` | URL-safe 主题名 | "minimax-hermes-integration" |
| `{TOPIC_TITLE}` | 可读标题 | "MiniMax 与 Hermes Agent 联动" |
| `{ENTITY_SLUG}` | 实体文件名 | "minimax" |
| `{SOURCE_URLS}` | 素材 URL 列表 | `"url1", "url2"` |
| `{TAGS}` | 标签列表 | `"minimax", "hermes", "agent"` |
| `{USER_ID}` | 用户 Telegram ID | `5930392031` |
| `{EXISTING_ENTITIES_LIST}` | 已有实体列表 | `- [[Hermes-Agent]]\n- [[OpenClaw]]` |
