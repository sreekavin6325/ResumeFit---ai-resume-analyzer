"""Interview-preparation display."""

from __future__ import annotations

import html

import streamlit as st


def render_interview_questions(result: dict) -> None:
    st.markdown(f"<span class='source-pill'>Generated with {html.escape(result['source'])}</span>", unsafe_allow_html=True)
    if result.get("error"):
        st.info("The AI request was unavailable, so the questions were generated locally.", icon=":material/info:")
    with st.container(border=True, key="card-interview"):
        st.markdown(result["content"])
