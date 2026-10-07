"""Matched, missing, and additional skills display."""

from __future__ import annotations

import html

import streamlit as st


def _tags(items: list[str], kind: str) -> str:
    if not items:
        return "<span class='empty-tag'>None identified</span>"
    return "".join(f"<span class='skill-tag {kind}'>{html.escape(item)}</span>" for item in items)


def render_skills_view(skills: dict) -> None:
    matched, missing, additional = st.columns(3)
    with matched:
        st.markdown(f"### Matched · {len(skills['matched'])}")
        st.markdown(_tags(skills["matched"], "matched"), unsafe_allow_html=True)
    with missing:
        st.markdown(f"### Missing · {len(skills['missing'])}")
        st.markdown(_tags(skills["missing"], "missing"), unsafe_allow_html=True)
    with additional:
        st.markdown(f"### Additional · {len(skills['additional'])}")
        st.markdown(_tags(skills["additional"], "additional"), unsafe_allow_html=True)

