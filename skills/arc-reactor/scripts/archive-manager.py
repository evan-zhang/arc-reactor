#!/usr/bin/env python3
import os
import sys
import argparse
import json
import hashlib
from datetime import datetime
import re


def _split_inline_list(text):
    """拆分 YAML 内联列表，支持简单引号场景。"""
    items = []
    current = []
    quote_char = None

    for char in text:
        if char in ('"', "'"):
            if quote_char == char:
                quote_char = None
            elif quote_char is None:
                quote_char = char
        if char == ',' and quote_char is None:
            item = ''.join(current).strip()
            if item:
                items.append(item)
            current = []
            continue
        current.append(char)

    tail = ''.join(current).strip()
    if tail:
        items.append(tail)
    return items


def _parse_yaml_scalar(value):
    """解析简单 YAML 标量/内联列表。"""
    value = value.strip()
    if value == '':
        return ''
    if value.startswith('[') and value.endswith(']'):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_yaml_scalar(item) for item in _split_inline_list(inner)]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    lowered = value.lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    if lowered in ('null', 'none'):
        return None
    if re.fullmatch(r'-?\d+', value):
        return int(value)
    if re.fullmatch(r'-?\d+\.\d+', value):
        return float(value)
    return value


def _parse_simple_yaml(filepath):
    """使用标准库解析简单 YAML：顶层键值、嵌套字典、列表字典。"""
    with open(filepath, 'r', encoding='utf-8') as file_obj:
        raw_lines = file_obj.readlines()

    processed = []
    for raw_line in raw_lines:
        if not raw_line.strip() or raw_line.lstrip().startswith('#'):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(' '))
        processed.append({
            'indent': indent,
            'text': raw_line.strip()
        })

    def parse_mapping(index, indent):
        data = {}
        while index < len(processed):
            line = processed[index]
            if line['indent'] < indent:
                break
            if line['indent'] > indent:
                index += 1
                continue
            if line['text'].startswith('- '):
                break

            key, sep, remainder = line['text'].partition(':')
            if not sep:
                index += 1
                continue

            key = key.strip()
            remainder = remainder.strip()
            if remainder:
                data[key] = _parse_yaml_scalar(remainder)
                index += 1
                continue

            next_index = index + 1
            if next_index < len(processed) and processed[next_index]['indent'] > indent:
                child_indent = processed[next_index]['indent']
                if processed[next_index]['text'].startswith('- '):
                    data[key], index = parse_list(next_index, child_indent)
                else:
                    data[key], index = parse_mapping(next_index, child_indent)
            else:
                data[key] = {}
                index += 1
        return data, index

    def parse_list(index, indent):
        items = []
        while index < len(processed):
            line = processed[index]
            if line['indent'] < indent:
                break
            if line['indent'] > indent:
                index += 1
                continue
            if not line['text'].startswith('- '):
                break

            body = line['text'][2:].strip()
            if ':' in body:
                key, _, remainder = body.partition(':')
                item = {key.strip(): _parse_yaml_scalar(remainder.strip()) if remainder.strip() else {}}
                index += 1
                if index < len(processed) and processed[index]['indent'] > indent:
                    child_block, index = parse_mapping(index, processed[index]['indent'])
                    item.update(child_block)
                items.append(item)
                continue

            if body:
                items.append(_parse_yaml_scalar(body))
                index += 1
                continue

            index += 1
            if index < len(processed) and processed[index]['indent'] > indent:
                child_indent = processed[index]['indent']
                if processed[index]['text'].startswith('- '):
                    item, index = parse_list(index, child_indent)
                else:
                    item, index = parse_mapping(index, child_indent)
                items.append(item)
        return items, index

    parsed, _ = parse_mapping(0, 0)
    return parsed


