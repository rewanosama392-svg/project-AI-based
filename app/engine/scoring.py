def compute_final_score(lexical, semantic, skills, experience):
    weights = {"lexical": 0.15, "semantic": 0.45, "skills": 0.30, "experience": 0.10}

    score = (
        lexical * weights["lexical"]
        + semantic * weights["semantic"]
        + skills * weights["skills"]
        + experience * weights["experience"]
    )

    return round(score * 100, 2)


def get_recommendation(score):
    if score >= 75:
        return "Strong Match"
    elif score >= 60:
        return "Good Match"
    elif score >= 45:
        return "Moderate Match"
    elif score >= 30:
        return "Weak Match"
    else:
        return "Poor Match"
