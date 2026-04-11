#!/usr/bin/env python3
"""
compile-report.py — ARC Reactor 结构化报告生成器

强制执行多维分析框架，输出符合 JSON Schema 的结构化报告。

Usage:
    cat raw_content.txt | python3 compile-report.py --topic "Topic Name" --raw - --output report.json
    python3 compile-report.py --topic "Topic Name" --raw /path/to/content.txt --output report.json
"""

import argparse
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HAS_ANTHROPIC = False
HAS_OPENAI = False
HAS_GEMINI = False

genai = None
genai_types = None
anthropic = None
OpenAIClient = None

try:
    import anthropic  # type: ignore
    HAS_ANTHROPIC = True
except ImportError:
    pass

try:
    from openai import OpenAI as OpenAIClient  # type: ignore
    HAS_OPENAI = True
except ImportError:
    pass

try:
    import google.genai as genai  # type: ignore
    try:
        from google.genai import types as genai_types  # type: ignore
    except ImportError:
        genai_types = None
    HAS_GEMINI = True
except ImportError:
    pass

MODEL_CONFIG = {
    "default": "google/gemini-2.0-flash",
    "fast": "google/gemini-2.0-flash",
    "quality": "anthropic/claude-sonnet-4-5",
}

MAX_RETRIES = 3

REPORT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "topic",
        "summary",
        "key_findings",
        "structure",
        "credibility",
        "alternatives",
        "actionable",
    ],
    "properties": {
        "topic": {"type": "string", "minLength": 1, "maxLength": 200},
        "summary": {"type": "string", "minLength": 1, "maxLength": 100},
        "key_findings": {
            "type": "array",
            "minItems": 3,
            "maxItems": 8,
            "items": {"type": "string", "minLength": 10, "maxLength": 280},
        },
        "structure": {
            "type": "object",
            "additionalProperties": False,
            "required": ["background", "principle", "implementation", "evaluation"],
            "properties": {
                "background": {"type": "string", "minLength": 20, "maxLength": 3000},
                "principle": {"type": "string", "minLength": 20, "maxLength": 3000},
                "implementation": {"type": "string", "minLength": 20, "maxLength": 3000},
                "evaluation": {"type": "string", "minLength": 20, "maxLength": 3000},
            },
        },
        "credibility": {
            "type": "object",
            "additionalProperties": False,
            "required": ["rating", "verified", "disputed", "unverified"],
            "properties": {
                "rating": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
                "verified": {
                    "type": "array",
                    "maxItems": 10,
                    "items": {"type": "string", "minLength": 1, "maxLength": 200},
                },
                "disputed": {
                    "type": "array",
                    "maxItems": 10,
                    "items": {"type": "string", "minLength": 1, "maxLength": 200},
                },
                "unverified": {
                    "type": "array",
                    "maxItems": 10,
                    "items": {"type": "string", "minLength": 1, "maxLength": 200},
                },
            },
        },
        "alternatives": {
            "type": "array",
            "minItems": 1,
            "maxItems": 8,
            "items": {"type": "string", "minLength": 1, "maxLength": 200},
        },
        "actionable": {"type": "string", "minLength": 10, "maxLength": 1000},
    },
}

ANALYSIS_PROMPT = """## 角色
你是一个专业的技术调研分析师。你的任务是对给定的原始内容进行深度分析，并按照规定的 JSON Schema 输出结构化报告。

## 强制要求
1. 你必须为所有字段提供内容，禁止省略任何字段
2. topic 必须与输入主题完全一致
3. summary 必须 ≤100字，用一句话概括核心内容
4. key_findings 至少3条，每条要有信息增量（不是重复摘要）
5. structure 的四个子字段都必须有实质内容
6. alternatives 至少列出1个替代方案
7. actionable 必须给出可操作的建议（不是泛泛而谈）
8. 所有长度限制和枚举值都是硬限制，必须遵守

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
你必须输出一个有效的 JSON 对象。
不要输出任何其他内容，不要使用 Markdown 代码块，只输出 JSON。
"""


class CompileReportError(Exception):
    """Base error for compile-report."""


class RawContentError(CompileReportError):
    """Raised when raw content cannot be loaded."""


class LLMCallError(CompileReportError):
    """Raised when the LLM call fails."""


class RetryableError(CompileReportError):
    """Raised when the error is transient and retrying may succeed (e.g. rate limit, timeout)."""


