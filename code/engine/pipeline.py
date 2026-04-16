from engine.preprocessing import preprocess_text
from engine.scoring import compute_final_score
from engine.semantic import semantic_score
from engine.skills import match_skills


# -------------------------
# Experience Heuristic
# -------------------------
def compute_experience_score(cv_text: str):
    text = cv_text.lower()

    score = 50

    if "freelance" in text or "developer" in text:
        score += 10
    if "project" in text:
        score += 10
    if "in progress" in text or "expected" in text:
        score += 5

    return min(score, 100)


# -------------------------
# Recommendation
# -------------------------
def build_recommendation(final_score: float):
    if final_score >= 80:
        return "Excellent Match"
    elif final_score >= 65:
        return "Good Match"
    elif final_score >= 50:
        return "Moderate Match"
    else:
        return "Weak Match"


# -------------------------
# Strengths
# -------------------------
def build_strengths(skills_score, semantic):
    strengths = []

    if skills_score >= 80:
        strengths.append("Strong technical skill match")

    if semantic >= 70:
        strengths.append("High semantic alignment with job role")

    if not strengths:
        strengths.append("Basic match with job requirements")

    return strengths


# -------------------------
# Weaknesses
# -------------------------
def build_weaknesses(skills_score, missing_skills):
    weaknesses = []

    if len(missing_skills) > 0:
        weaknesses.append(f"Missing key skills: {', '.join(missing_skills)}")

    if skills_score < 70:
        weaknesses.append("Partial skill coverage")

    if not weaknesses:
        weaknesses.append("No major gaps")

    return weaknesses


# -------------------------
# MAIN PIPELINE
# -------------------------
def run_pipeline(cv_text: str, job_text: str):
    try:
        # ---------------- preprocessing
        try:
            cv_clean = preprocess_text(cv_text)
            job_clean = preprocess_text(job_text)
        except:
            cv_clean = cv_text
            job_clean = job_text

        # ---------------- semantic (ALWAYS FIRST SAFE)
        semantic = semantic_score(cv_clean, job_clean)
        semantic = max(0, min(semantic, 100))

        # ---------------- lexical (TF-IDF with safe fallback)
        try:
            from engine.scoring import tfidf_score

            lexical = tfidf_score(cv_clean, job_clean)
            lexical = max(0, min(lexical, 100))
        except:
            lexical = semantic  # fallback safe

        # ---------------- skills
        skills_data = match_skills(cv_clean, job_clean)

        # ---------------- experience
        experience_score = compute_experience_score(cv_clean)

        # ---------------- final score
        final_score = compute_final_score(
            lexical, semantic, skills_data["skills_score"], experience_score
        )

        # ---------------- output
        return {
            "lexical_score": round(lexical, 2),
            "semantic_score": round(semantic, 2),
            "skills_score": round(skills_data["skills_score"], 2),
            "experience_score": round(experience_score, 2),
            "final_score": round(final_score, 2),
            "matched_skills": skills_data["matched_skills"],
            "missing_skills": skills_data["missing_skills"],
            "level": "Mid",
            "strengths": build_strengths(skills_data["skills_score"], semantic),
            "weaknesses": build_weaknesses(
                skills_data["skills_score"], skills_data["missing_skills"]
            ),
            "recommendation": build_recommendation(final_score),
        }

    except Exception as e:
        return {
            "error": str(e),
            "lexical_score": 0,
            "semantic_score": 0,
            "skills_score": 0,
            "experience_score": 0,
            "final_score": 0,
            "recommendation": "Error",
        }
