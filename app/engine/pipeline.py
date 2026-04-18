import os
import re

from .scoring import compute_final_score, get_recommendation
from .semantic import compute_semantic_score
from .skills import match_skills
from .text_extractor import extract_text_from_pdf


# =========================
# LOAD INPUT
# =========================
def load_input(data):
    if isinstance(data, str) and data.lower().endswith(".pdf") and os.path.exists(data):
        return extract_text_from_pdf(data)
    return data or ""


# =========================
# CLEAN TOKENS (🔥 FIX engineerwe)
# =========================
def clean_tokens(tokens):
    return [t for t in tokens if len(t) > 2 and t.isalpha()]


# =========================
# EXPERIENCE
# =========================
def estimate_experience(cv_text):
    text = cv_text.lower()

    years = re.findall(r"(\d+)\s*\+?\s*years?", text)

    if years:
        y = max([int(i) for i in years])
        if y >= 6:
            return 1.0
        elif y >= 3:
            return 0.7
        elif y >= 1:
            return 0.4

    # fallback
    if any(k in text for k in ["flutter", "developed", "projects", "engineer"]):
        return 0.5

    return 0.2


# =========================
# INVALID SKILLS
# =========================
INVALID_SKILLS = {
    "understanding",
    "knowledge",
    "looking",
    "requirements",
    "responsibilities",
    "problem",
    "team",
    "members",
    "plus",
    "experience",
    "skills",
    "code",
    "solving",
}


# =========================
# CLEAN SKILLS
# =========================
def clean_skills(skills):
    cleaned = []
    for s in skills:
        s = s.lower().strip()

        if s in INVALID_SKILLS:
            continue
        if len(s) <= 2:
            continue
        if not s.isalpha():
            continue

        cleaned.append(s)

    return list(set(cleaned))


# =========================
# SKILL SCORE
# =========================
def compute_skill_score(matched, missing):
    matched = clean_skills(matched)
    missing = clean_skills(missing)

    total = len(matched) + len(missing)

    if total == 0:
        return 0.0, [], []

    base_score = len(matched) / total

    penalty = min(len(missing) * 0.005, 0.15)

    final_score = max(base_score - penalty, 0.0)

    return final_score, matched, missing


# =========================
# LEXICAL SCORE (🔥 FIX هنا)
# =========================
def compute_lexical(cv_text, job_text):
    cv_tokens = clean_tokens(re.findall(r"[a-zA-Z]+", cv_text.lower()))
    job_tokens = clean_tokens(re.findall(r"[a-zA-Z]+", job_text.lower()))

    cv_set = set(cv_tokens)
    job_set = set(job_tokens)

    if not job_set:
        return 0.0

    overlap = cv_set & job_set

    return min(len(overlap) / len(job_set), 1.0)


# =========================
# MAIN PIPELINE
# =========================
def run_pipeline(cv_input: str, job_input: str):
    cv_text = load_input(cv_input)
    job_text = load_input(job_input)

    if not cv_text.strip() or not job_text.strip():
        return {"error": "Empty input"}

    # -------- SKILLS --------
    skill_result = match_skills(cv_text, job_text)

    skills_score, matched_skills, missing_skills = compute_skill_score(
        skill_result["matched_skills"], skill_result["missing_skills"]
    )

    # -------- LEXICAL --------
    lexical_score = compute_lexical(cv_text, job_text)

    # -------- SEMANTIC --------
    semantic_score = compute_semantic_score(cv_text, job_text)
    semantic_score = min(max(semantic_score, 0.0), 1.0)

    # -------- EXPERIENCE --------
    experience_score = estimate_experience(cv_text)

    # -------- FINAL --------
    final_score = compute_final_score(lexical_score, semantic_score, skills_score, experience_score)

    return {
        "lexical_score": round(lexical_score, 3),
        "semantic_score": round(semantic_score, 3),
        "skills_score": round(skills_score, 3),
        "experience_score": round(experience_score, 3),
        "final_score": final_score,
        "recommendation": get_recommendation(final_score),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
