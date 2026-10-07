"""Prompt for holistic resume feedback."""

from __future__ import annotations


def build_resume_analysis_prompt(resume_text: str, job_description: str, metrics: dict) -> str:
    return f"""You are a careful career coach and resume editor.
Analyze the resume against the job description using only the supplied text. Do not invent experience.
Return concise Markdown with these headings: Executive summary, Strongest evidence, Highest-impact gaps,
Rewrite suggestions, and 30-day action plan. Make every suggestion specific and truthful.

Deterministic analysis metrics:
{metrics}

RESUME:
{resume_text[:14000]}

JOB DESCRIPTION:
{job_description[:9000]}
"""

