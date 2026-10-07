"""Lightweight text normalization and tokenization."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

from utils.constants import STOP_WORDS


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\u2022", " ").replace("\uf0b7", " ")
    text = re.sub(r"[\t\r]+", " ", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text: str, remove_stop_words: bool = True) -> list[str]:
    normalized = normalize_text(text).casefold()
    tokens = re.findall(r"[a-z0-9][a-z0-9+#./-]*", normalized)
    if remove_stop_words:
        tokens = [token for token in tokens if token not in STOP_WORDS and len(token) > 1]
    return tokens


def keyword_frequencies(text: str, limit: int = 30) -> list[tuple[str, int]]:
    return Counter(tokenize(text)).most_common(limit)


def phrase_present(text: str, phrase: str) -> bool:
    """Match a skill phrase without treating C as present in every word."""
    haystack = f" {normalize_text(text).casefold()} "
    needle = normalize_text(phrase).casefold()
    pattern = rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])"
    return bool(re.search(pattern, haystack))

