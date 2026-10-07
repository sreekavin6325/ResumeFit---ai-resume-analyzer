"""Interview-preparation display."""

from __future__ import annotations

import streamlit as st


def render_interview_questions(result: dict) -> None:
    st.caption(f"Generated with {result['source']}")
    if result.get("error"):
        st.info("The AI request was unavailable, so the questions were generated locally.")
    st.markdown(result["content"])

