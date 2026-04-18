from engine.lexical import compute_lexical_score
from engine.preprocessing import preprocess_text
from engine.semantic import compute_semantic_score


def run_pipeline(cv_text: str, job_text: str):
    # 1) preprocessing
    cv_clean = preprocess_text(cv_text)
    job_clean = preprocess_text(job_text)

    # 2) scores
    lexical_score = compute_lexical_score(job_clean, cv_clean)
    semantic_score = compute_semantic_score(job_clean, cv_clean)

    # 3) skills extraction (مؤقتة دلوقتي لحد ما STEP 6)
    job_words = set(job_clean.split())
    cv_words = set(cv_clean.split())

    matched_skills = list(job_words & cv_words)
    missing_skills = list(job_words - cv_words)

    # 4) skills score (بسيط دلوقتي)
    if len(job_words) > 0:
        skills_score = len(matched_skills) / len(job_words)
    else:
        skills_score = 0

    # 5) final score (نفس الفورميولا بتاعتك)
    final_score = (
        0.35 * lexical_score
        + 0.35 * semantic_score
        + 0.20 * skills_score
        + 0.10 * 0  # experience لسه هيتضاف في STEP 7
    )

    # 6) recommendation بسيط
    if final_score >= 0.8:
        recommendation = "Excellent Match"
    elif final_score >= 0.65:
        recommendation = "Good Match"
    elif final_score >= 0.5:
        recommendation = "Moderate Match"
    else:
        recommendation = "Weak Match"

    # 7) strengths / weaknesses (مؤقتة)
    strengths = [f"Matched keywords: {', '.join(matched_skills[:5])}"]
    weaknesses = [f"Missing keywords: {', '.join(missing_skills[:5])}"]

    return {
        "lexical_score": round(lexical_score, 3),
        "semantic_score": round(semantic_score, 3),
        "skills_score": round(skills_score, 3),
        "experience_score": 0,
        "final_score": round(final_score, 3),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "level": "Unknown",
        "recommendation": recommendation,
    }
