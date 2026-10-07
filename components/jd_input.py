"""Job description input and sample loader."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


def render_job_description_input(data_dir: Path) -> str:
    st.subheader("2. Add the job description")
    roles = json.loads((data_dir / "job_roles.json").read_text(encoding="utf-8"))
    options = ["Paste my own"] + [role["title"] for role in roles]
    selected = st.selectbox("Start with", options)
    sample = ""
    if selected != "Paste my own":
        role = next(item for item in roles if item["title"] == selected)
        sample = (data_dir / "sample_jobs" / role["description_file"]).read_text(encoding="utf-8")
    return st.text_area(
        "Job description",
        value=sample,
        height=255,
        placeholder="Paste the responsibilities, required skills, experience, and education…",
    )

