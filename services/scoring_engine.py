"""Transparent weighted scoring for resume-to-job fit."""

from __future__ import annotations

from services.jd_analyzer import analyze_job_description, analyze_resume
from services.similarity_engine import cosine_similarity, keyword_coverage
from services.skill_extractor import compare_skills
from utils.constants import SCORE_WEIGHTS
from utils.helpers import clamp


def _experience_score(candidate_years: float, required_years: float) -> float:
    if required_years <= 0:
        return 100.0
    return clamp(candidate_years / required_years * 100)


def _education_score(candidate_level: int, required_level: int) -> float:
    if required_level <= 0:
        return 100.0
    if candidate_level >= required_level:
        return 100.0
    return clamp(candidate_level / required_level * 100)


def calculate_match_score(resume_text: str, job_description: str) -> dict:
    resume = analyze_resume(resume_text)
    job = analyze_job_description(job_description)
    skill_comparison = compare_skills(resume["skills"], job["skills"])
    keyword_ratio, matched_keywords = keyword_coverage(resume_text, job["keywords"])
    semantic_ratio = cosine_similarity(resume_text, job_description)

    component_scores = {
        "skills": float(skill_comparison["coverage"]),
        "keywords": round((keyword_ratio * 0.7 + semantic_ratio * 0.3) * 100, 1),
        "experience": round(_experience_score(resume["years_experience"], job["minimum_years_experience"]), 1),
        "education": round(_education_score(resume["education_level"], job["education_level"]), 1),
        "completeness": round(sum(resume["sections"].values()) / len(resume["sections"]) * 100, 1),
    }
    total = sum(component_scores[name] * SCORE_WEIGHTS[name] for name in SCORE_WEIGHTS)
    total = round(clamp(total), 1)
    if total >= 80:
        label = "Excellent match"
    elif total >= 65:
        label = "Strong match"
    elif total >= 50:
        label = "Moderate match"
    else:
        label = "Needs alignment"

    return {
        "overall_score": total,
        "label": label,
        "components": component_scores,
        "weights": SCORE_WEIGHTS,
        "skills": skill_comparison,
        "matched_keywords": matched_keywords,
        "similarity": round(semantic_ratio * 100, 1),
        "resume": resume,
        "job": job,
    }

