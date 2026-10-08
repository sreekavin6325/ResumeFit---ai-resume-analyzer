"""Resume upload panel."""

from __future__ import annotations

import streamlit as st

from components.header import render_step


def render_resume_upload(max_size_mb: int):
    render_step(1, "Upload your resume", f"PDF, DOCX, or TXT · up to {max_size_mb} MB")
    return st.file_uploader(
        "Resume file",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        help="Text-based files work best. Scanned PDFs require OCR before upload.",
    )
