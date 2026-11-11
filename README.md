# Resume Job Match Agent

**Agent #8 — 200 AI Agents in 200 Days**

An evidence-first resume analysis tool with a local Streamlit interface and a Model Context Protocol (MCP) server for Claude Desktop, Claude Code, and other compatible AI clients.

The product goal is simple: help a job seeker understand how their real experience maps to a specific job, see the evidence behind every detected match, and decide what to improve next. It must never invent experience, skills, employers, qualifications, or performance metrics.

## Features

- Resume upload: selectable-text PDF, DOCX, and TXT.
- Evidence-first analysis: resume sentences and job-description context for each detected skill.
- Transparent scoring: weighted coverage of skills recognised by the built-in vocabulary. This is not an ATS score or hiring probability.
- Requirement prioritisation: heuristically labels job skills as required, preferred, or unclassified. Labels are inferred and should be checked.
- Actionable gaps: separates inferred required gaps from preferred gaps; never encourages applicants to claim skills they do not have.
- Export: Markdown and JSON reports.
- Claude integration through MCP: Claude can call the same local engine, analyse a user-selected local resume file, and retrieve resume evidence.
- Local-first matching: no model API key or cloud service is needed for the scoring engine.

## Quick start — Windows

Requirements: Python 3.11 or newer.

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Upload a PDF, DOCX, or TXT resume, review the extracted text, paste a job description, and select **Analyse this application**.

## Connect Claude Desktop on Windows

1. Install and open Claude Desktop once.
2. Double-click `setup_claude_windows.bat` from the extracted project folder.
3. The script creates `.venv`, installs the MCP/document-extraction dependencies, and adds the MCP server to Claude Desktop's configuration while preserving other configured servers.
4. Fully quit Claude Desktop and reopen it.
5. Check **Settings → Developer** for `resume-job-match`.

The script configures a local stdio server. Claude launches `mcp_server.py` as a child process.

### Claude Code

After installing dependencies in `.venv`, run this from the project folder:

```bat
claude mcp add resume-job-match -- ".venv\Scripts\python.exe" "%CD%\mcp_server.py"
```

Run `/mcp` inside Claude Code to verify the tools are available.

### MCP tools

| Tool | Purpose |
|---|---|
| `analyze_resume_match` | Analyse resume text against a job description and return structured findings plus a Markdown report |
| `analyze_resume_file` | Extract a local PDF/DOCX/TXT path supplied by the user, then analyse it |
| `get_resume_evidence` | Retrieve source sentences mentioning a skill to ground suggested edits |

Example Claude prompt:

> Use the Resume Job Match Agent MCP tools to analyse `C:\Users\Me\Documents\resume.pdf` against this job description. Explain the biggest gaps, cite the resume sentences that support the matches, and propose truthful edits. Do not add any skill, employer, qualification, project, result, or metric not supported by the resume. Ask me when evidence is missing.

## Scoring methodology

The score is **weighted coverage of skills recognised by the current vocabulary**:

- Detected skills in the job description receive weight 2 when nearby language suggests a requirement (for example, “required” or “must have”).
- Skills labelled preferred or not clearly classified receive weight 1.
- A detected skill present in the resume earns its weight; missing skills earn zero.
- Score = earned weight / total detected-job-skill weight.

Priority classification is heuristic and may be wrong. The app shows the job-description context so users can verify it. A term match does not prove proficiency.

## Privacy and safety

- Streamlit matching runs locally; it does not send resumes to a third-party API.
- The MCP server reads only a local file path explicitly supplied to its tool.
- When Claude is asked to analyse resume content, that information is sent to Claude under the user's Claude plan and privacy settings. This is not an offline Claude workflow.
- Review extracted text before relying on the report, especially for tables, columns, symbols, or scanned PDFs.
- Do not use a score as an automated hiring decision.
- Never add claims to a resume unless the user confirms they are true.

## Tests

```bat
python -m unittest discover -s tests -v
```

## Project structure

```text
resume-job-match-agent/
├── agent.py
├── app.py
├── documents.py
├── mcp_server.py
├── configure_claude.py
├── setup_claude_windows.bat
├── requirements.txt
├── requirements-claude.txt
├── tests/
│   ├── test_agent.py
│   └── test_documents.py
├── BENCHMARK.md
├── CLAUDE.md
└── LICENSE
```

## Roadmap

- Semantic similarity for synonym/transferable-skill detection, with model and confidence clearly disclosed.
- Better resume section parsing and ATS text-layout diagnostics.
- User-confirmed master-resume facts and tailored bullet drafts with source traceability.
- Additional languages and role-specific skill vocabularies.
- Regression datasets built from consented, anonymised examples.

## License

MIT — see `LICENSE`.
