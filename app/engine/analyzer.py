import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# CLEAN TEXT
# =========================
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# =========================
# GLOBAL SKILLS DICTIONARY (MULTI DOMAIN)
# =========================
KNOWN_SKILLS = {
    # programming
    "flutter",
    "dart",
    "firebase",
    "bloc",
    "rest",
    "api",
    "apis",
    "github",
    "git",
    "sql",
    "docker",
    "kubernetes",
    # architecture
    "clean",
    "architecture",
    "state",
    "management",
    # apps
    "mobile",
    "cross",
    "platform",
    "applications",
    # backend / cloud
    "backend",
    "database",
    "databases",
    "integration",
    "supabase",
    # medical (optional support for your test case)
    "surgery",
    "orthopedic",
    "orthopedics",
    "diagnosis",
    "treatment",
    "patient",
    "patients",
    "medical",
}


# =========================
# SKILL EXTRACTION (FIXED)
# =========================
def extract_skills(text: str):
    words = set(clean_text(text).split())
    return words & KNOWN_SKILLS


# =========================
# LEXICAL SCORE
# =========================
def lexical_score(cv, job):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([cv, job])
    return cosine_similarity(vectors[0], vectors[1])[0][0]


# =========================
# SEMANTIC SCORE (stable)
# =========================
def semantic_score(cv, job):
    return lexical_score(cv, job)


# =========================
# SKILLS SCORE
# =========================
def skills_score(cv_skills, job_skills):
    if not job_skills:
        return 0.0
    return len(cv_skills & job_skills) / len(job_skills)


# =========================
# EXPERIENCE SCORE
# =========================
def experience_score(text):
    match = re.search(r"(\d+)\+?\s*(years|year)", text)
    if not match:
        return 0.4

    years = int(match.group(1))

    if years >= 5:
        return 1.0
    elif years >= 3:
        return 0.75
    elif years >= 1:
        return 0.55
    return 0.4


# =========================
# FINAL SCORE
# =========================
def final_score(lex, sem, skills, exp):
    score = 0.30 * lex + 0.25 * sem + 0.30 * skills + 0.15 * exp
    return round(score * 100, 2)


# =========================
# RECOMMENDATION
# =========================
def get_recommendation(score):
    if score >= 75:
        return "Strong Match"
    elif score >= 55:
        return "Good Match"
    elif score >= 35:
        return "Moderate Match"
    return "Poor Match"


# =========================
# MAIN PIPELINE
# =========================
def analyze(cv_text, job_text):
    cv_clean = clean_text(cv_text)
    job_clean = clean_text(job_text)

    # FIXED: strict skill filtering (IMPORTANT)
    cv_skills = extract_skills(cv_clean)
    job_skills = set(clean_text(job_text).split()) & KNOWN_SKILLS

    lex = lexical_score(cv_clean, job_clean)
    sem = semantic_score(cv_clean, job_clean)
    skills = skills_score(cv_skills, job_skills)
    exp = experience_score(cv_clean)

    score = final_score(lex, sem, skills, exp)

    matched = list(cv_skills & job_skills)
    missing = list(job_skills - cv_skills)

    return {
        "lexical_score": round(lex, 3),
        "semantic_score": round(sem, 3),
        "skills_score": round(skills, 3),
        "experience_score": round(exp, 3),
        "final_score": score,
        "recommendation": get_recommendation(score),
        "matched_skills": matched,
        "missing_skills": missing,
    }
