"""Feedback and recommendation display."""

from __future__ import annotations

import html

import streamlit as st


def render_ai_feedback(result: dict) -> None:
    st.markdown(f"<span class='source-pill'>Generated with {html.escape(result['source'])}</span>", unsafe_allow_html=True)
    if result.get("error"):
        st.info("The AI request was unavailable, so this result uses the local analysis engine.", icon=":material/info:")
        with st.expander("Technical detail"):
            st.code(result["error"])
    with st.container(border=True, key="card-feedback"):
        st.markdown(result["content"])
