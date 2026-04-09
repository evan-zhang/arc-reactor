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

WIKI_LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')

def load_config(config_path=None):
    """Load arc-reactor-config.yaml (stdlib yaml subset – simple key:value only)."""
    if config_path is None:
        # Walk up to find config alongside skill dir
        cur = os.path.dirname(os.path.abspath(__file__))
        for _ in range(5):
            candidate = os.path.join(cur, 'arc-reactor-config.yaml')
            if os.path.exists(candidate):
                config_path = candidate
                break
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    if config_path is None or not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return _parse_simple_yaml(f.read())
    except Exception:
        return {}


def _parse_simple_yaml(text):
    """Minimal YAML parser for the config format we use (lists of dicts with nested lists).
    Handles: top-level key:, list items with - key: value, and nested list values."""
    import re as _re
    result = {}
    current_key = None
    current_list_items = []
    current_item = {}
    in_list = False
    in_nested_list = False
    nested_key = None
    nested_items = []

    for line in text.splitlines():
        stripped = line.rstrip()
        if not stripped or stripped.lstrip().startswith('#'):
            # Flush current item if we had one
            if in_list and current_item:
                if nested_key and nested_items:
                    current_item[nested_key] = nested_items
                current_list_items.append(current_item)
                current_item = {}
                nested_key = None
                nested_items = []
                in_nested_list = False
            continue

        indent = len(stripped) - len(stripped.lstrip())

        # Top-level key: value (indent 0)
        if indent == 0 and ':' in stripped:
            # Flush previous list
            if in_list and current_list_items:
                if current_item:
                    if nested_key and nested_items:
                        current_item[nested_key] = nested_items
                    current_list_items.append(current_item)
                    current_item = {}
                    nested_key = None
                    nested_items = []
                result[current_key] = current_list_items
                current_list_items = []
                in_list = False
                in_nested_list = False

            key, _, val = stripped.partition(':')
            key = key.strip()
            val = val.strip()
            if val:
                result[key] = val.strip('"').strip("'")
            else:
                current_key = key
                current_list_items = []
                in_list = True
                current_item = {}
            continue

        # List item at indent 2 (  - ...)
        if in_list and stripped.lstrip().startswith('- ') and indent <= 4:
            # Flush previous item
            if current_item:
                if nested_key and nested_items:
                    current_item[nested_key] = nested_items
                current_list_items.append(current_item)
                nested_key = None
                nested_items = []
                in_nested_list = False
            current_item = {}
            remainder = stripped.lstrip()[2:].strip()
            if ':' in remainder:
                k, _, v = remainder.partition(':')
                current_item[k.strip()] = v.strip().strip('"').strip("'")
            continue

        # Nested key inside list item (indent 4+)
        if in_list and indent >= 4 and ':' in stripped:
            k, _, v = stripped.strip().partition(':')
            k = k.strip()
            v = v.strip()
            if v:
                # Could be a list like: sources: ["a", "b"]
                if v.startswith('[') and v.endswith(']'):
                    items = _re.findall(r'"([^"]*)"', v)
                    if not items:
                        items = _re.findall(r"'([^']*)'", v)
                    if not items:
                        items = [x.strip().strip('"').strip("'") for x in v[1:-1].split(',')]
                    current_item[k] = items
                else:
                    current_item[k] = v.strip('"').strip("'")
            else:
                # Nested list follows
                if nested_key and nested_items:
                    current_item[nested_key] = nested_items
                nested_key = k
                nested_items = []
                in_nested_list = True
            continue

        # Items inside nested list (indent 6+, with - or just values)
        if in_nested_list and indent >= 6:
            val = stripped.strip().lstrip('- ').strip().strip('"').strip("'")
            if val:
                nested_items.append(val)
            continue

    # Final flush
    if in_list:
        if current_item:
            if nested_key and nested_items:
                current_item[nested_key] = nested_items
            current_list_items.append(current_item)
        result[current_key] = current_list_items

    return result


