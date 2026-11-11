# 03 · Analysis Playbook — turn a score into a better application

> **Audience:** job seekers, career changers, and developers testing the matching engine.  
> **Goal:** understand what the engine detects, what it misses, and how to use its output without gaming the score or fabricating qualifications.

![Resume Job Match Agent characters](assets/dev-squad.webp)

**QA-chan's principle:** a matched word is a lead to inspect, not proof that someone is proficient. Read the evidence before trusting the result.

## 1. Prepare a good input pair

A useful analysis depends on the quality of the two inputs.

### Resume checklist

- Use the most recent version of your resume.
- Include the real projects, jobs, education, tools, and outcomes relevant to the role.
- Use selectable text in PDF rather than a photo of a printed page.
- Make sure the file is not password-protected.
- Keep tables simple where possible; complex layouts can affect reading order.
- Check the extracted text box before you click Analyse.
- Remove private details that are not needed for the review (full home address, government identifiers, private phone numbers, or references' contact details).

### Job-description checklist

- Paste the complete description, including responsibilities and qualifications.
- Preserve wording such as `required`, `must have`, `preferred`, and `nice to have` because the current priority heuristic looks for wording around skill mentions.
- Do not paste only the company mission or a generic job title.
- If a requirement is ambiguous, verify it manually on the original posting.

### Visual 25 — Input quality funnel

```mermaid
flowchart TD
  A[Resume + job description] --> B[Readable text?]
  B -->|No| C[Fix document / paste clean text]
  B -->|Yes| D[Complete job posting?]
  D -->|No| E[Collect responsibilities + qualifications]
  D -->|Yes| F[Review extraction]
  E --> F
  C --> F
  F --> G[Run analysis]
```

## 2. What exactly is a “skill” to this engine?

`agent.py` contains a curated dictionary named `SKILL_ALIASES`. Each canonical skill maps to common spellings. For example, `react` recognises `React`, `React.js`, and `ReactJS`; `postgresql` recognises `Postgres`; and `natural language processing` recognises `NLP`.

Detection is phrase-based and uses token boundaries to avoid some accidental substring matches. It is not semantic understanding. A sentence that says “built a forecasting model” may not match “machine learning” unless a recognised phrase appears. The current vocabulary is a starting set, not a complete labour-market ontology.

### Visual 26 — Alias resolution

```mermaid
flowchart TD
  A[Raw sentence] --> B[Lowercase + normalise whitespace]
  B --> C[Check each canonical skill]
  C --> D[Check its aliases with word boundaries]
  D --> E{Any alias found?}
  E -->|Yes| F[Return canonical skill]
  E -->|No| G[No recognised skill]
```

### Visual 27 — A phrase match is not semantic understanding

```mermaid
flowchart TD
  A[Job says: build predictive models] --> B[Phrase in curated vocabulary?]
  B -->|No| C[May be missed]
  B -->|Yes| D[Skill detected]
  D --> E[Look for phrase in resume]
  E --> F[Attach source sentence]
  F --> G[Human verifies meaning and proficiency]
```

### Visual 28 — Text normalisation and evidence extraction

```mermaid
flowchart LR
  A[Original document text] --> B[Normalise case and whitespace]
  B --> C[Split into sentences]
  C --> D[Find sentence containing alias]
  D --> E[Keep up to five evidence contexts]
  E --> F[Attach to skill row]
```

## 3. The scoring formula

For each skill recognised in the job description:

- Weight `2` when nearby wording matches the engine's inferred required-language rules.
- Weight `1` when nearby wording matches its preferred-language rules or no clear priority is identified.
- Earn the skill's weight when that canonical skill is also detected in the resume; otherwise earn zero.

**Formula**

`weighted coverage = (sum of weights for matched job skills / sum of weights for all detected job skills) × 100`

Rounded to the nearest whole number. If no job skills are detected, the score is `0` and the report warns that the vocabulary found nothing. Do not interpret that as zero candidate quality.

### Visual 29 — Score calculation pipeline

```mermaid
flowchart TD
  A[Detect job skills] --> B[Attach nearby job context]
  B --> C[Infer priority]
  C --> D[Assign weight 2 or 1]
  E[Detect resume skills] --> F[Find intersection]
  D --> G[Total possible weight]
  F --> H[Total earned weight]
  G --> I[Earned / possible × 100]
  H --> I
  I --> J[Round and report coverage]
```

### Visual 30 — Worked example

```mermaid
flowchart TD
  A[Job skills] --> B[Python required: 2]
  A --> C[SQL required: 2]
  A --> D[AWS preferred: 1]
  B --> E[Present in resume: 2 earned]
  C --> F[Present in resume: 2 earned]
  D --> G[Missing: 0 earned]
  E --> H[4 earned]
  F --> H
  G --> I[5 possible]
  H --> J[80% weighted coverage]
  I --> J
```

## 4. Priority labels are inferred, not authoritative

The code checks the sentence context around a skill for a list of words. The first required-language test has precedence over preferred-language detection. The labels in the UI explicitly say `(inferred)`.

This can be wrong. For example, a phrase such as “experience with Python is preferred” contains wording from both categories. Depending on the sentence, the current required-language pattern may take precedence. Treat the label as a review hint, not a legal or contractual interpretation of the job posting.

### Visual 31 — Priority classification and precedence

```mermaid
flowchart TD
  A[Skill context] --> B{Required phrase found?}
  B -->|Yes| C[Required inferred · weight 2]
  B -->|No| D{Preferred phrase found?}
  D -->|Yes| E[Preferred inferred · weight 1]
  D -->|No| F[Unclassified · weight 1]
```

## 5. Read the skill-by-skill table correctly

For each row, inspect:

- **Skill:** canonical term recognised by the engine.
- **Group:** broad category such as Programming, AI & Data, Web & Software, Cloud & DevOps, or Business & Collaboration.
- **Priority:** required/preferred/unclassified inference based on job text.
- **Resume evidence:** source sentences from the resume that mention the term.
- **Job context:** source sentences from the job description that mention it.
- **Present:** whether the canonical skill was detected in both inputs.
- **Weight:** the contribution to the denominator and, when matched, numerator.

### Visual 32 — Anatomy of one skill row

```mermaid
flowchart TD
  A[Skill row] --> B[Canonical skill]
  A --> C[Group]
  A --> D[Inferred priority + weight]
  A --> E[Resume evidence]
  A --> F[Job context]
  A --> G[Present / gap]
  E --> H[Human verification]
  F --> H
  D --> H
  G --> H
```

## 6. Turn gaps into actions

A missing term is not an instruction to add that term to the resume. Decide which kind of gap it is:

1. **You have the skill, but the resume does not say it clearly.** Add a truthful bullet or project detail and make the evidence easy to see.
2. **You have adjacent experience.** Explain the transferable task or tool honestly. Do not rename it as a skill you have not used.
3. **You do not have the skill yet.** Treat it as a learning objective, not as resume content.
4. **The engine misunderstood the job wording.** Reject or manually reclassify the finding in your own notes.
5. **The skill vocabulary missed a concept.** Add a vocabulary improvement through code contribution, but do not assume the score is complete today.

### Visual 33 — Gap triage decision tree

```mermaid
flowchart TD
  A[Detected gap] --> B{Do you genuinely have the skill?}
  B -->|Yes| C{Is it supported by a real example?}
  C -->|Yes| D[Rewrite bullet with the actual evidence]
  C -->|No| E[Ask for details or leave claim out]
  B -->|Adjacent experience| F[Describe transferable task precisely]
  B -->|No| G[Create a learning plan]
  B -->|Detection error| H[Ignore / report vocabulary issue]
```

### Visual 34 — Truthful resume rewrite loop

```mermaid
sequenceDiagram
  participant User
  participant Claude
  participant Tool as Evidence tool
  User->>Claude: Ask to improve a resume bullet
  Claude->>Tool: Retrieve evidence for the skill
  Tool-->>Claude: Source sentences or no evidence
  Claude->>Claude: Draft only from supported facts
  Claude-->>User: Original, proposed edit, evidence, questions
  User->>Claude: Confirm or correct missing details
  Claude-->>User: Final candidate wording
```

## 7. Write stronger bullets without inventing metrics

A useful bullet often contains **action + context + method/tool + outcome**. The outcome does not always need a number. If a metric is not present in the resume or confirmed by the user, leave a placeholder or ask.

Example transformation:

- Source: `Built a dashboard in Python for weekly sales reporting.`
- Safe rewrite: `Built a Python dashboard to consolidate weekly sales reporting and make recurring trends easier to review.`
- Unsafe rewrite: `Built a Python dashboard that increased revenue by 37% and reduced reporting time by 80%.` — those metrics were not supplied.

### Visual 35 — Bullet construction

```mermaid
flowchart LR
  A[Real action] --> B[Project / business context]
  B --> C[Tools actually used]
  C --> D[Observed outcome]
  D --> E[One concise bullet]
  F[Missing metric?] --> G[Ask user; do not estimate]
```

## 8. Export the right format

| Format | Best for | Notes |
|---|---|---|
| Markdown `.md` | Reading, reviewing, sharing with a mentor | Human-friendly headings and source evidence |
| JSON `.json` | Scripts, dashboards, future integrations | Structured fields and arrays; keep the raw file to preserve detail |

### Visual 36 — Export routing

```mermaid
flowchart TD
  A[Completed analysis] --> B{Who / what consumes it?}
  B -->|Person or mentor| C[Markdown report]
  B -->|Code or data pipeline| D[JSON report]
  C --> E[Review and annotate]
  D --> F[Parse and validate schema]
```

## 9. Quality-control checklist before using a finding

- [ ] Can I point to a sentence in my resume that supports this match?
- [ ] Does the sentence show real use, not only a list of keywords?
- [ ] Did the extracted text preserve the intended meaning?
- [ ] Is the priority label consistent with the full job description?
- [ ] Is the role genuinely relevant to my experience and interests?
- [ ] Have I removed private information from the version I plan to share?
- [ ] Did Claude add any claim or metric I did not provide?

### Visual 37 — Final review gate

```mermaid
flowchart TD
  A[Report ready] --> B[Check evidence]
  B --> C[Check job context]
  C --> D[Check priority]
  D --> E[Check every generated claim]
  E --> F{All true and relevant?}
  F -->|Yes| G[Use as a draft for your own review]
  F -->|No| H[Correct, remove, or ask a question]
  H --> E
```

### Visual 38 — What the score should and should not do

```mermaid
flowchart LR
  A[Weighted skill coverage] --> B[Prioritise review]
  A --> C[Find evidence gaps]
  A --> D[Compare versions cautiously]
  A -. never .-> E[Predict hiring outcome]
  A -. never .-> F[Replace recruiter judgement]
  A -. never .-> G[Prove proficiency]
```

---

**QA-chan's sign-off:** the report is useful only when you inspect the evidence and use your judgement. A score is a navigation aid, not a verdict.