#!/usr/bin/env python3
import os
import sys
import argparse
import json
import hashlib
from datetime import datetime
import re

def slugify(text):
    """简单规范化文件名"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text if text else "untitled"

def main():
    parser = argparse.ArgumentParser(description='ARC Reactor V4 Archive Manager (Karpathy Wiki Edition)')
    parser.add_argument('--type', choices=[
        'raw', 'source', 'entity', 'concept', 'index', 'log', 'template'
    ], required=True, help='归档进入的 Wiki 圈层类型')
    
    parser.add_argument('--topic', required=False, default='knowledge-node', help='话题/实体名 (用于生成文件名)')
    parser.add_argument('--stdin', action='store_true', help='强制通过标准输入读取内容 (防止转义错误)')
    parser.add_argument('--root', default='arc-reactor-doc', help='文档根目录名称')

    args = parser.parse_args()

    # 1. 验证必须使用 --stdin
    if not args.stdin:
        print(json.dumps({"status": "error", "message": "安全限制: 必须使用 --stdin 通过管道传参"}))
        sys.exit(1)

    content_to_write = sys.stdin.read()
    if not content_to_write.strip():
        print(json.dumps({"status": "error", "message": "写入内容为空"}))
        sys.exit(1)

    # 2. 确定物理路径
    cwd = os.getcwd()
    
    # 自动探测工作区根目录 (向上一圈圈遍历寻找 arc-reactor-doc 或 .git)
    doc_root = None
    curr_dir = cwd
    while curr_dir and curr_dir != '/':
        # 如果当前大目录下有我们想要的归档文件夹，这就是正确的工作区
        if os.path.exists(os.path.join(curr_dir, args.root)):
            doc_root = os.path.join(curr_dir, args.root)
            break
        # 如果碰到 .git，也认为到达了顶层
        if os.path.exists(os.path.join(curr_dir, '.git')):
            doc_root = os.path.join(curr_dir, args.root)
            break
        curr_dir = os.path.dirname(curr_dir)
        
    # 如果全遍历完都没找到，兜底使用最初的 cwd
    if not doc_root:
        doc_root = os.path.join(cwd, args.root)

    target_dir = ""
    filename = ""
    topic_slug = slugify(args.topic)
    
    # Wiki 层路由判定
    if args.type == 'raw':
        target_dir = os.path.join(doc_root, 'raw')
        filename = f"{topic_slug}.md"
    elif args.type == 'source':
        target_dir = os.path.join(doc_root, 'wiki', 'sources', args.date)
        filename = f"{topic_slug}.md"
    elif args.type == 'entity':
        target_dir = os.path.join(doc_root, 'wiki', 'entities')
        filename = f"{topic_slug}.md"
    elif args.type == 'concept':
        target_dir = os.path.join(doc_root, 'wiki', 'concepts')
        filename = f"{topic_slug}.md"
    elif args.type == 'index':
        target_dir = os.path.join(doc_root, 'wiki')
        filename = "index.md"
    elif args.type == 'log':
        target_dir = os.path.join(doc_root, 'wiki')
        filename = "log.md"
    elif args.type == 'template':
        target_dir = os.path.join(doc_root, 'references', 'templates')
        filename = f"custom_{topic_slug}.md"

    # 3. 稳健创建父目录
    try:
        os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"目录自愈创建失败: {str(e)}"}))
        sys.exit(1)

    # 4. 路由特定的写入模式 (Append vs Overwrite)
    target_path = os.path.join(target_dir, filename)
    mode = 'w'
    final_write_content = content_to_write
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    now_date = datetime.now().strftime('%Y-%m-%d')

    if args.type in ['index', 'log']:
        # index 和 log 永远是增量追加
        mode = 'a'
        if args.type == 'log':
            final_write_content = f"\n- **[{now_str}]** {content_to_write.strip()}"
        else: # index.md
            final_write_content = f"\n{content_to_write.strip()}"
            
    elif args.type in ['entity', 'concept'] and os.path.exists(target_path):
        # 知识节点增量追加
        mode = 'a'
        final_write_content = f"\n\n---\n## 增量知识点合入 ({now_str})\n\n" + content_to_write
        
    # 自动探测并注入 Frontmatter 时间戳 (仅对新建的文件有效)
    if mode == 'w' and final_write_content.strip().startswith('---'):
        lines = final_write_content.strip().splitlines()
        # 扫描前20行看有没有 date: 字段
        has_date = any(line.lower().startswith('date:') for line in lines[:20])
        if not has_date and len(lines) > 1:
            # 在第一行 --- 下面插入 date
            lines.insert(1, f"date: {now_date}")
            final_write_content = "\n".join(lines)

    # 5. 原子落盘及防幻觉回执生成
    try:
        with open(target_path, mode, encoding='utf-8') as f:
            f.write(final_write_content)
        
        with open(target_path, 'rb') as f:
            file_bytes = f.read()
            checksum = hashlib.sha256(file_bytes).hexdigest()
            size_bytes = len(file_bytes)
            
        receipt = {
            "status": "success",
            "type_routed": args.type,
            "path": target_path,
            "size_bytes": size_bytes,
            "checksum": checksum,
            "message": "Karpathy Wiki Layer write valid."
        }
        print(json.dumps(receipt, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "error", "message": f"I/O 崩溃: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
