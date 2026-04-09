#!/bin/bash

# ARC Reactor v4.2.0 Comprehensive Verification Suite
# 此脚本用于自动化验证 Ingest, Injection, Weekly Report 核心功能

ROOT_NAME="verification-vault"
SKILL_PATH="skills/arc-reactor"
ARCHIVE_SCRIPT="$SKILL_PATH/scripts/archive-manager.py"
INJECT_SCRIPT="$SKILL_PATH/scripts/context-injector.py"
WEEKLY_SCRIPT="$SKILL_PATH/scripts/weekly-reporter.py"

echo "=== [Step 0] 清理与环境准备 ==="
rm -rf "$ROOT_NAME"
mkdir -p "$ROOT_NAME"

echo -e "\n=== [Step 1] 测试 Ingest (4-Combo / Day 1) ==="
# 存入关于 OpenClaw 的知识 (模拟 2026-04-01)
cat << 'EOF' | python3 "$ARCHIVE_SCRIPT" --type source --topic "openclaw-intro" --date "2026-04-01" --root "$ROOT_NAME" --stdin
---
title: OpenClaw Introduction
date: 2026-04-01
tags: [framework, ai]
---
# OpenClaw Architecture
OpenClaw is a modular agent gateway. It supports [[Skills]] and custom [[Reactors]].
EOF

# 存入 Entity
cat << 'EOF' | python3 "$ARCHIVE_SCRIPT" --type entity --topic "OpenClaw" --root "$ROOT_NAME" --stdin
# OpenClaw
Core framework of the ARC ecosystem.
EOF

# 更新 Index
echo "- [[OpenClaw]]: Core framework for Agent gateways" | python3 "$ARCHIVE_SCRIPT" --type index --root "$ROOT_NAME" --stdin

# 追加 Log
echo "Ingested OpenClaw introduction" | python3 "$ARCHIVE_SCRIPT" --type log --root "$ROOT_NAME" --stdin

echo -e "\n=== [Step 2] 测试 Ingest (4-Combo / Day 2) ==="
# 存入关于 RSI 的知识 (模拟 2026-04-02)
cat << 'EOF' | python3 "$ARCHIVE_SCRIPT" --type source --topic "rsi-concept" --date "2026-04-02" --root "$ROOT_NAME" --stdin
---
title: Recursive Self Improvement
date: 2026-04-02
tags: [rsi, future]
---
# RSI Path
Recursive Self Improvement (RSI) is the key to singularity. It connects with [[OpenClaw]] via internal feedback loops.
EOF

# 更新 Index
echo "- [[RSI]]: Recursive Self Improvement concept" | python3 "$ARCHIVE_SCRIPT" --type index --root "$ROOT_NAME" --stdin

# 追加 Log
echo "Ingested RSI concept" | python3 "$ARCHIVE_SCRIPT" --type log --root "$ROOT_NAME" --stdin

echo -e "\n=== [Step 3] 验证文件目录完整性 ==="
ls -R "$ROOT_NAME" | grep ".md"

echo -e "\n=== [Step 4] 测试 Subconscious Injection (RT-007) ==="
echo "Query: '告诉我关于 OpenClaw 的设计'"
python3 "$INJECT_SCRIPT" --query "告诉我关于 OpenClaw 的设计" --root "$ROOT_NAME"

echo -e "\n=== [Step 5] 测试 Weekly Executive Brief (RT-008) ==="
echo "Generating report for last 10 days..."
# 我们通过环境变量或系统时间模拟，脚本内部基于日期计算，这里直接运行以验证聚合
python3 "$WEEKLY_SCRIPT" --days 10 --root "$ROOT_NAME"

echo -e "\n=== [Step 6] 验证结束 ==="
# rm -rf "$ROOT_NAME" # 暂时保留，供用户审阅后手动删除
echo "测试流程已全部执行。请检查上方输出是否包含 <ARC_KNOWLEDGE_CONTEXT> 以及 周报内容。"