def _find_config_path(start_path=None):
    """向上查找配置文件路径。"""
    search_dir = os.path.abspath(start_path or os.getcwd())
    if os.path.isfile(search_dir):
        search_dir = os.path.dirname(search_dir)

    while True:
        direct_path = os.path.join(search_dir, 'arc-reactor-config.yaml')
        nested_path = os.path.join(search_dir, 'skills', 'arc-reactor', 'arc-reactor-config.yaml')
        if os.path.exists(direct_path):
            return direct_path
        if os.path.exists(nested_path):
            return nested_path

        parent_dir = os.path.dirname(search_dir)
        if parent_dir == search_dir:
            return None
        search_dir = parent_dir


def load_config(start_path=None):
    """查找并解析 `arc-reactor-config.yaml`。"""
    config_path = _find_config_path(start_path)
    if not config_path:
        return {}
    return _parse_simple_yaml(config_path)


def resolve_kb_root(content_source, tags=None):
    """根据来源或标签自动匹配知识库根目录。"""
    config = load_config()
    knowledge_bases = config.get('knowledge_bases', []) or []
    normalized_tags = {str(tag) for tag in (tags or [])}

    for kb_entry in knowledge_bases:
        auto_route = kb_entry.get('auto_route', {}) or {}
        sources = auto_route.get('sources', []) or []
        if content_source in sources:
            return kb_entry.get('root')

    for kb_entry in knowledge_bases:
        auto_route = kb_entry.get('auto_route', {}) or {}
        route_tags = {str(tag) for tag in (auto_route.get('tags', []) or [])}
        if normalized_tags & route_tags:
            return kb_entry.get('root')

    return None


def _format_kb_yaml_entry(kb_entry):
    """格式化 knowledge_bases 条目为 YAML 文本。"""
    name = kb_entry['name']
    root = kb_entry['root']
    description = kb_entry.get('description', '')
    auto_route = kb_entry.get('auto_route', {}) or {}
    sources = auto_route.get('sources', []) or []
    tags = auto_route.get('tags', []) or []
    sources_str = ', '.join(json.dumps(item, ensure_ascii=False) for item in sources)
    tags_str = ', '.join(json.dumps(item, ensure_ascii=False) for item in tags)

    return (
        f"  - name: {name}\n"
        f"    root: {root}\n"
        f"    description: {json.dumps(description, ensure_ascii=False)}\n"
        f"    auto_route:\n"
        f"      sources: [{sources_str}]\n"
        f"      tags: [{tags_str}]\n"
    )


def kb_init(root_name, name=None, description=None):
    """初始化一个新的多实例知识库并写回配置。"""
    config_path = _find_config_path()
    if not config_path:
        return {"status": "error", "message": "arc-reactor-config.yaml 未找到"}

    config = load_config()
    knowledge_bases = config.get('knowledge_bases', []) or []
    kb_name = name or root_name
    kb_description = description or ''

    for kb_entry in knowledge_bases:
        if kb_entry.get('name') == kb_name:
            return {"status": "error", "message": f"知识库名称已存在: {kb_name}"}
        if kb_entry.get('root') == root_name:
            return {"status": "error", "message": f"知识库根目录已存在: {root_name}"}

    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(config_path)))
    kb_root = os.path.join(workspace_root, root_name)
    dirs_to_create = [
        os.path.join(kb_root, 'wiki', 'sources'),
        os.path.join(kb_root, 'wiki', 'entities'),
        os.path.join(kb_root, 'wiki', 'concepts'),
        os.path.join(kb_root, 'raw'),
    ]
    files_to_create = [
        os.path.join(kb_root, 'wiki', 'index.md'),
        os.path.join(kb_root, 'wiki', 'log.md'),
    ]

    created = []
    try:
        for dir_path in dirs_to_create:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                created.append(dir_path)
        for file_path in files_to_create:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as file_obj:
                    file_obj.write('')
                created.append(file_path)

        new_entry = {
            'name': kb_name,
            'root': root_name,
            'description': kb_description,
            'auto_route': {
                'sources': [],
                'tags': [],
            },
        }

        with open(config_path, 'r', encoding='utf-8') as file_obj:
            config_text = file_obj.read().rstrip()

        yaml_entry = _format_kb_yaml_entry(new_entry)
        if 'knowledge_bases:' in config_text:
            updated_text = f"{config_text}\n\n{yaml_entry.rstrip()}\n"
        else:
            updated_text = f"{config_text}\n\nknowledge_bases:\n{yaml_entry}"

        with open(config_path, 'w', encoding='utf-8') as file_obj:
            file_obj.write(updated_text)

        return {
            "status": "success",
            "action": "kb_init",
            "name": kb_name,
            "root": root_name,
            "path": kb_root,
            "config": config_path,
            "created": created,
            "message": "Knowledge base initialized."
        }
    except Exception as exc:
        return {"status": "error", "message": f"知识库初始化失败: {str(exc)}"}