def resolve_kb_root(content_source, tags=None):
    """Resolve which KB root directory should be used based on content source and tags.

    Args:
        content_source: string like "cwork-api", "web_fetch"
        tags: list of tag strings

    Returns:
        matched root directory name, or None if no match found.
    """
    config = load_config()
    knowledge_bases = config.get('knowledge_bases', [])
    if isinstance(knowledge_bases, dict):
        knowledge_bases = [knowledge_bases]
    if not knowledge_bases:
        return None

    tags = tags or []

    # Priority 1: match by source
    for kb in knowledge_bases:
        auto_route = kb.get('auto_route', {})
        if isinstance(auto_route, dict):
            sources = auto_route.get('sources', [])
            if content_source in sources:
                return kb.get('root')

    # Priority 2: match by tag
    for kb in knowledge_bases:
        auto_route = kb.get('auto_route', {})
        if isinstance(auto_route, dict):
            kb_tags = auto_route.get('tags', [])
            if any(t in kb_tags for t in tags):
                return kb.get('root')

    return None


def kb_init(args):
    """Create a new knowledge base directory structure and register it in config."""
    cwd = os.getcwd()

    # Resolve config path
    config_dir = os.path.dirname(os.path.abspath(__file__))
    for _ in range(5):
        candidate = os.path.join(config_dir, 'arc-reactor-config.yaml')
        if os.path.exists(candidate):
            config_path = candidate
            break
        parent = os.path.dirname(config_dir)
        if parent == config_dir:
            break
        config_dir = parent
    else:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arc-reactor-config.yaml')

    root_name = args.root
    name = args.name or root_name
    description = args.description or ""

    # Create directory structure relative to cwd (where the KB will live)
    kb_root = os.path.join(cwd, root_name)
    dirs_to_create = [
        os.path.join(kb_root, 'wiki', 'sources'),
        os.path.join(kb_root, 'wiki', 'entities'),
        os.path.join(kb_root, 'wiki', 'concepts'),
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    # Create index.md if not exists
    index_path = os.path.join(kb_root, 'wiki', 'index.md')
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# {name} — Knowledge Index\n\n> Auto-generated by ARC Reactor kb-init\n")

    # Create log.md if not exists
    log_path = os.path.join(kb_root, 'wiki', 'log.md')
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as f:
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"# {name} — Activity Log\n\n- **[{now_str}]** KB initialized via kb-init\n")

    # Update config.yaml — append to knowledge_bases list
    new_entry = f"""
  - name: {name}
    root: {root_name}
    description: "{description}"
"""
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'knowledge_bases:' in content:
            # Append to existing list
            content = content.rstrip() + '\n' + new_entry
        else:
            # Add new section
            content = content.rstrip() + '\n\nknowledge_bases:\n' + new_entry

        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        # Create new config with the entry
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(f"knowledge_bases:\n{new_entry}\n")

    return {
        "status": "success",
        "action": "kb_init",
        "kb_name": name,
        "root": root_name,
        "path": kb_root,
        "dirs_created": dirs_to_create,
        "config_updated": config_path,
        "message": f"Knowledge base '{name}' initialized at {root_name}/"
    }


