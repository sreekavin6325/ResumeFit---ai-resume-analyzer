"""Small, dependency-free helper functions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    return max(minimum, min(maximum, value))


def unique_preserving_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        cleaned = item.strip()
        key = cleaned.casefold()
        if cleaned and key not in seen:
            seen.add(key)
            result.append(cleaned)
    return result


def safe_filename(name: str, default: str = "resume") -> str:
    stem = Path(name).stem
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-._")
    return cleaned or default


def extract_json_object(text: str) -> dict[str, Any] | None:
    """Extract a JSON object from plain text or a fenced code block."""
    candidates = [text.strip()]
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.I)
    candidates.extend(fenced)
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidates.append(match.group(0))
    for candidate in candidates:
        try:
            value = json.loads(candidate)
            if isinstance(value, dict):
                return value
        except (json.JSONDecodeError, TypeError):
            continue
    return None

