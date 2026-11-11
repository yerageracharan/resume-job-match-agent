# Agent Instructions

These instructions apply across Resume Job Match Agent.

## Product and privacy invariants

- Never invent a candidate's skills, employers, qualifications, projects, dates, responsibilities, achievements, or metrics.
- Every matched skill and suggested rewrite must remain traceable to text the candidate supplied; distinguish detected keyword presence from demonstrated proficiency.
- The score is weighted coverage of recognized skills, not an ATS score, hiring probability, or prediction of interview outcomes.
- Required/preferred labels are inferred heuristics; preserve the original job-description context so users can verify them.
- Treat resumes and job descriptions as sensitive personal data. Keep local-first behavior clear and disclose that Claude receives content under the user's Claude account/privacy settings when used.

## Repository map

- `agent.py`: deterministic skill vocabulary, matching, scoring, evidence, and report formatting.
- `documents.py`: PDF/DOCX/TXT extraction boundaries.
- `app.py`: Streamlit interface.
- `mcp_server.py`: local MCP tools for text and user-selected local files.
- `configure_claude.py` and `setup_claude_windows.bat`: Claude Desktop configuration helpers.
- `tests/`: unit and document-extraction tests.
- `docs/`: user and developer handbook.

## Working rules

- Never fabricate candidate facts, skills, dates, metrics, employers, or education.
- Treat phrase matching as detection, not proficiency verification.
- Preserve the distinction between required/preferred inferred heuristics and confirmed job requirements.
- When modifying score calculation, update methodology documentation and tests together.
- Keep document parsing bounded; reject unsupported/empty files clearly.
- Never persist or log uploaded resume contents unnecessarily.
- Explain that using Claude sends content to Claude under the user's account/privacy terms; do not call the whole workflow offline when Claude is involved.
- Do not add automatic job applications, email sending, or external submission actions without a separate explicit design and opt-in.

## Validation

```bash
python -m unittest discover -s tests -v
streamlit run app.py
```

## Change ownership and proof

- Keep one authoritative owner for each domain rule and each persisted state. UI, CLI, MCP, and provider adapters translate inputs and outputs; they must not reimplement business policy or become competing sources of truth.
- Before changing a contract, trace the input through its owner to every consumer. Update callers, schemas, examples, docs, and regression tests together. Remove superseded paths unless a documented public-compatibility requirement keeps them.
- Keep optional external model/provider integrations behind adapters. Use injected or mocked adapters for deterministic unit tests; label live network/provider checks separately and never describe a mock as live verification.
- Validate untrusted user, model, file, and network data at the boundary. Preserve the product's evidence/provenance rules and reject malformed inputs rather than silently inventing defaults.
- Verify the supported user entry point and at least one relevant failure path. Report exact commands and results; CI on a different commit SHA is not proof for the current change.
- Keep the root README as the user entry point, `docs/README.md` as the documentation map, and focused guides as the owners of detailed contracts. Update links when files move. Do not hand-edit generated output when a source or generator owns it.
