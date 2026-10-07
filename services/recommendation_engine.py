"""Generate deterministic, evidence-based resume recommendations."""

from __future__ import annotations

import re


def _has_metrics(text: str) -> bool:
    return bool(re.search(r"(?:\d+%|[$₹€£]\s?\d+|\d+\s*(?:users|clients|projects|hours|days|months))", text, re.I))


def generate_recommendations(resume_text: str, analysis: dict) -> list[dict[str, str]]:
    recommendations: list[dict[str, str]] = []
    missing_skills = analysis["skills"]["missing"]
    if missing_skills:
        recommendations.append({
            "priority": "High",
            "title": "Address the most important skill gaps",
            "detail": "If you genuinely have experience with them, add evidence for: " + ", ".join(missing_skills[:6]) + ". Never list unsupported skills.",
        })
    if analysis["components"]["experience"] < 100:
        recommendations.append({
            "priority": "High",
            "title": "Make experience duration explicit",
            "detail": "Use clear month/year dates and a short summary so recruiters can verify your relevant experience quickly.",
        })
    if not _has_metrics(resume_text):
        recommendations.append({
            "priority": "Medium",
            "title": "Quantify outcomes",
            "detail": "Add truthful scale, speed, quality, revenue, cost, or adoption metrics to achievement bullets.",
        })
    missing_sections = [name.title() for name, present in analysis["resume"]["sections"].items() if not present]
    if missing_sections:
        recommendations.append({
            "priority": "Medium",
            "title": "Improve resume structure",
            "detail": "Add or clearly label these useful sections: " + ", ".join(missing_sections) + ".",
        })
    if analysis["resume"]["word_count"] < 180:
        recommendations.append({
            "priority": "Medium",
            "title": "Add evidence, not filler",
            "detail": "The resume is quite short. Add relevant projects, responsibilities, and measurable achievements.",
        })
    elif analysis["resume"]["word_count"] > 1100:
        recommendations.append({
            "priority": "Low",
            "title": "Tighten the document",
            "detail": "Remove repetition and keep the strongest, most role-relevant evidence near the top.",
        })
    if analysis["components"]["keywords"] < 55:
        recommendations.append({
            "priority": "Medium",
            "title": "Mirror the employer's language",
            "detail": "Where accurate, use the same terminology as the job description in your summary and experience bullets.",
        })
    if not recommendations:
        recommendations.append({
            "priority": "Low",
            "title": "Polish the strongest evidence",
            "detail": "Lead each bullet with an action, keep outcomes measurable, and tailor the top third of the resume to this role.",
        })
    return recommendations


def generate_interview_questions(analysis: dict) -> list[dict[str, str]]:
    matched = analysis["skills"]["matched"]
    missing = analysis["skills"]["missing"]
    questions: list[dict[str, str]] = []
    for skill in matched[:3]:
        questions.append({
            "category": "Technical",
            "question": f"Tell me about a production problem you solved using {skill}. What trade-offs did you make?",
        })
    if missing:
        questions.append({
            "category": "Growth",
            "question": f"This role uses {missing[0]}. How would you become productive with it, and what related experience transfers?",
        })
    questions.extend([
        {"category": "Behavioral", "question": "Describe a time requirements changed late. How did you reset expectations and deliver value?"},
        {"category": "Behavioral", "question": "Tell me about a disagreement with a teammate and how you resolved it."},
        {"category": "Impact", "question": "Which achievement on your resume had the greatest measurable impact, and how did you measure it?"},
        {"category": "Role fit", "question": f"Why does the {analysis['job']['title']} role fit your next career step?"},
    ])
    return questions[:8]

