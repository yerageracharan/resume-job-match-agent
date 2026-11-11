# Benchmark notes — Agent #10

**Research snapshot:** 11 November 2026. Repository activity, stars, and feature sets change; re-check upstream repositories before making comparative claims in public content.

## Selected references

### 1. srbhr/Resume-Matcher
https://github.com/srbhr/Resume-Matcher

A strong direct product reference. Its repository describes a master-resume workflow, tailored resumes, local/remote LLM support, deterministic ATS checks, multiple templates, and MCP/agent integration.

**Adopt:** evidence-backed deterministic checks, local-first options, and MCP as an integration boundary.

**Defer:** a full resume editor, multiple provider adapters, application database, queues, and template renderer. Those features would overwhelm a one-day challenge build.

### 2. xitanggg/open-resume
https://github.com/xitanggg/open-resume

A useful reference for resume creation/parsing and document-centric usability.

**Adopt:** make document import first-class and let users inspect extracted content before analysis.

### 3. kbaas-ai/reparse-oss
https://github.com/kbaas-ai/reparse-oss

Its README describes a self-hosted workflow that confirms resume lines, ties scoring to resume evidence, and reports gaps.

**Adopt:** source-grounded findings and a hard boundary against inventing candidate experience.

### 4. simeononsecurity/ats-resume-improver
https://github.com/simeononsecurity/ats-resume-improver

Its README describes local resume parsing/ATS checks, multiple document formats, optional Anthropic/OpenAI/Ollama support, and export formats.

**Adopt:** separate local deterministic analysis from optional AI-assisted workflows.

### 5. sliday/resume-job-matcher
https://github.com/sliday/resume-job-matcher

A resume-screening workflow describing a staged pipeline: optional similarity prefilter, hard-constraint checks, and evidence-anchored scoring.

**Adopt:** keep hard eligibility constraints separate from a skills score. This is deferred because work authorisation, location, and licence checks require user confirmation.

### 6. OmkarPathak/pyresparser
https://github.com/OmkarPathak/pyresparser

A historical Python resume-extraction reference. It is not selected as a core dependency.

**Adopt:** the idea of a focused parser boundary, not the entire dependency or architecture.

## Product gap

The MVP answers four questions:

1. Which recognised job-description skills also appear in this resume?
2. Which resume sentences provide evidence for each match?
3. Which gaps appear important, and how was priority inferred?
4. What should the applicant inspect or improve next without inventing experience?

## Claims we intentionally do not make

- Not a real ATS simulator.
- Not a hiring probability model.
- Not a semantic model or LLM-powered scorer.
- Not a guarantee of interviews or employment.
- Not an exhaustive parser for every resume layout or a scanned-PDF OCR system.

## Value-creation design lens

Applying the value-equation idea from the user's business reference library:

- Desired outcome: a clearer, more relevant job application.
- Perceived likelihood: show evidence sentences and expose how the report was calculated.
- Time delay: produce a useful result immediately after upload and paste.
- Effort: accept common file types, prefill resume text, and export the report.

The principle is to reduce user work and uncertainty, not inflate promises.
