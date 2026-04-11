#!/usr/bin/env python3
"""
compile-report.py — ARC Reactor 结构化报告生成器

强制执行多维分析框架，输出符合 JSON Schema 的结构化报告。

Usage:
    cat raw_content.txt | python3 compile-report.py --topic "Topic Name" --raw - --output report.json
    python3 compile-report.py --topic "Topic Name" --raw /path/to/content.txt --output report.json
"""

import sys
import json
import argparse
import os
import re
from pathlib import Path

# LLM provider detection
HAS_ANTHROPIC = False
HAS_OPENAI = False
HAS_GEMINI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    pass

try:
    from openai import OpenAI as OpenAIClient
    HAS_OPENAI = True
except ImportError:
    pass

try:
    import google.genai as genai
    import google.genai.models as models
    HAS_GEMINI = True
except ImportError:
    try:
        import google.ai.generativelanguage as gal
        HAS_GEMINI = True
    except ImportError:
        pass

# ============ Configuration ============
MODEL_CONFIG = {
    "default": "google/gemini-2.0-flash",
    "fast": "google/gemini-2.0-flash",
    "quality": "anthropic/claude-sonnet-4-5",
}

ANALYSIS_PROMPT = """## 角色
你是一个专业的技术调研分析师。你的任务是对给定的原始内容进行深度分析，并按照规定的 JSON Schema 输出结构化报告。

## 强制要求
1. 你必须为所有字段提供内容，禁止省略任何字段
2. summary 必须 ≤100字，用一句话概括核心内容
3. key_findings 至少3条，每条要有信息增量（不是重复摘要）
4. structure 的四个子字段都必须有实质内容
5. alternatives 至少列出1个替代方案
6. actionable 必须给出可操作的建议（不是泛泛而谈）
7. 所有字数限制是硬限制，必须遵守

## 分析维度指导

### background（背景）
- 这是什么项目/技术？
- 解决了什么痛点？
- 背景是什么（谁做的？为什么做？）

### principle（原理/机制）
- 核心技术原理是什么？
- 关键机制是怎样的？
- 和传统方案有什么本质区别？

### implementation（实现方式）
- 如何落地的？
- 核心代码/架构是怎样的？
- 技术栈是什么？

### evaluation（优缺点评价）
- 优点：至少2点，要有具体数据或案例支撑
- 缺点：至少2点，要客观
- 局限性：边界在哪里？

### alternatives（替代方案）
- 同类竞品有哪些？
- 各有什么优劣？
- 为什么选这个而不是其他的？

### credibility（可信度评级）
- HIGH：数据有官方/第三方佐证
- MEDIUM：部分数据可验证，部分来自作者声称
- LOW：数据主要来自作者声称，无第三方验证

## 输出格式
你必须输出一个有效的 JSON 对象，符合上述 Schema。
不要输出任何其他内容，只输出 JSON。
"""

MAX_RETRIES = 3
# ============ Configuration End ============


def load_raw_content(raw_path: str) -> str:
    """Load raw content from file or stdin."""
    if raw_path == "-":
        return sys.stdin.read()
    
    path = Path(raw_path)
    if not path.exists():
        print(json.dumps({
            "status": "error",
            "message": f"Raw content file not found: {raw_path}"
        }), file=sys.stderr)
        sys.exit(1)
    
    return path.read_text(encoding="utf-8")


def build_analysis_prompt(raw_content: str, topic: str) -> str:
    """Build the complete analysis prompt."""
    return f"""{ANALYSIS_PROMPT}

---

## 原始内容（需要分析的材料）

topic: {topic}

---

{raw_content}

---

## 输出要求
严格按照上述 Schema 输出 JSON。确保所有 required 字段都存在且有效。
"""