def kb_list(args):
    """List all registered knowledge bases with statistics."""
    config = load_config()
    knowledge_bases = config.get('knowledge_bases', [])
    if isinstance(knowledge_bases, dict):
        knowledge_bases = [knowledge_bases]

    cwd = os.getcwd()
    results = []

    for kb in knowledge_bases:
        root_name = kb.get('root', '')
        kb_root = os.path.join(cwd, root_name)

        # Count sources
        source_count = 0
        sources_dir = os.path.join(kb_root, 'wiki', 'sources')
        if os.path.exists(sources_dir):
            for dirpath, dirnames, filenames in os.walk(sources_dir):
                source_count += sum(1 for f in filenames if f.endswith('.md'))

        # Count entities
        entity_count = 0
        entities_dir = os.path.join(kb_root, 'wiki', 'entities')
        if os.path.exists(entities_dir):
            entity_count = sum(1 for f in os.listdir(entities_dir) if f.endswith('.md'))

        # Last modified time
        last_updated = None
        wiki_dir = os.path.join(kb_root, 'wiki')
        if os.path.exists(wiki_dir):
            latest_mtime = 0
            for dirpath, dirnames, filenames in os.walk(wiki_dir):
                for fname in filenames:
                    fpath = os.path.join(dirpath, fname)
                    try:
                        mtime = os.path.getmtime(fpath)
                        if mtime > latest_mtime:
                            latest_mtime = mtime
                    except OSError:
                        continue
            if latest_mtime > 0:
                last_updated = datetime.fromtimestamp(latest_mtime).strftime('%Y-%m-%d %H:%M:%S')

        results.append({
            "name": kb.get('name', ''),
            "root": root_name,
            "description": kb.get('description', ''),
            "source_count": source_count,
            "entity_count": entity_count,
            "last_updated": last_updated,
            "exists": os.path.exists(kb_root),
        })

    return {
        "status": "success",
        "action": "kb_list",
        "total_kbs": len(results),
        "knowledge_bases": results
    }


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

def _parse_simple_yaml(filepath):
    """Parse a simple YAML file (stdlib only). Handles top-level scalars and nested lists/dicts up to 3 levels."""
    result = {}
    current_key = None
    current_list = None
    current_dict = None
    nested_key = None
    in_list = False
    in_nested_dict = False

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                stripped = line.rstrip()
                if not stripped or stripped.startswith('#'):
                    continue

                # Nested dict value (e.g. "      sources: [...]")
                if in_nested_dict and stripped.startswith('      '):
                    val = stripped.strip()
                    if nested_key and current_dict is not None:
                        if val.startswith('[') and val.endswith(']'):
                            items = [x.strip().strip('"').strip("'") for x in val[1:-1].split(',')]
                            current_dict[nested_key] = items
                        else:
                            current_dict[nested_key] = val.strip('"').strip("'")
                    continue

                # List item under nested dict
                if in_nested_dict and stripped.startswith('        '):
                    continue

                # Nested dict key (e.g. "    auto_route:")
                if in_list and stripped.startswith('    ') and not stripped.startswith('      '):
                    val = stripped.strip()
                    if val.endswith(':'):
                        nk = val[:-1].strip()
                        if current_dict is None:
                            current_dict = {}
                        current_dict[nk] = None
                        nested_key = nk
                        in_nested_dict = True
                        continue
                    else:
                        # key: value
                        parts = val.split(':', 1)
                        if len(parts) == 2:
                            k = parts[0].strip()
                            v = parts[1].strip().strip('"').strip("'")
                            if current_dict is None:
                                current_dict = {}
                            current_dict[k] = v
                        continue

                # List item (e.g. "  - name: ...")
                if in_list and stripped.startswith('  - '):
                    # Save previous dict if any
                    if current_dict is not None and current_key and current_list is not None:
                        current_list.append(current_dict)
                    current_dict = {}
                    in_nested_dict = False
                    nested_key = None
                    val = stripped[4:].strip()
                    if ':' in val:
                        parts = val.split(':', 1)
                        k = parts[0].strip()
                        v = parts[1].strip().strip('"').strip("'")
                        current_dict[k] = v
                    continue

                # Top-level key
                if ':' in stripped and not stripped.startswith(' '):
                    # Save previous list/dict
                    if in_list and current_dict is not None and current_key:
                        current_list.append(current_dict)
                    in_list = False
                    in_nested_dict = False
                    nested_key = None

                    parts = stripped.split(':', 1)
                    current_key = parts[0].strip()
                    val = parts[1].strip() if len(parts) > 1 else ''
                    if not val:
                        current_list = []
                        in_list = True
                        current_dict = None
                    else:
                        result[current_key] = val.strip('"').strip("'")

        # Save final list item
        if in_list and current_dict is not None and current_key:
            current_list.append(current_dict)
            result[current_key] = current_list

    except FileNotFoundError:
        pass
    return result

