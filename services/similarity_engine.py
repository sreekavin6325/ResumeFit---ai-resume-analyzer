"""Dependency-free document similarity metrics."""

from __future__ import annotations

import math
from collections import Counter

from services.text_preprocessor import tokenize


def cosine_similarity(text_a: str, text_b: str) -> float:
    a = Counter(tokenize(text_a))
    b = Counter(tokenize(text_b))
    if not a or not b:
        return 0.0
    shared = a.keys() & b.keys()
    dot_product = sum(a[token] * b[token] for token in shared)
    magnitude_a = math.sqrt(sum(value * value for value in a.values()))
    magnitude_b = math.sqrt(sum(value * value for value in b.values()))
    return dot_product / (magnitude_a * magnitude_b) if magnitude_a and magnitude_b else 0.0


def keyword_coverage(resume_text: str, job_keywords: list[str]) -> tuple[float, list[str]]:
    resume_tokens = set(tokenize(resume_text, remove_stop_words=False))
    unique_keywords = list(dict.fromkeys(word.casefold() for word in job_keywords if word))
    if not unique_keywords:
        return 1.0, []
    matched = [word for word in unique_keywords if word in resume_tokens]
    return len(matched) / len(unique_keywords), matched

