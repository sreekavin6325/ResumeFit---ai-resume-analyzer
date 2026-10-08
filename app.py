"""Streamlit entry point for AI Resume Analyzer."""

from __future__ import annotations

import html

import streamlit as st

from components.ai_feedback import render_ai_feedback
from components.header import render_header
from components.interview_questions import render_interview_questions
from components.jd_input import render_job_description_input
from components.resume_upload import render_resume_upload
from components.score_card import render_score_card
from components.skills_view import render_skills_view
from config.settings import get_settings
from services.ai_engine import AIEngine
from services.pdf_parser import ResumeParseError, extract_resume_text
from services.recommendation_engine import generate_recommendations
from services.report_generator import build_json_report, build_pdf_report
from services.scoring_engine import calculate_match_score
from utils.constants import SCORE_WEIGHTS
from utils.helpers import safe_filename
from utils.validators import validate_job_description, validate_resume_file


settings = get_settings()
st.set_page_config(
    page_title=settings.app_name,
    page_icon=str(settings.base_dir / "assets" / "logo.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

css_path = settings.base_dir / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

mode_label = f"AI feedback · {settings.openai_model}" if settings.ai_enabled else "Local analysis mode"
render_header(
    settings.app_name,
    settings.app_tagline,
    settings.base_dir / "assets" / "logo.png",
    mode_label,
    settings.ai_enabled,
)

with st.sidebar:
    st.subheader("How scoring works")
    st.markdown(
        "".join(
            f"<div class='weight-row'><span>{name.title()}</span><b>{weight * 100:.0f}%</b></div>"
            for name, weight in SCORE_WEIGHTS.items()
        ),
        unsafe_allow_html=True,
    )
    st.divider()
    if not settings.ai_enabled:
        st.info("Add `OPENAI_API_KEY` to `.env` for AI-enhanced feedback.", icon=":material/auto_awesome:")
    st.caption("Privacy: files stay in memory unless AI feedback is enabled. API requests use `store=False`.")

resume_column, job_column = st.columns(2, gap="medium")
with resume_column:
    with st.container(border=True, key="card-resume"):
        uploaded_file = render_resume_upload(settings.max_file_size_mb)
with job_column:
    with st.container(border=True, key="card-job"):
        job_description = render_job_description_input(settings.base_dir / "data")

analyze = st.button("Analyze resume", type="primary", icon=":material/insights:", use_container_width=True)

if analyze:
    file_valid, file_error = validate_resume_file(uploaded_file, settings.max_file_size_mb)
    job_valid, job_error = validate_job_description(job_description)
    if not file_valid:
        st.error(file_error, icon=":material/error:")
    if not job_valid:
        st.error(job_error, icon=":material/error:")
    if file_valid and job_valid:
        try:
            with st.spinner("Reading the resume and comparing it with the role…"):
                resume_text = extract_resume_text(uploaded_file, uploaded_file.name)
                analysis = calculate_match_score(resume_text, job_description)
                recommendations = generate_recommendations(resume_text, analysis)
                ai_engine = AIEngine(settings)
                feedback = ai_engine.feedback(resume_text, job_description, analysis)
                questions = ai_engine.interview_questions(resume_text, job_description, analysis)
                st.session_state["result"] = {
                    "filename": uploaded_file.name,
                    "resume_text": resume_text,
                    "job_description": job_description,
                    "analysis": analysis,
                    "recommendations": recommendations,
                    "feedback": feedback,
                    "questions": questions,
                }
            st.toast("Analysis complete", icon=":material/check_circle:")
        except ResumeParseError as exc:
            st.error(str(exc), icon=":material/error:")
        except Exception as exc:
            st.error("The analysis could not be completed.", icon=":material/error:")
            with st.expander("Technical detail"):
                st.code(str(exc))

result = st.session_state.get("result")
if result:
    st.markdown("<div class='header-rule'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<p class='section-title' style='margin-top:0'>Results for {html.escape(result['filename'])}</p>",
        unsafe_allow_html=True,
    )
    render_score_card(result["analysis"])

    overview_tab, skills_tab, feedback_tab, interview_tab, report_tab = st.tabs(
        [
            ":material/dashboard: Overview",
            ":material/checklist: Skills",
            ":material/rate_review: Feedback",
            ":material/forum: Interview prep",
            ":material/download: Report",
        ]
    )
    with overview_tab:
        analysis = result["analysis"]
        resume, job = analysis["resume"], analysis["job"]
        rows = [
            ("Experience", f"{resume['years_experience']:g} years", f"{job['minimum_years_experience']:g}+ years"),
            ("Education", resume["education"], job["education"]),
            ("Skills", f"{len(analysis['skills']['matched'])} matched", f"{len(job['skills'])} requested"),
            ("Text similarity", f"{analysis['similarity']}%", "—"),
            ("Resume length", f"{resume['word_count']} words", "—"),
        ]
        table_rows = "".join(
            f"<tr><td>{html.escape(label)}</td><td>{html.escape(str(mine))}</td><td>{html.escape(str(theirs))}</td></tr>"
            for label, mine, theirs in rows
        )
        # Strip indentation: Markdown treats 4+ leading spaces as a code block.
        overview_html = (
            f"""
            <table class="compare">
              <thead><tr><th>Signal</th><th>Your resume</th><th>{html.escape(job['title'])}</th></tr></thead>
              <tbody>{table_rows}</tbody>
            </table>
            <p class="section-title">Recommended next moves</p>
            """
            + "".join(
                f"""
                <div class="rec {item['priority'].lower()}">
                  <span class="pill {item['priority'].lower()}">{html.escape(item['priority'])}</span>
                  <div><p class="rec-title">{html.escape(item['title'])}</p>
                  <p class="rec-detail">{html.escape(item['detail'])}</p></div>
                </div>"""
                for item in result["recommendations"]
            )
        )
        st.markdown("\n".join(line.strip() for line in overview_html.splitlines()), unsafe_allow_html=True)
    with skills_tab:
        render_skills_view(result["analysis"]["skills"])
        st.caption("Skills are matched against the editable catalog in `data/skills.json`.")
    with feedback_tab:
        render_ai_feedback(result["feedback"])
    with interview_tab:
        render_interview_questions(result["questions"])
    with report_tab:
        stem = safe_filename(result["filename"])
        json_bytes = build_json_report(result["filename"], result["analysis"], result["recommendations"])
        pdf_bytes = build_pdf_report(result["filename"], result["analysis"], result["recommendations"])
        pdf_col, json_col = st.columns(2, gap="medium")
        with pdf_col, st.container(border=True, key="card-pdf"):
            st.markdown("<p class='step-title'>PDF report</p>"
                        "<p class='download-copy'>A formatted summary to read or share.</p>", unsafe_allow_html=True)
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=f"{stem}-analysis.pdf",
                mime="application/pdf",
                icon=":material/picture_as_pdf:",
                use_container_width=True,
            )
        with json_col, st.container(border=True, key="card-json"):
            st.markdown("<p class='step-title'>JSON data</p>"
                        "<p class='download-copy'>Raw scores and skills for other tools.</p>", unsafe_allow_html=True)
            st.download_button(
                "Download JSON",
                data=json_bytes,
                file_name=f"{stem}-analysis.json",
                mime="application/json",
                icon=":material/data_object:",
                use_container_width=True,
            )
        st.caption("Use this score as coaching guidance only — not as an automated hiring decision.")