class NonRetryableError(CompileReportError):
    """Raised when the error is permanent and retrying will not help (e.g. SDK not installed)."""


class ValidationError(CompileReportError):
    """Raised when the generated report fails validation."""


class OutputWriteError(CompileReportError):
    """Raised when the output file cannot be written."""


def emit_status(status: str, **payload: Any) -> None:
    message = {"status": status, **payload}
    print(json.dumps(message, ensure_ascii=False), file=sys.stderr)


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max_length, adding '...' if truncated."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def resolve_model(model: Optional[str]) -> str:
    if not model:
        return MODEL_CONFIG["default"]
    return MODEL_CONFIG.get(model, model)


def load_raw_content(raw_path: str) -> str:
    """Load raw content from file or stdin."""
    try:
        if raw_path == "-":
            content = sys.stdin.read()
        else:
            path = Path(raw_path)
            if not path.exists():
                raise RawContentError(f"Raw content file not found: {raw_path}")
            if not path.is_file():
                raise RawContentError(f"Raw content path is not a file: {raw_path}")
            # M2 fix: check size before reading to avoid wasting resources on large empty files
            file_size = path.stat().st_size
            if file_size == 0:
                raise RawContentError(f"Raw content file is empty: {raw_path}")
            content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise RawContentError(f"Failed to read raw content: {exc}") from exc

    if not content.strip():
        raise RawContentError("Raw content is empty after stripping whitespace")
    return content


def build_analysis_prompt(
    raw_content: str,
    topic: str,
    validation_error: Optional[str] = None,
    previous_output: Optional[str] = None,
) -> str:
    """Build the complete analysis prompt."""
    schema_text = json.dumps(REPORT_SCHEMA, ensure_ascii=False, indent=2)
    retry_section = ""

    if validation_error:
        retry_section = f"""
## 上一轮输出校验失败
请修复以下问题后重新输出完整 JSON：
- {validation_error}
"""
        if previous_output:
            retry_section += f"""
## 上一轮原始输出（供纠错参考）
```text
{previous_output[:4000]}
```
"""

    return f"""{ANALYSIS_PROMPT}

## 目标 Topic
{topic}

## JSON Schema
```json
{schema_text}
```
{retry_section}

---

## 原始内容（需要分析的材料）

topic: {topic}

---

{raw_content}

---

## 输出要求
严格按照上述 Schema 输出 JSON。确保所有 required 字段都存在、类型正确、长度合法、枚举值合法。
"""


def build_fallback_report(topic: str) -> Dict[str, Any]:
    short_topic = truncate_text(topic, 40)
    return {
        "topic": topic,
        "summary": f"[Fallback] {short_topic} 当前仅返回占位报告，需配置可用 LLM 后重新生成。",
        "key_findings": [
            "Finding 1: 当前环境未成功调用可用的 LLM 提供方。",
            "Finding 2: 报告结构仍然完整，但内容属于回退占位文本。",
            "Finding 3: 请配置 Gemini、OpenAI 或 Anthropic 以生成正式分析。",
        ],
        "structure": {
            "background": f"{topic} 的背景分析暂不可用，因为本次执行未获得有效的模型响应，当前文本仅用于保持结构完整。",
            "principle": f"{topic} 的原理分析暂不可用，因为本次执行处于回退模式，尚未生成真实的技术机制总结。",
            "implementation": f"{topic} 的实现方式暂不可用，因为本次执行未连接成功到模型服务，无法抽取落地细节。",
            "evaluation": f"{topic} 的优缺点评价暂不可用，因为本次输出来自回退模板，不应视为正式结论。",
        },
        "credibility": {
            "rating": "LOW",
            "verified": [],
            "disputed": ["当前内容来自回退模板，不包含真实分析结论。"],
            "unverified": ["所有主体字段均为占位信息，需要重新生成正式报告。"],
        },
        "alternatives": ["重新配置可用 LLM 后再次生成正式报告"],
        "actionable": "检查 API Key 与 SDK 安装状态，确认模型可调用后重新运行 compile-report.py。",
    }


def _extract_gemini_text(response: Any) -> str:
    text = getattr(response, "text", None)
    if isinstance(text, str) and text.strip():
        return text

    candidates = getattr(response, "candidates", None) or []
    parts: List[str] = []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            part_text = getattr(part, "text", None)
            if isinstance(part_text, str) and part_text:
                parts.append(part_text)
    return "\n".join(parts).strip()