def kb_list():
    """列出所有已配置知识库的统计信息。"""
    config = load_config()
    knowledge_bases = config.get('knowledge_bases', []) or []
    config_path = _find_config_path()
    if not config_path:
        return []

    workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(config_path)))
    results = []

    for kb_entry in knowledge_bases:
        kb_root = os.path.join(workspace_root, kb_entry.get('root', ''))
        sources_dir = os.path.join(kb_root, 'wiki', 'sources')
        entities_dir = os.path.join(kb_root, 'wiki', 'entities')
        concepts_dir = os.path.join(kb_root, 'wiki', 'concepts')

        def count_markdown_files(root_dir):
            count = 0
            if not os.path.exists(root_dir):
                return count
            for _, _, files in os.walk(root_dir):
                count += sum(1 for filename in files if filename.endswith('.md'))
            return count

        latest_mtime = None
        if os.path.exists(kb_root):
            for root, _, files in os.walk(kb_root):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    file_mtime = os.path.getmtime(file_path)
                    if latest_mtime is None or file_mtime > latest_mtime:
                        latest_mtime = file_mtime

        results.append({
            'name': kb_entry.get('name'),
            'root': kb_entry.get('root'),
            'description': kb_entry.get('description', ''),
            'sources_count': count_markdown_files(sources_dir),
            'entities_count': count_markdown_files(entities_dir),
            'concepts_count': count_markdown_files(concepts_dir),
            'last_modified': datetime.fromtimestamp(latest_mtime).strftime('%Y-%m-%d %H:%M:%S') if latest_mtime else None,
            'exists': os.path.exists(kb_root),
        })

    return results