def call_llm(prompt: str, model: str = None) -> str:
    """Call LLM with the given prompt. Supports multiple providers."""
    model = model or MODEL_CONFIG["default"]
    
    # Parse provider/model
    if "/" in model:
        provider, model_name = model.split("/", 1)
    else:
        provider = "unknown"
        model_name = model
    
    # Google Gemini
    if provider in ("google", "gemini") and HAS_GEMINI:
        try:
            client = genai.Client()
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(json.dumps({
                "status": "warning",
                "message": f"Gemini call failed: {e}. Falling back."
            }), file=sys.stderr)
    
    # OpenAI
    if provider == "openai" and HAS_OPENAI:
        try:
            client = OpenAIClient()
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(json.dumps({
                "status": "warning",
                "message": f"OpenAI call failed: {e}. Falling back."
            }), file=sys.stderr)
    
    # Anthropic
    if provider == "anthropic" and HAS_ANTHROPIC:
        try:
            client = anthropic.Anthropic()
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(json.dumps({
                "status": "warning",
                "message": f"Anthropic call failed: {e}. Falling back."
            }), file=sys.stderr)
    
    # Fallback: return a structured template (for testing only)
    print(json.dumps({
        "status": "warning",
        "message": "No LLM provider available. Using structured template fallback."
    }), file=sys.stderr)
    
    return json.dumps({
        "topic": topic,
        "summary": f"[Fallback] Summary for {topic}",
        "key_findings": [
            "Finding 1: This is a fallback response",
            "Finding 2: No LLM provider was available",
            "Finding 3: Please configure an LLM provider"
        ],
        "structure": {
            "background": f"Background for {topic} (fallback mode)",
            "principle": f"Principle of {topic} (fallback mode)",
            "implementation": f"Implementation of {topic} (fallback mode)",
            "evaluation": f"Evaluation of {topic} (fallback mode)"
        },
        "credibility": {
            "rating": "LOW",
            "verified": [],
            "disputed": ["Fallback mode - no real analysis"],
            "unverified": ["All content is placeholder"]
        },
        "alternatives": ["Alternative 1 (fallback)"],
        "actionable": "Configure LLM provider for real analysis"
    })


def extract_json(text: str) -> str:
    """Extract JSON from potentially wrapped text."""
    text = text.strip()
    
    # Handle markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last line if they are code fences
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    
    # Try to find JSON object
    json_match = re.search(r'\{[\s\S]*\}', text)
    if json_match:
        return json_match.group(0)
    
    return text


def validate_output(json_str: str) -> tuple:
    """Validate output against schema. Returns (is_valid, message, data)."""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}", {}
    
    # Check required fields
    required_fields = [
        "topic", "summary", "key_findings", 
        "structure", "credibility", "alternatives", "actionable"
    ]
    
    missing = [f for f in required_fields if f not in data]
    if missing:
        return False, f"Missing required fields: {missing}", {}
    
    # Check key_findings
    if not isinstance(data.get("key_findings"), list) or len(data["key_findings"]) < 3:
        return False, "key_findings must have at least 3 items", {}
    
    # Check structure
    structure_fields = ["background", "principle", "implementation", "evaluation"]
    if "structure" not in data or not isinstance(data["structure"], dict):
        return False, "structure must be a dict", {}
    
    structure_missing = [f for f in structure_fields if f not in data["structure"]]
    if structure_missing:
        return False, f"Missing structure fields: {structure_missing}", {}
    
    # Check alternatives
    if not isinstance(data.get("alternatives"), list) or len(data["alternatives"]) < 1:
        return False, "alternatives must have at least 1 item", {}
    
    # Check credibility
    credibility_required = ["rating", "verified", "disputed", "unverified"]
    if "credibility" not in data or not isinstance(data["credibility"], dict):
        return False, "credibility must be a dict", {}
    
    cred_missing = [f for f in credibility_required if f not in data["credibility"]]
    if cred_missing:
        return False, f"Missing credibility fields: {cred_missing}", {}
    
    return True, "Valid", data


def compile_report(raw_content: str, topic: str, model: str = None) -> dict:
    """Main compilation flow."""
    prompt = build_analysis_prompt(raw_content, topic)
    
    for attempt in range(MAX_RETRIES):
        raw_output = call_llm(prompt, model)
        json_str = extract_json(raw_output)
        
        is_valid, message, data = validate_output(json_str)
        
        if is_valid:
            return {
                "status": "success",
                "topic": topic,
                "report": data,
                "attempts": attempt + 1
            }
        
        print(json.dumps({
            "status": "retry",
            "attempt": attempt + 1,
            "reason": message
        }), file=sys.stderr)
    
    # All retries failed
    print(json.dumps({
        "status": "error",
        "message": f"Failed after {MAX_RETRIES} attempts. Last error: {message}"
    }), file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="ARC Reactor 结构化报告生成器 — 强制执行多维分析框架"
    )
    parser.add_argument(
        "--topic", 
        required=True, 
        help="主题名称"
    )
    parser.add_argument(
        "--raw", 
        required=True, 
        help="原始内容文件路径（或 '-' 读取 stdin）"
    )
    parser.add_argument(
        "--model", 
        help="指定模型（provider/name 格式，如 google/gemini-2.0-flash）"
    )
    parser.add_argument(
        "--output", 
        help="输出文件路径（默认为 stdout）"
    )
    
    args = parser.parse_args()
    
    # Load raw content
    raw_content = load_raw_content(args.raw)
    
    # Compile report
    result = compile_report(raw_content, args.topic, args.model)
    
    # Output
    output = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(json.dumps({
            "status": "success",
            "output": args.output,
            "topic": args.topic
        }))
    else:
        print(output)


if __name__ == "__main__":
    main()
