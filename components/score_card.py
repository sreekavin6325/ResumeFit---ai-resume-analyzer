"""Score summary visualization."""

from __future__ import annotations

import html

import streamlit as st


def score_tone(score: float) -> str:
    if score >= 80:
        return "good"
    if score >= 65:
        return "ok"
    if score >= 50:
        return "fair"
    return "low"


def render_score_card(analysis: dict) -> None:
    score = analysis["overall_score"]
    bars = "".join(
        f"""
        <div class="bar-row tone-{score_tone(value)}">
          <div class="bar-name">{html.escape(name.title())}<span>{analysis['weights'][name] * 100:.0f}% weight</span></div>
          <div class="bar-track" role="progressbar" aria-label="{html.escape(name.title())}"
               aria-valuenow="{value:.0f}" aria-valuemin="0" aria-valuemax="100">
            <div class="bar-fill" style="width:{value:.0f}%"></div>
          </div>
          <div class="bar-value">{value:.0f}%</div>
        </div>"""
        for name, value in analysis["components"].items()
    )
    st.markdown(
        f"""
        <section class="score-card">
          <div class="score-main tone-{score_tone(score)}">
            <div class="score-ring" style="--value:{score:.0f}" role="img" aria-label="Overall match {score:.0f} percent">
              <div class="score-ring-inner">{score:.0f}<small>%</small></div>
            </div>
            <div>
              <p class="score-label">{html.escape(analysis['label'])}</p>
              <p class="score-copy">Overall fit based on skills, keywords, experience, education, and structure.</p>
            </div>
          </div>
          <div>{bars}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )
