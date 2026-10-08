"""Matched, missing, and additional skills display."""

from __future__ import annotations

import html

import streamlit as st

_GROUPS = (
    ("matched", "Matched", "In your resume and the job"),
    ("missing", "Missing", "Asked for, not found in your resume"),
    ("additional", "Additional", "Extra strengths you bring"),
)


def _tags(items: list[str], kind: str) -> str:
    if not items:
        return "<span class='empty-tag'>None identified</span>"
    return "".join(f"<span class='skill-tag {kind}'>{html.escape(item)}</span>" for item in items)


def render_skills_view(skills: dict) -> None:
    for column, (kind, title, copy) in zip(st.columns(3), _GROUPS):
        column.markdown(
            f"""
            <div class="skill-col {kind}">
              <div class="skill-col-head">
                <span class="skill-col-title">{title}</span>
                <span class="skill-count">{len(skills[kind])}</span>
              </div>
              <p class="skill-col-copy">{copy}</p>
              {_tags(skills[kind], kind)}
            </div>
            """,
            unsafe_allow_html=True,
        )