def load_config(start_path=None):
    """Load arc-reactor-config.yaml. Returns parsed dict."""
    if start_path is None:
        start_path = os.getcwd()
    config_path = None
    curr = start_path
    while curr and curr != '/':
        candidate = os.path.join(curr, 'arc-reactor-config.yaml')
        if os.path.exists(candidate):
            config_path = candidate
            break
        # Also check in skills/arc-reactor/
        candidate2 = os.path.join(curr, 'skills', 'arc-reactor', 'arc-reactor-config.yaml')
        if os.path.exists(candidate2):
            config_path = candidate2
            break
        if os.path.exists(os.path.join(curr, '.git')):
            break
        curr = os.path.dirname(curr)
    if not config_path:
        return {}
    return _parse_simple_yaml(config_path)

def resolve_kb_root(content_source, tags=None):
    """Given a content source and tags, return the matching KB root directory or None."""
    config = load_config()
    kb_list = config.get('knowledge_bases', [])
    if isinstance(kb_list, dict):
        kb_list = [kb_list]
    if tags is None:
        tags = []

    for kb in kb_list:
        if not isinstance(kb, dict):
            continue
        auto_route = kb.get('auto_route', {})
        if not isinstance(auto_route, dict):
            continue
        # Priority 1: source match
        sources = auto_route.get('sources', [])
        if isinstance(sources, str):
            sources = [sources]
        if content_source in sources:
            return kb.get('root', None)
        # Priority 2: tag match
        route_tags = auto_route.get('tags', [])
        if isinstance(route_tags, str):
            route_tags = [route_tags]
        for t in tags:
            if t in route_tags:
                return kb.get('root', None)
    return None

def kb_init(root_name, name=None, description=None):
    """Initialize a new knowledge base directory structure and update config."""
    cwd = os.getcwd()
    # Create directory structure
    kb_root = os.path.join(cwd, root_name)
    dirs_to_create = [
        os.path.join(kb_root, 'wiki', 'sources'),
        os.path.join(kb_root, 'wiki', 'entities'),
        os.path.join(kb_root, 'wiki', 'concepts'),
        os.path.join(kb_root, 'raw'),
    ]
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    # Create index.md if not exists
    index_path = os.path.join(kb_root, 'wiki', 'index.md')
    if not os.path.exists(index_path):
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# Knowledge Base Index: {name or root_name}\n\n")

    # Create log.md if not exists
    log_path = os.path.join(kb_root, 'wiki', 'log.md')
    if not os.path.exists(log_path):
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Knowledge Base Log: {name or root_name}\n\n")

    # Update config.yaml — find and append knowledge_bases entry
    config_updated = False
    config_path = None
    curr = cwd
    while curr and curr != '/':
        for candidate in [
            os.path.join(curr, 'arc-reactor-config.yaml'),
            os.path.join(curr, 'skills', 'arc-reactor', 'arc-reactor-config.yaml'),
        ]:
            if os.path.exists(candidate):
                config_path = candidate
                break
        if config_path:
            break
        if os.path.exists(os.path.join(curr, '.git')):
            break
        curr = os.path.dirname(curr)

    if config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'knowledge_bases' not in content:
            content += "\n\nknowledge_bases:\n"
        # Append new KB entry
        entry = f"\n  - name: {name or root_name}\n"
        entry += f"    root: {root_name}\n"
        entry += f"    description: \"{description or ''}\"\n"
        content += entry
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        config_updated = True

    return {
        "status": "success",
        "action": "kb_init",
        "root": root_name,
        "path": kb_root,
        "name": name or root_name,
        "description": description or "",
        "dirs_created": dirs_to_create,
        "config_updated": config_updated,
        "config_path": config_path,
        "message": f"Knowledge base '{name or root_name}' initialized at {kb_root}"
    }

