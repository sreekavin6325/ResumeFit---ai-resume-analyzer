"""Score summary visualization."""

from __future__ import annotations

import streamlit as st


def render_score_card(analysis: dict) -> None:
    score = analysis["overall_score"]
    st.markdown(
        f"""
        <section class="score-hero">
          <div class="score-number">{score:.0f}<span>%</span></div>
          <div><div class="score-label">{analysis['label']}</div>
          <div class="score-copy">Directional fit based on skills, keywords, experience, education, and structure.</div></div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.progress(int(score))
    columns = st.columns(len(analysis["components"]))
    for column, (name, value) in zip(columns, analysis["components"].items()):
        column.metric(name.title(), f"{value:.0f}%", help=f"Weight: {analysis['weights'][name] * 100:.0f}%")

