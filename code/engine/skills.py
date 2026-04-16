import re

KNOWN_SKILLS = [
    "flutter",
    "dart",
    "firebase",
    "rest",
    "bloc",
    "clean architecture",
    "docker",
    "python",
    "sql",
]


def normalize(text):
    return text.lower()


def extract(text, skills_list):
    found = []
    text = normalize(text)

    for skill in skills_list:
        pattern = re.escape(skill.lower())

        if re.search(pattern, text):
            found.append(skill)

    return found


def match_skills(cv_text, job_text):
    cv_text = normalize(cv_text)
    job_text = normalize(job_text)

    cv_skills = extract(cv_text, KNOWN_SKILLS)
    job_skills = extract(job_text, KNOWN_SKILLS)

    matched = list(set(cv_skills) & set(job_skills))
    missing = list(set(job_skills) - set(cv_skills))

    if len(job_skills) == 0:
        skills_score = 0
    else:
        skills_score = (len(matched) / len(job_skills)) * 100

    return {
        "skills_score": round(skills_score, 2),
        "matched_skills": matched,
        "missing_skills": missing,
    }
