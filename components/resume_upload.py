"""Resume upload panel."""

from __future__ import annotations

import streamlit as st


def render_resume_upload():
    st.subheader("1. Upload your resume")
    st.caption("PDF, DOCX, or UTF-8 TXT · maximum size is configured in `.env`")
    return st.file_uploader(
        "Resume file",
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        help="Text-based files work best. Scanned PDFs require OCR before upload.",
    )

