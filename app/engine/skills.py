import re

STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "are",
    "this",
    "that",
    "job",
    "role",
    "will",
    "you",
    "our",
    "your",
    "responsibilities",
    "requirements",
    "looking",
    "candidate",
    "ability",
    "work",
    "team",
}


def tokenize(text):
    return re.findall(r"[a-zA-Z]+", text.lower())


def extract_keywords(text, top_n=30):
    tokens = tokenize(text)

    # remove stopwords + short words
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 3]

    # frequency
    freq = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1

    # sort by importance
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    keywords = [t[0] for t in sorted_tokens[:top_n]]

    return set(keywords)


def match_skills(cv_text, job_text):
    job_skills = extract_keywords(job_text)
    cv_skills = extract_keywords(cv_text)

    matched = list(cv_skills & job_skills)
    missing = list(job_skills - cv_skills)

    total = len(job_skills)

    if total == 0:
        skills_score = 0.0
    else:
        skills_score = len(matched) / total

    return {"skills_score": skills_score, "matched_skills": matched, "missing_skills": missing}