def _extract_openai_text(response: Any) -> str:
    message = response.choices[0].message
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        chunks: List[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                chunks.append(item.get("text", ""))
            else:
                text = getattr(item, "text", None)
                if isinstance(text, str):
                    chunks.append(text)
        return "\n".join(chunk for chunk in chunks if chunk).strip()
    return str(content or "")


def _extract_anthropic_text(response: Any) -> str:
    parts: List[str] = []
    for block in getattr(response, "content", []) or []:
        text = getattr(block, "text", None)
        if isinstance(text, str) and text:
            parts.append(text)
    return "\n".join(parts).strip()


def _is_rate_limit_error(exc: Exception) -> bool:
    """Detect rate limit (429) errors across different provider SDKs."""
    exc_str = str(exc).lower()
    # Check common rate limit indicators
    if "429" in exc_str or "rate limit" in exc_str or "quota" in exc_str or "too many requests" in exc_str:
        return True
    # Check exception types
    exc_type_name = type(exc).__name__.lower()
    if "rate" in exc_type_name or "quota" in exc_type_name:
        return True
    # Check for specific SDK error attributes
    if hasattr(exc, "status_code") and getattr(exc, "status_code", None) == 429:
        return True
    if hasattr(exc, "code") and getattr(exc, "code", None) == 429:
        return True
    return False


def _classify_exception(exc: Exception, provider: str) -> "RetryableError|NonRetryableError":
    """Classify an exception as retryable or non-retryable."""
    # SDK not installed = non-retryable
    if "not installed" in str(exc).lower() or "not found" in str(exc).lower():
        return NonRetryableError(f"[{provider}] {exc}")
    # API key missing = non-retryable
    if "api_key" in str(exc).lower() or "auth" in str(exc).lower() or "credential" in str(exc).lower():
        return NonRetryableError(f"[{provider}] {exc}")
    # Rate limit = retryable
    if _is_rate_limit_error(exc):
        return RetryableError(f"[{provider}] Rate limit exceeded: {exc}")
    # Network timeout = retryable
    if "timeout" in str(exc).lower() or "timed out" in str(exc).lower():
        return RetryableError(f"[{provider}] Timeout: {exc}")
    # Server error (5xx) = retryable
    if hasattr(exc, "status_code"):
        code = getattr(exc, "status_code", 0)
        if 500 <= code < 600:
            return RetryableError(f"[{provider}] Server error {code}: {exc}")
    # Default: treat as non-retryable to avoid infinite loops
    return NonRetryableError(f"[{provider}] {exc}")


def call_llm(prompt: str, topic: str, model: Optional[str] = None) -> str:
    """Call LLM with the given prompt. Supports multiple providers.
    
    Raises:
        RetryableError: For transient errors (rate limit, timeout) that should retry.
        NonRetryableError: For permanent errors (SDK missing, auth failure).
        LLMCallError: For provider-level call failures that may be transient (empty response).
    """
    resolved_model = resolve_model(model)

    if "/" in resolved_model:
        provider, model_name = resolved_model.split("/", 1)
    else:
        provider = "unknown"
        model_name = resolved_model

    if provider in ("google", "gemini"):
        if not HAS_GEMINI or genai is None:
            raise NonRetryableError("Gemini SDK is not installed. Run: pip install google-genai")
        try:
            client = genai.Client()
            config: Any = {
                "response_mime_type": "application/json",
                "response_schema": REPORT_SCHEMA,
            }
            if genai_types is not None:
                config = genai_types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=REPORT_SCHEMA,
                )
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            text = _extract_gemini_text(response)
            if text:
                return text
            # Empty response is potentially transient — treat as retryable
            raise RetryableError("Gemini returned an empty response")
        except (RetryableError, NonRetryableError, LLMCallError):
            raise
        except Exception as exc:
            raise _classify_exception(exc, "Gemini") from exc

    if provider == "openai":
        if not HAS_OPENAI or OpenAIClient is None:
            raise NonRetryableError("OpenAI SDK is not installed. Run: pip install openai")
        try:
            client = OpenAIClient()
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You must return a single JSON object that matches the provided schema.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "arc_reactor_report",
                        "strict": True,
                        "schema": REPORT_SCHEMA,
                    },
                },
            )
            text = _extract_openai_text(response)
            if text:
                return text
            # Empty response is potentially transient — treat as retryable
            raise RetryableError("OpenAI returned an empty response")
        except (RetryableError, NonRetryableError, LLMCallError):
            raise
        except Exception as exc:
            raise _classify_exception(exc, "OpenAI") from exc

    if provider == "anthropic":
        if not HAS_ANTHROPIC or anthropic is None:
            raise NonRetryableError("Anthropic SDK is not installed. Run: pip install anthropic")
        try:
            client = anthropic.Anthropic()
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            text = _extract_anthropic_text(response)
            if text:
                return text
            # Empty response is potentially transient — treat as retryable
            raise RetryableError("Anthropic returned an empty response")
        except (RetryableError, NonRetryableError, LLMCallError):
            raise
        except Exception as exc:
            raise _classify_exception(exc, "Anthropic") from exc

    raise NonRetryableError(f"Unsupported model provider: {resolved_model}")


