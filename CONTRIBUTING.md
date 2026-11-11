# Contributing

Thanks for improving Resume Job Match Agent. The project helps applicants understand how their documented experience maps to a job. It must improve clarity without inventing qualifications or overstating what its score means.

## Before changing code

- Search existing issues and commits for related work.
- Open an issue before changing scoring semantics, document formats, MCP tools, or report schema. Include the user problem, proposed behavior, privacy implications, alternatives, and validation plan.
- For bugs, provide synthetic resume/job-description text, exact command, expected result, actual result, and redacted logs.
- Keep parser, scoring, UI, and Claude integration changes focused.

## Development setup

Python 3.11 or newer.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For Claude Desktop/MCP setup, install the additional requirements only when needed:

```bash
python -m pip install -r requirements-claude.txt
```

## Validation

```bash
python -m unittest discover -s tests -v
streamlit run app.py
```

Use synthetic resumes and job descriptions in tests. Add regression coverage for document extraction, skill aliases, requirement-priority inference, wrapped lines, evidence mapping, and cases where unknown skills should not create a fake score.

## Engineering expectations

- Never add a skill or achievement unless it appears in source material or is explicitly confirmed by the user.
- Keep weighted coverage and inferred priority semantics transparent.
- Do not market the score as an ATS score or hiring probability.
- Keep the deterministic matching engine local-first; make any external model/data transfer explicit.
- Do not log, commit, or screenshot real resumes, contact details, or private job application data.
- Update README/docs when formats, scoring, MCP tools, or privacy behavior changes.

## Pull requests

Use the PR template. Include the problem, applicant impact, exact tests/results, and remaining limitations. Link an issue for non-trivial work.

## Security and privacy

Use [SECURITY.md](SECURITY.md) for private vulnerability reports. Treat resumes and job descriptions as sensitive data and use synthetic fixtures only.
