#!/usr/bin/env python3
import os
import sys
import argparse
from datetime import datetime
import re

def slugify(text):
    """简单规范化文件名"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text

def main():
    parser = argparse.ArgumentParser(description='ARC Reactor Archive Manager')
    parser.add_argument('--type', choices=['report', 'entity', 'concept', 'template'], required=True, 
                        help='档案类型')
    parser.add_argument('--topic', required=True, help='话题或文件名')
    parser.add_argument('--content', required=True, help='内容字符串')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='归档日期 (默认今天)')
    parser.add_argument('--root', default='arc-reactor-doc', help='文档根目录名称')

    args = parser.parse_args()

    # 1. 确定工作区根路径 (当前执行目录)
    cwd = os.getcwd()
    doc_root = os.path.join(cwd, args.root)

    # 2. 根据类型计算物理路径
    target_dir = ""
    filename = ""

    topic_slug = slugify(args.topic)

    if args.type == 'report':
        target_dir = os.path.join(doc_root, 'reports', args.date, topic_slug)
        filename = "report.md"
    elif args.type == 'entity':
        target_dir = os.path.join(doc_root, 'knowledge', 'entities')
        filename = f"{topic_slug}.md"
    elif args.type == 'concept':
        target_dir = os.path.join(doc_root, 'knowledge', 'concepts')
        filename = f"{topic_slug}.md"
    elif args.type == 'template':
        target_dir = os.path.join(doc_root, 'references', 'templates')
        filename = f"custom_{topic_slug}.md"

    # 3. 目录自愈
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
        print(f"创建目录: {target_dir}")

    # 4. 执行写入
    target_path = os.path.join(target_dir, filename)
    
    # 如果是 entity 且文件已存在，执行增量写入
    mode = 'w'
    if args.type == 'entity' and os.path.exists(target_path):
        mode = 'a'
        content_to_write = f"\n\n---\n### 增量更新 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n" + args.content
    else:
        content_to_write = args.content

    with open(target_path, mode, encoding='utf-8') as f:
        f.write(content_to_write)

    print(f"成功归档: {target_path}")

if __name__ == "__main__":
    main()