def _scan_balanced_json(text: str, start_index: int) -> Optional[str]:
    stack: List[str] = []
    in_string = False
    escape = False

    for index in range(start_index, len(text)):
        char = text[index]

        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char == "{":
            stack.append("}")
            continue

        if char == "[":
            stack.append("]")
            continue

        if char in ("}", "]"):
            if not stack or char != stack[-1]:
                return None
            stack.pop()
            if not stack:
                return text[start_index : index + 1]

    return None


def extract_json(text: str) -> str:
    """Extract JSON from potentially wrapped text."""
    if not isinstance(text, str):
        return json.dumps(text, ensure_ascii=False)

    text = text.strip()
    if not text:
        return text

    code_block_pattern = re.compile(r"```(?:json)?\s*([\s\S]*?)\s*```", re.IGNORECASE)
    for match in code_block_pattern.finditer(text):
        candidate = match.group(1).strip()
        if candidate.startswith(("{", "[")):
            extracted = _scan_balanced_json(candidate, 0)
            if extracted:
                return extracted.strip()

    for match in re.finditer(r"[\[{]", text):
        extracted = _scan_balanced_json(text, match.start())
        if extracted:
            return extracted.strip()

    return text


def normalize_strings(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return [normalize_strings(item) for item in value]
    if isinstance(value, dict):
        return {key: normalize_strings(item) for key, item in value.items()}
    return value


def _validate_schema(value: Any, schema: Dict[str, Any], path: str, errors: List[str]) -> None:
    expected_type = schema.get("type")

    if expected_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path} must be an object")
            return

        required_fields = schema.get("required", [])
        missing = [field for field in required_fields if field not in value]
        if missing:
            errors.append(f"{path} is missing required fields: {', '.join(missing)}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = [field for field in value if field not in properties]
            if extras:
                errors.append(f"{path} has unexpected fields: {', '.join(extras)}")

        for field_name, field_schema in properties.items():
            if field_name in value:
                _validate_schema(value[field_name], field_schema, f"{path}.{field_name}", errors)
        return

    if expected_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path} must be an array")
            return

        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path} must contain at least {min_items} items")
        if max_items is not None and len(value) > max_items:
            errors.append(f"{path} must contain at most {max_items} items")

        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, f"{path}[{index}]", errors)
        return

    if expected_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path} must be a string")
            return

        normalized = value.strip()
        min_length = schema.get("minLength")
        max_length = schema.get("maxLength")
        if min_length is not None and len(normalized) < min_length:
            errors.append(f"{path} length must be >= {min_length}")
        if max_length is not None and len(normalized) > max_length:
            errors.append(f"{path} length must be <= {max_length}")

        enum_values = schema.get("enum")
        if enum_values is not None and normalized not in enum_values:
            errors.append(f"{path} must be one of: {', '.join(enum_values)}")
        return

    errors.append(f"{path} uses unsupported schema type: {expected_type}")


def validate_output(json_str: str, expected_topic: str) -> Tuple[bool, str, Dict[str, Any]]:
    """Validate output against schema. Returns (is_valid, message, data)."""
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        return False, f"Invalid JSON: {exc}", {}
    except TypeError as exc:
        return False, f"Invalid JSON payload type: {exc}", {}

    data = normalize_strings(data)
    errors: List[str] = []
    _validate_schema(data, REPORT_SCHEMA, "$", errors)

    topic = data.get("topic") if isinstance(data, dict) else None
    if isinstance(topic, str) and topic != expected_topic:
        errors.append(f"$.topic must exactly equal the requested topic: {expected_topic}")

    if errors:
        return False, "; ".join(errors), {}

    return True, "Valid", data


