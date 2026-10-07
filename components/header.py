"""Application header."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


def render_header(title: str, tagline: str, logo_path: Path) -> None:
    logo, copy = st.columns([1, 7], vertical_alignment="center")
    with logo:
        if logo_path.exists():
            st.image(str(logo_path), width=92)
    with copy:
        st.markdown(f"<h1 class='app-title'>{title}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='app-tagline'>{tagline}</p>", unsafe_allow_html=True)
    st.markdown("<div class='header-rule'></div>", unsafe_allow_html=True)