def kb_list():
    """List all configured knowledge bases with stats."""
    config = load_config()
    kb_entries = config.get('knowledge_bases', [])
    if isinstance(kb_entries, dict):
        kb_entries = [kb_entries]

    cwd = os.getcwd()
    results = []
    for kb in kb_entries:
        if not isinstance(kb, dict):
            continue
        root = kb.get('root', '')
        kb_path = os.path.join(cwd, root)
        stats = {"sources": 0, "entities": 0, "concepts": 0, "last_updated": None}
        if os.path.exists(kb_path):
            # Count sources
            sources_dir = os.path.join(kb_path, 'wiki', 'sources')
            if os.path.exists(sources_dir):
                for dirpath, dirnames, filenames in os.walk(sources_dir):
                    stats["sources"] += sum(1 for f in filenames if f.endswith('.md'))
            # Count entities
            entities_dir = os.path.join(kb_path, 'wiki', 'entities')
            if os.path.exists(entities_dir):
                stats["entities"] = sum(1 for f in os.listdir(entities_dir) if f.endswith('.md'))
            # Count concepts
            concepts_dir = os.path.join(kb_path, 'wiki', 'concepts')
            if os.path.exists(concepts_dir):
                stats["concepts"] = sum(1 for f in os.listdir(concepts_dir) if f.endswith('.md'))
            # Last updated
            last_mtime = 0
            for dirpath, dirnames, filenames in os.walk(kb_path):
                for fn in filenames:
                    fp = os.path.join(dirpath, fn)
                    try:
                        mt = os.path.getmtime(fp)
                        if mt > last_mtime:
                            last_mtime = mt
                    except OSError:
                        pass
            if last_mtime:
                stats["last_updated"] = datetime.fromtimestamp(last_mtime).strftime('%Y-%m-%d %H:%M')
        results.append({
            "name": kb.get('name', ''),
            "root": root,
            "description": kb.get('description', ''),
            "exists": os.path.exists(kb_path),
            "stats": stats
        })
    return results

def main():
    parser = argparse.ArgumentParser(description='ARC Reactor V4 Archive Manager (Karpathy Wiki Edition)')
    parser.add_argument('--lint', action='store_true', help='Run Wiki health check')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues found during lint')
    parser.add_argument('--kb-init', action='store_true', help='Initialize a new knowledge base')
    parser.add_argument('--kb-list', action='store_true', help='List all registered knowledge bases')
    parser.add_argument('--name', required=False, default=None, help='KB display name (used with --kb-init)')
    parser.add_argument('--description', required=False, default=None, help='KB description (used with --kb-init)')
    parser.add_argument('--type', choices=[
        'raw', 'source', 'entity', 'concept', 'index', 'log', 'template'
    ], required=False, help='归档进入的 Wiki 圈层类型')
    
    parser.add_argument('--topic', required=False, default='knowledge-node', help='话题/实体名 (用于生成文件名)')
    parser.add_argument('--stdin', action='store_true', help='强制通过标准输入读取内容 (防止转义错误)')
    parser.add_argument('--root', default='arc-reactor-doc', help='文档根目录名称')
    parser.add_argument('--date', required=False, default=None, help='指定的日期戳，缺省为今日')
    parser.add_argument('--dedup', choices=['merge', 'skip', 'overwrite'], default='overwrite',
                        help='去重策略: merge=增量合并, skip=跳过, overwrite=覆盖(默认)')
    # Multi-KB commands
    parser.add_argument('--kb-init', action='store_true', help='Initialize a new knowledge base')
    parser.add_argument('--kb-list', action='store_true', help='List all configured knowledge bases')
    parser.add_argument('--name', required=False, default=None, help='KB display name (for --kb-init)')
    parser.add_argument('--description', required=False, default=None, help='KB description (for --kb-init)')

    args = parser.parse_args()

    # KB-Init mode
    if args.kb_init:
        result = kb_init(args.root, name=args.name, description=args.description)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # KB-List mode
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

    # KB init mode
    if args.kb_init:
        result = kb_init(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    # KB list mode
    if args.kb_list:
        result = kb_list(args)
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
