"""Application header."""

from __future__ import annotations

import html
from pathlib import Path

import streamlit as st


def render_header(title: str, tagline: str, logo_path: Path, mode_label: str, ai_enabled: bool) -> None:
    logo, copy, status = st.columns([1, 8, 3], vertical_alignment="center")
    with logo:
        if logo_path.exists():
            st.image(str(logo_path), width=68)
    with copy:
        st.markdown(
            f"<h1 class='app-title'>{html.escape(title)}</h1>"
            f"<p class='app-tagline'>{html.escape(tagline)}</p>",
            unsafe_allow_html=True,
        )
    with status:
        kind = "ai" if ai_enabled else "local"
        st.markdown(f"<span class='mode-pill {kind}'>{html.escape(mode_label)}</span>", unsafe_allow_html=True)
    st.markdown("<div class='header-rule'></div>", unsafe_allow_html=True)


def render_step(number: int, title: str, copy: str) -> None:
    st.markdown(
        f"<div class='step-head'><span class='step-num'>{number}</span>"
        f"<p class='step-title'>{html.escape(title)}</p></div>"
        f"<p class='step-copy'>{html.escape(copy)}</p>",
        unsafe_allow_html=True,
    )
