"""Feedback and recommendation display."""

from __future__ import annotations

import streamlit as st


def render_ai_feedback(result: dict) -> None:
    st.caption(f"Generated with {result['source']}")
    if result.get("error"):
        st.info("The AI request was unavailable, so this result uses the local analysis engine.")
        with st.expander("Technical detail"):
            st.code(result["error"])
    st.markdown(result["content"])

