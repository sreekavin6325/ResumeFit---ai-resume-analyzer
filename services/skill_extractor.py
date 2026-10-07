"""Dictionary-based, explainable skill extraction."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from config.settings import BASE_DIR
from services.text_preprocessor import phrase_present
from utils.helpers import unique_preserving_order


@lru_cache(maxsize=4)
def load_skill_catalog(path: str | None = None) -> dict:
    catalog_path = Path(path) if path else BASE_DIR / "data" / "skills.json"
    return json.loads(catalog_path.read_text(encoding="utf-8"))


def extract_skills(text: str, catalog: dict | None = None) -> list[str]:
    catalog = catalog or load_skill_catalog()
    aliases: dict[str, str] = catalog.get("aliases", {})
    canonical: list[str] = []
    for category, skills in catalog.items():
        if category == "aliases":
            continue
        canonical.extend(skills)

    found = [skill for skill in canonical if phrase_present(text, skill)]
    for alias, target in aliases.items():
        if phrase_present(text, alias):
            found.append(target)
    return sorted(unique_preserving_order(found), key=str.casefold)


def compare_skills(resume_skills: list[str], job_skills: list[str]) -> dict[str, list[str] | float]:
    resume_map = {skill.casefold(): skill for skill in resume_skills}
    job_map = {skill.casefold(): skill for skill in job_skills}
    matched_keys = resume_map.keys() & job_map.keys()
    missing_keys = job_map.keys() - resume_map.keys()
    extra_keys = resume_map.keys() - job_map.keys()
    matched = sorted((job_map[key] for key in matched_keys), key=str.casefold)
    missing = sorted((job_map[key] for key in missing_keys), key=str.casefold)
    additional = sorted((resume_map[key] for key in extra_keys), key=str.casefold)
    coverage = (len(matched) / len(job_map) * 100) if job_map else 100.0
    return {"matched": matched, "missing": missing, "additional": additional, "coverage": round(coverage, 1)}

