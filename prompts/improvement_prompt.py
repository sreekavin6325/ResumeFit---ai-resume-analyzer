"""Prompt for bullet-level resume improvements."""

from __future__ import annotations


def build_improvement_prompt(resume_text: str, missing_skills: list[str]) -> str:
    missing = ", ".join(missing_skills) or "none identified"
    return f"""Act as an ethical resume editor. Suggest up to six stronger bullet rewrites.
Never add tools, metrics, employers, or achievements that are absent from the resume.
When information is missing, use a bracketed placeholder such as [measurable result].
Target skills that are genuinely supported by the resume and note unsupported gaps separately.

Potential gaps: {missing}

RESUME:
{resume_text[:14000]}
"""

