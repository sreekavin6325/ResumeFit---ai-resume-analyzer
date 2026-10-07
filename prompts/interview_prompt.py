"""Prompt for tailored interview questions."""

from __future__ import annotations


def build_interview_prompt(resume_text: str, job_description: str, missing_skills: list[str]) -> str:
    return f"""Create exactly eight interview questions for this candidate and role:
three technical, two behavioral, two resume-deep-dive, and one gap-focused question.
After each question, add one short line beginning with 'What a strong answer covers:'.
Do not provide fabricated candidate answers.

Known skill gaps: {', '.join(missing_skills) or 'none'}

RESUME:
{resume_text[:12000]}

JOB DESCRIPTION:
{job_description[:8000]}
"""