def slugify(text):
    """简单规范化文件名"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text if text else "untitled"

WIKI_LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def find_doc_root(start_path, root_name='arc-reactor-doc'):
    """Walk up from start_path to find the workspace root."""
    curr_dir = start_path
    while curr_dir and curr_dir != '/':
        if os.path.exists(os.path.join(curr_dir, root_name)):
            return os.path.join(curr_dir, root_name)
        if os.path.exists(os.path.join(curr_dir, '.git')):
            return os.path.join(curr_dir, root_name)
        curr_dir = os.path.dirname(curr_dir)
    return os.path.join(start_path, root_name)

def lint_wiki(doc_root, fix=False):
    """Health check for Wiki integrity. Returns issues found."""
    issues = []
    fixed = []
    
    wiki_dir = os.path.join(doc_root, 'wiki')
    if not os.path.exists(wiki_dir):
        return {"status": "error", "message": f"Wiki directory not found: {wiki_dir}"}
    
    # 1. Scan all entity files
    entities_dir = os.path.join(wiki_dir, 'entities')
    existing_entities = set()
    if os.path.exists(entities_dir):
        for f in os.listdir(entities_dir):
            if f.endswith('.md'):
                existing_entities.add(f[:-3])  # strip .md
    
    # 2. Scan all source files for wiki-links
    all_links = set()
    sources_dir = os.path.join(wiki_dir, 'sources')
    all_files = []
    
    # Collect all markdown files
    for root, dirs, files in os.walk(wiki_dir):
        for f in files:
            if f.endswith('.md'):
                all_files.append(os.path.join(root, f))
    
    for fpath in all_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find all [[wiki-links]]
                links = WIKI_LINK_RE.findall(content)
                for link in links:
                    slug = slugify(link)
                    all_links.add(slug)
                    
                    # Check for orphan links
                    if slug not in existing_entities:
                        rel_path = os.path.relpath(fpath, doc_root)
                        issues.append({
                            "type": "orphan_link",
                            "link": f"[[{link}]]",
                            "slug": slug,
                            "found_in": rel_path,
                            "fix": f"Create entity: wiki/entities/{slug}.md"
                        })
                        # Auto-fix: create stub entity
                        if fix and not os.path.exists(os.path.join(entities_dir, f"{slug}.md")):
                            stub = f"---\ndate: {datetime.now().strftime('%Y-%m-%d')}\n---\n\n# {link}\n\n> Stub entity — awaiting Ingest completion.\n"
                            stub_path = os.path.join(entities_dir, f"{slug}.md")
                            with open(stub_path, 'w', encoding='utf-8') as ef:
                                ef.write(stub)
                            fixed.append(f"Created stub: wiki/entities/{slug}.md")
        except Exception:
            continue
    
    # 3. Check entities not in index.md
    index_path = os.path.join(wiki_dir, 'index.md')
    indexed_entities = set()
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
            indexed_links = WIKI_LINK_RE.findall(index_content)
            for link in indexed_links:
                indexed_entities.add(slugify(link))
    
    for entity in existing_entities:
        if entity not in indexed_entities:
            issues.append({
                "type": "missing_from_index",
                "entity": entity,
                "fix": f"Add [[{entity}]] to wiki/index.md"
            })
    
    # 4. Check source files missing date
    if os.path.exists(sources_dir):
        for root, dirs, files in os.walk(sources_dir):
            for f in files:
                if f.endswith('.md'):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as sf:
                            content = sf.read()
                            if 'date:' not in content[:500].lower():
                                rel_path = os.path.relpath(fpath, doc_root)
                                issues.append({
                                    "type": "missing_date",
                                    "file": rel_path,
                                    "fix": "Add date field to frontmatter"
                                })
                    except Exception:
                        continue
    
    # 5. Check for empty files (< 50 bytes)
    for fpath in all_files:
        try:
            if os.path.getsize(fpath) < 50:
                rel_path = os.path.relpath(fpath, doc_root)
                issues.append({
                    "type": "empty_file",
                    "file": rel_path,
                    "fix": "Populate or remove empty file"
                })
        except Exception:
            continue
    
    return {
        "status": "lint_complete",
        "total_files": len(all_files),
        "total_entities": len(existing_entities),
        "total_links": len(all_links),
        "issues_found": len(issues),
        "issues_fixed": len(fixed),
        "issues": issues,
        "fixed": fixed
    }

def main():
    parser = argparse.ArgumentParser(description='ARC Reactor V4 Archive Manager (Karpathy Wiki Edition)')
    parser.add_argument('--lint', action='store_true', help='Run Wiki health check')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues found during lint')
    parser.add_argument('--kb-init', action='store_true', help='初始化新的知识库实例')
    parser.add_argument('--kb-list', action='store_true', help='列出所有已配置知识库')
    parser.add_argument('--type', choices=[
        'raw', 'source', 'entity', 'concept', 'index', 'log', 'template'
    ], required=False, help='归档进入的 Wiki 圈层类型')
    
    parser.add_argument('--topic', required=False, default='knowledge-node', help='话题/实体名 (用于生成文件名)')
    parser.add_argument('--stdin', action='store_true', help='强制通过标准输入读取内容 (防止转义错误)')
    parser.add_argument('--root', default='arc-reactor-doc', help='文档根目录名称')
    parser.add_argument('--name', required=False, default=None, help='KB 显示名称，仅用于 --kb-init')
    parser.add_argument('--description', required=False, default=None, help='KB 描述，仅用于 --kb-init')
    parser.add_argument('--date', required=False, default=None, help='指定的日期戳，缺省为今日')
    parser.add_argument('--dedup', choices=['merge', 'skip', 'overwrite'], default='overwrite',
                        help='去重策略: merge=增量合并, skip=跳过, overwrite=覆盖(默认)')

    args = parser.parse_args()

    if args.kb_init:
        result = kb_init(args.root, name=args.name, description=args.description)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.kb_list:
        result = kb_list()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Lint mode — separate flow
    if args.lint:
        cwd = os.getcwd()
        doc_root = find_doc_root(cwd, args.root)
        result = lint_wiki(doc_root, fix=args.fix)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # Normal archive mode — type is required
    if not args.type:
        print(json.dumps({"status": "error", "message": "归档模式需要 --type 参数，或使用 --lint / --kb-init / --kb-list"}))
        sys.exit(1)

    # 0. 预计算常用值
    topic_slug = slugify(args.topic)
    now_date = datetime.now().strftime('%Y-%m-%d')
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
    doc_root = find_doc_root(cwd, args.root)

    target_dir = ""
    filename = ""
    # topic_slug already computed above
    
    # Wiki 层路由判定
    if args.type == 'raw':
        target_dir = os.path.join(doc_root, 'raw')
        filename = f"{topic_slug}.md"
    elif args.type == 'source':
        date_dir = args.date if args.date else now_date
        target_dir = os.path.join(doc_root, 'wiki', 'sources', date_dir)
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
    # now_str and now_date already computed above

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
        
    # 自动探测并注入 Frontmatter 时间戳 (仅对新建的 Markdown 有效)
    if mode == 'w' and args.type in ['source', 'entity', 'concept', 'raw']:
        content_stripped = final_write_content.lstrip()
        if content_stripped.startswith('---'):
            lines = content_stripped.splitlines()
            # 扫描前20行看有没有 date: 字段
            has_date = any(line.lower().startswith('date:') for line in lines[:20])
            if not has_date and len(lines) > 1:
                # 在第一行 --- 下面插入 date
                lines.insert(1, f"date: {now_date}")
                final_write_content = "\n".join(lines)
        else:
            # 完全没有 YAML Frontmatter 格式，强制注入一个
            final_write_content = f"---\ndate: {now_date}\n---\n\n" + content_stripped

    # 4.5 去重检查 (dedup check)
    dedup_status = "new"
    if os.path.exists(target_path) and args.dedup != 'overwrite':
        existing_size = os.path.getsize(target_path)
        if args.dedup == 'skip':
            with open(target_path, 'rb') as ef:
                existing_checksum = hashlib.sha256(ef.read()).hexdigest()
            receipt = {
                "status": "skipped",
                "dedup": "skipped",
                "type_routed": args.type,
                "path": target_path,
                "size_bytes": existing_size,
                "checksum": existing_checksum,
                "message": f"Entity already exists ({existing_size} bytes). Skipped per --dedup skip."
            }
            print(json.dumps(receipt, ensure_ascii=False))
            sys.exit(0)
        elif args.dedup == 'merge':
            # For entity/concept: append (mode already set above)
            # For source: refuse to merge, warn instead
            if args.type == 'source':
                receipt = {
                    "status": "skipped",
                    "dedup": "source_exists",
                    "type_routed": args.type,
                    "path": target_path,
                    "message": f"Source already exists. Use --dedup overwrite to replace, or pick a different topic."
                }
                print(json.dumps(receipt, ensure_ascii=False))
                sys.exit(0)
            dedup_status = "merged"

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
            "dedup": dedup_status,
            "type_routed": args.type,
            "path": target_path,
            "size_bytes": size_bytes,
            "checksum": checksum,
            "date": now_date,
            "message": "Karpathy Wiki Layer write valid."
        }
        print(json.dumps(receipt, ensure_ascii=False))
        sys.exit(0)

    except Exception as e:
        print(json.dumps({"status": "error", "message": f"I/O 崩溃: {str(e)}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
