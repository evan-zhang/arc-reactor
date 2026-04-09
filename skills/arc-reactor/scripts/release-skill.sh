#!/bin/bash
# ARC Reactor Skill Release Packager (v1.0)
# 作用：自动将 Skill 组件打包成标准的发布格式

set -e

# 1. 自动定位 Skill 根目录 (当前脚本所在目录的父目录)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SKILL_NAME_ID="arc-reactor"

echo "📦 正在初始化 ARC Reactor Skill 打包流程..."
echo "📍 Skill 根路径: $SKILL_ROOT"

# 2. 读取元数据
META_FILE="$SKILL_ROOT/_meta.json"
if [ ! -f "$META_FILE" ]; then
    echo "❌ 错误: 找不到 $META_FILE，请确保脚本在正确的 Skill 目录下运行。"
    exit 1
fi

VERSION=$(grep -o '"version": "[^"]*"' "$META_FILE" | cut -d'"' -f4)
NAME=$(grep -o '"name": "[^"]*"' "$META_FILE" | cut -d'"' -f4)

echo "🏷️  检测到版本: $VERSION (Skill: $NAME)"

# 3. 创建发布目录
DIST_DIR="$SKILL_ROOT/dist"
mkdir -p "$DIST_DIR"

PACKAGE_NAME="${NAME}-v${VERSION}.zip"
TARGET_ZIP="$DIST_DIR/$PACKAGE_NAME"

# 4. 执行打包 (精准排除)
echo "📂 正在整理文件并压缩..."

cd "$SKILL_ROOT"

# 计算脚本相对于 SKILL_ROOT 的路径，以便精准排除
REL_SCRIPT_PATH=$(python3 -c "import os; print(os.path.relpath('$SCRIPT_DIR/release-skill.sh', '$SKILL_ROOT'))")

# 使用 zip 命令，精准排除
# -x "*/__pycache__" 排除目录节点本身
# -x "*/__pycache__/*" 排除目录下的所有文件
zip -r "$TARGET_ZIP" . \
    -x "dist/*" \
    -x "$REL_SCRIPT_PATH" \
    -x "*/__pycache__" \
    -x "*/__pycache__/*" \
    -x "*.pyc" \
    -x ".DS_Store" \
    -x "*/.DS_Store" \
    -x "arc-reactor-doc/*" \
    -x ".git/*" \
    -x ".git" \
    -x ".cursor/*" \
    -x ".cursor"

echo "------------------------------------------------"
echo "✅ 打包成功！"
echo "🚀 发布包路径: $TARGET_ZIP"
echo "📊 文件大小: $(du -h "$TARGET_ZIP" | cut -f1)"
echo "------------------------------------------------"

# 5. 生成 Release 摘要建议
echo "📝 GitHub Release 建议内容:"
echo "---"
echo "## ARC Reactor Skill v$VERSION"
echo ""
echo "### ✨ 核心更新"
echo "- **Smart Ingest 增强**: 支持今日头条、掘金等高反爬站点的智能抓取。"
echo "- **沙盒自适应**: 引入了云端 Reader 桥接逻辑，解决本地无浏览器环境的痛点。"
echo ""
echo "### 🚀 安装方式"
echo "下载后解压到 \`~/.openclaw/skills/arc-reactor/\` 即可。"
echo "---"
