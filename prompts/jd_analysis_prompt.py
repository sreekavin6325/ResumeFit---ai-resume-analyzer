"""Prompt for extracting structured job requirements."""

from __future__ import annotations


def build_jd_analysis_prompt(job_description: str) -> str:
    return f"""Extract job requirements from the text below. Return only valid JSON with keys:
title (string), required_skills (array), preferred_skills (array), minimum_years_experience (number),
education (string), and keywords (array). Do not infer requirements that are not stated.

JOB DESCRIPTION:
{job_description[:12000]}
"""

