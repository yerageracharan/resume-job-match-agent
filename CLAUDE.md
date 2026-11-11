# Claude Code project instructions

## Product invariants
- Do not invent candidate experience, skills, employers, qualifications, projects, dates, results, or metrics.
- Every match or rewritten claim must be traceable to supplied resume evidence.
- Label requirement priority as inferred unless directly confirmed by the user.
- Never call weighted skill coverage an ATS score or hiring probability.
- Preserve local-first behavior and keep model API calls optional and explicit.

## Engineering rules
- Keep analysis deterministic and testable in `agent.py`.
- Keep document extraction in `documents.py`.
- Keep MCP tools thin wrappers around the tested core functions.
- Never write MCP protocol messages or debug output to stdout; use stderr for logs.
- Add tests for parsing, scoring, evidence mapping, file handling, and failure cases.
- Do not silently change the scoring formula. Update README and tests together.
