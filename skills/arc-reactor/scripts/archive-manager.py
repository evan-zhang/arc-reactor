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
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text

def main():
    parser = argparse.ArgumentParser(description='ARC Reactor Archive Manager')
    parser.add_argument('--type', choices=['report', 'entity', 'concept', 'template'], required=True, 
                        help='档案类型')
    parser.add_argument('--topic', required=True, help='话题或文件名')
    parser.add_argument('--content', help='内容字符串 (已废弃，请使用 --stdin)')
    parser.add_argument('--stdin', action='store_true', help='通过标准输入读取内容 (推荐，防止转义错误)')
    parser.add_argument('--date', default=datetime.now().strftime('%Y-%m-%d'), help='归档日期 (默认今天)')
    parser.add_argument('--root', default='arc-reactor-doc', help='文档根目录名称')

    args = parser.parse_args()

    # 0. 获取正文内容
    if args.stdin:
        content_to_write = sys.stdin.read()
    elif args.content is not None:
        content_to_write = args.content
    else:
        print(json.dumps({"status": "error", "message": "必须提供内容: 请开启 --stdin 或提供 --content 参数"}))
        sys.exit(1)

    if not content_to_write.strip():
        print(json.dumps({"status": "error", "message": "写入内容为空"}))
        sys.exit(1)

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
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"目录创建失败: {str(e)}"}))
        sys.exit(1)

    # 4. 执行写入
    target_path = os.path.join(target_dir, filename)
    mode = 'w'
    
    # 增量写入逻辑
    if args.type == 'entity' and os.path.exists(target_path):
        mode = 'a'
        final_write_content = f"\n\n---\n### 增量更新 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n\n" + content_to_write
    else:
        final_write_content = content_to_write

    try:
        # Atomic Write
        with open(target_path, mode, encoding='utf-8') as f:
            f.write(final_write_content)
        
        # 提取文件状态供验证
        with open(target_path, 'rb') as f:
            file_bytes = f.read()
            checksum = hashlib.sha256(file_bytes).hexdigest()
            size_bytes = len(file_bytes)
            
        receipt = {
            "status": "success",
            "path": target_path,
            "size_bytes": size_bytes,
            "checksum": checksum,
            "message": "Archive completed successfully."
        }
        print(json.dumps(receipt, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "error", "message": f"写入发生异常: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
