"""Extract explainable signals from job descriptions and resumes."""

from __future__ import annotations

import re

from services.skill_extractor import extract_skills
from services.text_preprocessor import keyword_frequencies, normalize_text
from utils.constants import EDUCATION_LEVELS, RESUME_SECTIONS


def extract_years_experience(text: str) -> float:
    patterns = [
        r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)",
        r"(?:minimum|min(?:imum)?\.?|at least)\s+(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
    ]
    values: list[float] = []
    for pattern in patterns:
        values.extend(float(value) for value in re.findall(pattern, text, flags=re.I))
    return max(values, default=0.0)


def extract_education_level(text: str) -> tuple[str, int]:
    lowered = normalize_text(text).casefold()
    matches = [(name, level) for name, level in EDUCATION_LEVELS.items() if name in lowered]
    if not matches:
        return "Not specified", 0
    name, level = max(matches, key=lambda item: item[1])
    labels = {4: "Doctorate", 3: "Master's", 2: "Bachelor's", 1: "Diploma"}
    return labels[level], level


def detect_resume_sections(text: str) -> dict[str, bool]:
    lowered = normalize_text(text).casefold()
    return {
        section: any(re.search(rf"(?m)^\s*{re.escape(label)}\s*:?[\s]*$", lowered) for label in labels)
        or any(label in lowered for label in labels)
        for section, labels in RESUME_SECTIONS.items()
    }


def _guess_title(text: str) -> str:
    first_lines = [line.strip(" :-") for line in normalize_text(text).splitlines() if line.strip()]
    for line in first_lines[:5]:
        if len(line.split()) <= 8 and any(word in line.casefold() for word in ("engineer", "developer", "scientist", "analyst", "manager", "designer")):
            return line
    return "Target role"


def analyze_job_description(text: str) -> dict:
    normalized = normalize_text(text)
    education, education_level = extract_education_level(normalized)
    return {
        "title": _guess_title(normalized),
        "skills": extract_skills(normalized),
        "minimum_years_experience": extract_years_experience(normalized),
        "education": education,
        "education_level": education_level,
        "keywords": [word for word, _ in keyword_frequencies(normalized, limit=25)],
    }


def analyze_resume(text: str) -> dict:
    normalized = normalize_text(text)
    education, education_level = extract_education_level(normalized)
    return {
        "skills": extract_skills(normalized),
        "years_experience": extract_years_experience(normalized),
        "education": education,
        "education_level": education_level,
        "sections": detect_resume_sections(normalized),
        "word_count": len(normalized.split()),
    }

