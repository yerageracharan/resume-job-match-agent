from __future__ import annotations

import hashlib
import json

import streamlit as st

from agent import analyze, format_report
from documents import extract_text_from_bytes

st.set_page_config(page_title="Resume Job Match Agent", page_icon="🎯", layout="wide")
st.title("Resume Job Match Agent")
st.caption("Evidence-first resume analysis. Runs locally; no model API key required for matching.")

with st.sidebar:
    st.header("How the score works")
    st.write("The score measures weighted coverage of skills recognised in the job description.")
    st.write("It is not an ATS score or a prediction of whether you will get hired.")
    st.divider()
    st.caption("Your resume text is processed by this local app. Do not upload documents you are not authorised to share.")

left, right = st.columns([1, 1])
with left:
    st.subheader("1. Your resume")
    uploaded = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if uploaded is not None:
        signature = f"{uploaded.name}:{hashlib.sha256(uploaded.getvalue()).hexdigest()}"
        if st.session_state.get("last_uploaded_signature") != signature:
            try:
                extracted = extract_text_from_bytes(uploaded.getvalue(), uploaded.name)
                st.session_state["resume_text"] = extracted
                st.session_state["last_uploaded_signature"] = signature
                st.success(f"Extracted text from {uploaded.name}")
            except ValueError as exc:
                st.error(str(exc))
    resume = st.text_area(
        "Resume text (review extracted text before analysis)",
        key="resume_text",
        height=360,
        placeholder="Upload a resume or paste its text here...",
    )
with right:
    st.subheader("2. Target job")
    jd = st.text_area("Paste the complete job description", height=430, placeholder="Paste the job description here...")

run = st.button("Analyse this application", type="primary", use_container_width=True)
if run:
    if not resume.strip() or not jd.strip():
        st.error("Add both a resume and a job description.")
    else:
        try:
            report = analyze(resume, jd)
            st.session_state["latest_report"] = format_report(report)
            st.session_state["latest_json"] = report.to_dict()
        except (TypeError, ValueError) as exc:
            st.error(str(exc))

if st.session_state.get("latest_report"):
    report_data = st.session_state["latest_json"]
    st.divider()
    st.subheader("3. Your application analysis")
    m1, m2, m3 = st.columns(3)
    m1.metric("Weighted skill coverage", f"{report_data['score']}%")
    m2.metric("Detected skills matched", f"{report_data['matched_count']} / {report_data['job_skill_count']}")
    m3.metric("Inferred required skills", f"{report_data['required_matched_count']} / {report_data['required_count']}")
    st.caption("Coverage is based only on detected skills and inferred priority. It is not an ATS score or hiring probability.")

    tab1, tab2, tab3 = st.tabs(["Skill evidence", "Next actions", "Limitations"])
    with tab1:
        for row in report_data["skills"]:
            title = f"{'✅' if row['present'] else '⚠️'} {row['skill']} · {row['priority']}"
            with st.expander(title):
                st.write(f"**Category:** {row['group']}")
                st.write("**Evidence in your resume**")
                if row["resume_evidence"]:
                    for item in row["resume_evidence"]:
                        st.write(f"- {item}")
                else:
                    st.write("No supporting sentence detected.")
                if row["job_context"]:
                    st.write("**Job description context**")
                    for item in row["job_context"]:
                        st.write(f"- {item}")
    with tab2:
        for item in report_data["recommendations"]:
            st.write(f"- {item}")
        st.info("Never add a skill, responsibility, employer, qualification, or metric unless it is true and you can support it.")
    with tab3:
        for item in report_data["limitations"]:
            st.write(f"- {item}")

    st.download_button("Download full report (Markdown)", st.session_state["latest_report"], file_name="resume-job-match-report.md", mime="text/markdown")
    st.download_button("Download structured report (JSON)", json.dumps(report_data, indent=2), file_name="resume-job-match-report.json", mime="application/json")
