"""Local MCP server for Claude Desktop, Claude Code, and compatible hosts.

The server exposes the same transparent analysis engine as the Streamlit app.
It reads local resume files only when the user provides an explicit file path.
"""
from __future__ import annotations

from agent import analyze, format_report
from documents import extract_text_from_path
from mcp.server import MCPServer

mcp = MCPServer("Resume Job Match Agent")


@mcp.tool()
def analyze_resume_match(resume_text: str, job_description: str) -> dict:
    """Compare resume text with a job description and return a structured, evidence-backed skill report."""
    report = analyze(resume_text, job_description)
    result = report.to_dict()
    result["report_markdown"] = format_report(report)
    return result


@mcp.tool()
def analyze_resume_file(resume_path: str, job_description: str) -> dict:
    """Read a user-selected local PDF, DOCX, or TXT resume and compare it with a job description."""
    resume_text = extract_text_from_path(resume_path)
    report = analyze(resume_text, job_description)
    result = report.to_dict()
    result["source_file"] = resume_path
    result["report_markdown"] = format_report(report)
    return result


@mcp.tool()
def get_resume_evidence(resume_text: str, skill: str) -> dict:
    """Find resume sentences that mention a skill; use these as evidence when Claude suggests edits."""
    from agent import _contexts_for_skill, extract_skills
    detected = sorted(extract_skills(resume_text))
    canonical = next((item for item in detected if item == skill.lower()), skill.lower())
    evidence = _contexts_for_skill(resume_text, canonical)
    return {
        "requested_skill": skill,
        "detected_skill": canonical if canonical in detected else None,
        "evidence": evidence,
        "warning": "Only use claims and metrics explicitly supported by the user's resume. Ask the user before adding new facts.",
    }


if __name__ == "__main__":
    mcp.run()