def compile_report(raw_content: str, topic: str, model: Optional[str] = None) -> Dict[str, Any]:
    """Main compilation flow.
    
    Raises:
        ValidationError: After MAX_RETRIES of validation failures.
        NonRetryableError: When a permanent error occurs (SDK missing, auth failure).
        RetryableError: When a transient error persists after MAX_RETRIES.
    """
    last_error = ""
    last_output = ""
    last_retryable_error: Optional[RetryableError] = None
    rate_limit_backoff = 1.0  # seconds, exponential backoff for rate limits

    for attempt in range(1, MAX_RETRIES + 1):
        prompt = build_analysis_prompt(
            raw_content,
            topic,
            validation_error=last_error or None,
            previous_output=last_output or None,
        )

        try:
            raw_output = call_llm(prompt, topic=topic, model=model)
        except NonRetryableError as exc:
            # Permanent error: raise immediately to fail-closed (don't pollute knowledge base)
            raise
        except RetryableError as exc:
            # Track the last retryable error so we can re-raise it if retries are exhausted
            last_retryable_error = exc
            last_error = str(exc)
            emit_status("retry", attempt=attempt, reason=last_error, backoff=rate_limit_backoff)
            if attempt < MAX_RETRIES:
                time.sleep(rate_limit_backoff)
                rate_limit_backoff = min(rate_limit_backoff * 2, 30.0)  # cap at 30 seconds
            continue
        except LLMCallError as exc:
            # LLMCallError is treated as potentially transient — retry
            last_retryable_error = RetryableError(str(exc))
            last_error = str(exc)
            emit_status("retry", attempt=attempt, reason=f"LLM call error: {exc}")
            continue
        except Exception as exc:
            # Unknown exceptions: raise immediately to fail-closed
            raise NonRetryableError(f"Unexpected error during LLM call: {exc}") from exc

        # M1 fix: clear last_retryable_error once we get a valid model response (even if validation fails)
        last_retryable_error = None

        json_str = extract_json(raw_output)
        is_valid, message, data = validate_output(json_str, expected_topic=topic)

        if is_valid:
            return {
                "status": "success",
                "topic": topic,
                "report": data,
                "attempts": attempt,
            }

        last_error = message
        last_output = raw_output
        emit_status("retry", attempt=attempt, reason=message)
        rate_limit_backoff = 1.0  # reset backoff on validation failure (not a rate limit)

    # H1 fix: if the last failure was a retryable error, re-raise it rather than ValidationError
    if last_retryable_error is not None:
        raise last_retryable_error

    raise ValidationError(f"Failed after {MAX_RETRIES} attempts. Last error: {last_error}")


def write_output(output_path: str, output_text: str) -> None:
    path = Path(output_path)
    temp_path: Optional[str] = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(output_text)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = handle.name
        os.replace(temp_path, path)
    except OSError as exc:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass
        raise OutputWriteError(f"Failed to write output file {output_path}: {exc}") from exc


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="ARC Reactor 结构化报告生成器 — 强制执行多维分析框架"
    )
    parser.add_argument("--topic", required=True, help="主题名称")
    parser.add_argument("--raw", required=True, help="原始内容文件路径（或 '-' 读取 stdin）")
    parser.add_argument("--model", help="指定模型（provider/name 格式，如 google/gemini-2.0-flash）")
    parser.add_argument("--output", help="输出文件路径（默认为 stdout）")
    args = parser.parse_args(argv)

    try:
        raw_content = load_raw_content(args.raw)
        result = compile_report(raw_content, args.topic, args.model)
        output = json.dumps(result, ensure_ascii=False, indent=2)

        if args.output:
            write_output(args.output, output)
            print(
                json.dumps(
                    {
                        "status": "success",
                        "output": args.output,
                        "topic": args.topic,
                    },
                    ensure_ascii=False,
                )
            )
        else:
            print(output)
        return 0
    except CompileReportError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(json.dumps({"status": "error", "message": "Interrupted"}, ensure_ascii=False), file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
