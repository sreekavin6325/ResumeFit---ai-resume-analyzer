"""Streamlit entry point for AI Resume Analyzer."""

from __future__ import annotations

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
from utils.helpers import safe_filename
from utils.validators import validate_job_description, validate_resume_file


settings = get_settings()
st.set_page_config(
    page_title=settings.app_name,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

css_path = settings.base_dir / "assets" / "styles.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

render_header(settings.app_name, settings.app_tagline, settings.base_dir / "assets" / "logo.png")

with st.sidebar:
    st.header("How scoring works")
    st.markdown(
        """
        The score combines:

        - **Skills — 45%**
        - **Keywords — 20%**
        - **Experience — 20%**
        - **Education — 10%**
        - **Resume structure — 5%**
        """
    )
    st.divider()
    if settings.ai_enabled:
        st.success(f"AI feedback enabled · {settings.openai_model}")
    else:
        st.info("Local analysis mode. Add `OPENAI_API_KEY` to `.env` for AI-enhanced feedback.")
    st.caption("Privacy note: files stay in memory unless AI feedback is enabled. API requests use `store=False`.")

resume_column, job_column = st.columns(2, gap="large")
with resume_column:
    uploaded_file = render_resume_upload()
with job_column:
    job_description = render_job_description_input(settings.base_dir / "data")

analyze = st.button("Analyze resume", type="primary", use_container_width=True)

if analyze:
    file_valid, file_error = validate_resume_file(uploaded_file, settings.max_file_size_mb)
    job_valid, job_error = validate_job_description(job_description)
    if not file_valid:
        st.error(file_error)
    if not job_valid:
        st.error(job_error)
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
            st.toast("Analysis complete", icon="✅")
        except ResumeParseError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error("The analysis could not be completed.")
            with st.expander("Technical detail"):
                st.code(str(exc))

result = st.session_state.get("result")
if result:
    st.divider()
    render_score_card(result["analysis"])

    overview_tab, skills_tab, feedback_tab, interview_tab, report_tab = st.tabs(
        ["Overview", "Skills", "Feedback", "Interview prep", "Download report"]
    )
    with overview_tab:
        left, right = st.columns(2)
        analysis = result["analysis"]
        with left:
            st.subheader("Candidate signals")
            st.write(f"**Detected experience:** {analysis['resume']['years_experience']:g} years")
            st.write(f"**Education:** {analysis['resume']['education']}")
            st.write(f"**Resume length:** {analysis['resume']['word_count']} words")
            st.write(f"**Text similarity:** {analysis['similarity']}%")
        with right:
            st.subheader("Role signals")
            st.write(f"**Detected title:** {analysis['job']['title']}")
            st.write(f"**Required experience:** {analysis['job']['minimum_years_experience']:g} years")
            st.write(f"**Education:** {analysis['job']['education']}")
            st.write(f"**Skills detected:** {len(analysis['job']['skills'])}")
        st.subheader("Recommended next moves")
        for item in result["recommendations"]:
            with st.expander(f"{item['priority']} · {item['title']}", expanded=item["priority"] == "High"):
                st.write(item["detail"])
    with skills_tab:
        render_skills_view(result["analysis"]["skills"])
        st.caption("Skills are matched against the editable catalog in `data/skills.json`.")
    with feedback_tab:
        render_ai_feedback(result["feedback"])
    with interview_tab:
        render_interview_questions(result["questions"])
    with report_tab:
        st.subheader("Export your analysis")
        stem = safe_filename(result["filename"])
        json_bytes = build_json_report(result["filename"], result["analysis"], result["recommendations"])
        pdf_bytes = build_pdf_report(result["filename"], result["analysis"], result["recommendations"])
        pdf_col, json_col = st.columns(2)
        pdf_col.download_button(
            "Download PDF report",
            data=pdf_bytes,
            file_name=f"{stem}-analysis.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        json_col.download_button(
            "Download JSON data",
            data=json_bytes,
            file_name=f"{stem}-analysis.json",
            mime="application/json",
            use_container_width=True,
        )
        st.warning("Use this score as coaching guidance only—not as an automated hiring decision.")

