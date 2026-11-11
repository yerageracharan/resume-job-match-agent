"""Transparent, evidence-first resume/job matching engine.

The scoring engine is deliberately deterministic. It reports skill coverage, not
an ATS score or a probability of getting hired.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass

# Canonical skill -> common spellings. Keep this list editable and domain-specific.
SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "python": ("python",),
    "java": ("java",),
    "javascript": ("javascript",),
    "typescript": ("typescript",),
    "c++": ("c++", "cpp"),
    "c#": ("c#", "c sharp"),
    "sql": ("sql", "structured query language"),
    "r": ("r programming", "r language"),
    "go": ("golang", "go language"),
    "rust": ("rust",),
    "machine learning": ("machine learning",),
    "deep learning": ("deep learning",),
    "natural language processing": ("natural language processing", "nlp"),
    "pandas": ("pandas",),
    "numpy": ("numpy",),
    "pytorch": ("pytorch", "torch"),
    "tensorflow": ("tensorflow",),
    "scikit-learn": ("scikit-learn", "scikit learn", "sklearn"),
    "data analysis": ("data analysis", "data analytics", "analysing data", "analyzing data"),
    "statistics": ("statistics", "statistical analysis"),
    "large language models": ("large language models", "large language model", "llm", "llms"),
    "generative ai": ("generative ai", "genai"),
    "react": ("react", "react.js", "reactjs"),
    "node.js": ("node.js", "nodejs", "node js"),
    "html": ("html", "html5"),
    "css": ("css", "css3"),
    "fastapi": ("fastapi", "fast api"),
    "flask": ("flask",),
    "django": ("django",),
    "rest apis": ("rest api", "rest apis", "restful api", "restful apis"),
    "git": ("git",),
    "github": ("github",),
    "docker": ("docker", "containers"),
    "linux": ("linux",),
    "aws": ("aws", "amazon web services"),
    "azure": ("azure", "microsoft azure"),
    "google cloud": ("google cloud", "gcp"),
    "kubernetes": ("kubernetes", "k8s"),
    "ci/cd": ("ci/cd", "continuous integration", "continuous delivery", "continuous deployment"),
    "terraform": ("terraform",),
    "cloud computing": ("cloud computing", "cloud infrastructure"),
    "communication": ("communication", "written communication", "verbal communication"),
    "leadership": ("leadership", "team leadership"),
    "project management": ("project management", "project planning"),
    "agile": ("agile", "agile methodology"),
    "scrum": ("scrum",),
    "stakeholder management": ("stakeholder management", "stakeholder communication"),
    "problem solving": ("problem solving", "problem-solving", "analytical thinking"),
    "data visualization": ("data visualization", "data visualisation", "dashboarding"),
    "excel": ("excel", "microsoft excel"),
    "power bi": ("power bi", "powerbi"),
    "tableau": ("tableau",),
    "mongodb": ("mongodb", "mongo db"),
    "postgresql": ("postgresql", "postgres"),
    "mysql": ("mysql",),
    "redis": ("redis",),
    "unit testing": ("unit testing", "unit tests"),
    "api design": ("api design", "api development"),
}

SKILL_GROUPS: dict[str, tuple[str, ...]] = {
    "Programming": ("python", "java", "javascript", "typescript", "c++", "c#", "sql", "r", "go", "rust"),
    "AI & Data": ("machine learning", "deep learning", "natural language processing", "pandas", "numpy", "pytorch", "tensorflow", "scikit-learn", "data analysis", "statistics", "large language models", "generative ai", "data visualization"),
    "Web & Software": ("react", "node.js", "html", "css", "fastapi", "flask", "django", "rest apis", "git", "github", "docker", "linux", "mongodb", "postgresql", "mysql", "redis", "unit testing", "api design"),
    "Cloud & DevOps": ("aws", "azure", "google cloud", "kubernetes", "ci/cd", "terraform", "cloud computing"),
    "Business & Collaboration": ("communication", "leadership", "project management", "agile", "scrum", "stakeholder management", "problem solving", "excel", "power bi", "tableau"),
}

# Stronger requirement language receives more weight. This classification is a
# heuristic; the UI calls it inferred priority, not an objective job requirement.
REQUIRED_RE = re.compile(r"\b(required|requirements?|must have|must-have|minimum|mandatory|need to|you will need|essential|proficient in|experience with|qualifications?)\b", re.I)
PREFERRED_RE = re.compile(r"\b(preferred|nice to have|nice-to-have|bonus|a plus|desirable|ideally|familiarity with)\b", re.I)


@dataclass
class SkillEvidence:
    skill: str
    group: str
    priority: str
    resume_evidence: list[str]
    job_context: list[str]
    present: bool
    weight: int


@dataclass
class MatchReport:
    score: int
    matched_count: int
    job_skill_count: int
    required_count: int
    required_matched_count: int
    matched_skills: list[str]
    missing_skills: list[str]
    resume_only_skills: list[str]
    evidence: dict[str, list[str]]
    skills: list[SkillEvidence]
    recommendations: list[str]
    limitations: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def normalize(text: str) -> str:
    text = text.lower().replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"\s+", " ", text).strip()


def _contains_phrase(text: str, phrase: str) -> bool:
    # Keep boundary checks robust for punctuation-heavy tokens such as C++ and C#.
    escaped = re.escape(phrase.lower())
    return bool(re.search(r"(?<![a-z0-9])" + escaped + r"(?![a-z0-9])", text, re.I))


def _skill_group(skill: str) -> str:
    for group, skills in SKILL_GROUPS.items():
        if skill in skills:
            return group
    return "Other"


def extract_skills(text: str) -> set[str]:
    haystack = normalize(text)
    found: set[str] = set()
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_phrase(haystack, alias) for alias in aliases):
            found.add(canonical)
    return found


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"(?<=[.!?])\s+|\n+|\s+[•●▪]\s+", text)
    return [re.sub(r"\s+", " ", item).strip(" \t-•") for item in chunks if len(item.strip()) > 12]


def _contexts_for_skill(text: str, skill: str) -> list[str]:
    aliases = SKILL_ALIASES.get(skill, (skill,))
    contexts = [
        sentence for sentence in split_sentences(text)
        if any(_contains_phrase(normalize(sentence), alias) for alias in aliases)
    ][:5]
    if contexts:
        return contexts

    # PDF extraction can wrap a multi-word skill across adjacent lines. Recover
    # a two-line source window so a detected skill still has inspectable evidence.
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index in range(len(lines) - 1):
        window = f"{lines[index]} {lines[index + 1]}"
        if any(_contains_phrase(normalize(window), alias) for alias in aliases):
            contexts.append(window)
            if len(contexts) == 5:
                break
    return contexts


def _job_priority(contexts: list[str], skill: str) -> tuple[str, int]:
    """Infer priority from the nearest requirement phrase to this skill mention.

    Evaluating the whole sentence makes a phrase like "Required: Python; Preferred:
    AWS" incorrectly mark both skills as required. Clause boundaries and nearest
    marker distance keep mixed-priority lists skill-specific.
    """
    aliases = SKILL_ALIASES.get(skill, (skill,))
    candidates: list[tuple[int, str]] = []
    for context in contexts:
        normalized = normalize(context)
        for alias in aliases:
            pattern = re.compile(r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])", re.I)
            for mention in pattern.finditer(normalized):
                separators = [m.start() for m in re.finditer(r"[;•]", normalized)]
                left = max((position + 1 for position in separators if position < mention.start()), default=0)
                right = min((position for position in separators if position >= mention.end()), default=len(normalized))
                clause = normalized[left:right]
                mention_start = mention.start() - left
                mention_end = mention.end() - left
                for label, expression in (("Required (inferred)", REQUIRED_RE), ("Preferred (inferred)", PREFERRED_RE)):
                    for marker in expression.finditer(clause):
                        if marker.end() <= mention_start:
                            distance = mention_start - marker.end()
                        elif marker.start() >= mention_end:
                            distance = marker.start() - mention_end
                        else:
                            distance = 0
                        candidates.append((distance, label))
    if not candidates:
        return "Unclassified", 1
    distance, label = min(candidates, key=lambda item: (item[0], 0 if item[1].startswith("Required") else 1))
    return (label, 2) if label.startswith("Required") else (label, 1)


def analyze(resume: str, job_description: str) -> MatchReport:
    if not isinstance(resume, str) or not isinstance(job_description, str):
        raise TypeError("Resume and job description must be text strings.")
    if not resume.strip() or not job_description.strip():
        raise ValueError("Both resume and job description are required.")

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job_description)
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)
    resume_only = sorted(resume_skills - job_skills)

    skill_rows: list[SkillEvidence] = []
    evidence_by_skill: dict[str, list[str]] = {}
    weighted_total = 0
    weighted_earned = 0
    required = 0
    required_matched = 0
    for skill in sorted(job_skills):
        job_context = _contexts_for_skill(job_description, skill)
        priority, weight = _job_priority(job_context, skill)
        present = skill in resume_skills
        resume_evidence = _contexts_for_skill(resume, skill) if present else []
        skill_rows.append(SkillEvidence(skill, _skill_group(skill), priority, resume_evidence, job_context, present, weight))
        evidence_by_skill[skill] = resume_evidence
        weighted_total += weight
        weighted_earned += weight if present else 0
        if priority.startswith("Required"):
            required += 1
            if present:
                required_matched += 1

    score = round(100 * weighted_earned / weighted_total) if weighted_total else 0
    recs: list[str] = []
    required_gaps = [row.skill for row in skill_rows if not row.present and row.priority.startswith("Required")]
    preferred_gaps = [row.skill for row in skill_rows if not row.present and row.priority.startswith("Preferred")]
    unclassified_gaps = [row.skill for row in skill_rows if not row.present and row.priority == "Unclassified"]
    if required_gaps:
        recs.append("Address the inferred required-skill gaps first: " + ", ".join(required_gaps) + ". Do not claim these skills unless you can demonstrate genuine experience.")
    if preferred_gaps:
        recs.append("Treat these as lower-priority gaps because the job text appears to label them preferred: " + ", ".join(preferred_gaps) + ".")
    if matched:
        recs.append("Strengthen the proof for skills you already have: " + ", ".join(matched) + ". Make the relevant project, task, tools, and actual outcome easy to find.")
    if unclassified_gaps:
        recs.append("Review these detected job skills manually; the description did not clearly label their priority: " + ", ".join(unclassified_gaps) + ".")
    if not job_skills:
        recs.append("No skills from the built-in vocabulary were detected in the job description. Add missing domain terms or inspect the role manually before relying on this report.")
    if not recs:
        recs.append("No recognised skill gap was detected. Review responsibilities and add concrete evidence of your impact where it is currently missing.")

    limitations = [
        "The score is weighted coverage of recognised skills, not an ATS score, hiring probability, or measure of candidate quality.",
        "Required/preferred labels are inferred from nearby wording and can be wrong; verify them against the original job description.",
        "The vocabulary is curated, not exhaustive. Synonyms, transferable skills, seniority, years of experience, credentials, and context may be missed.",
        "A matched skill means the term appears in the resume; it does not verify proficiency or quality of experience.",
    ]
    return MatchReport(score, len(matched), len(job_skills), required, required_matched,
                       matched, missing, resume_only, evidence_by_skill, skill_rows, recs, limitations)


def format_report(report: MatchReport) -> str:
    lines = [
        "# Resume-to-Job Match Report",
        "",
        f"**Weighted recognised-skill coverage: {report.score}%**",
        f"Matched {report.matched_count} of {report.job_skill_count} detected job skills.",
        f"Inferred required skills matched: {report.required_matched_count}/{report.required_count}",
        "",
        "## Skill-by-skill findings",
    ]
    if not report.skills:
        lines.append("No skills were detected from the current vocabulary.")
    for row in report.skills:
        state = "MATCH" if row.present else "GAP"
        lines.append(f"### {row.skill} — {state}")
        lines.append(f"Group: {row.group} | Priority: {row.priority}")
        if row.resume_evidence:
            lines.extend(f"- Resume evidence: {item}" for item in row.resume_evidence)
        else:
            lines.append("- Resume evidence: no supporting sentence detected")
        if row.job_context:
            lines.extend(f"- Job context: {item}" for item in row.job_context)
    lines += ["", "## Recommendations"]
    lines.extend(f"- {item}" for item in report.recommendations)
    lines += ["", "## Limitations"]
    lines.extend(f"- {item}" for item in report.limitations)
    return "\n".join(lines)
