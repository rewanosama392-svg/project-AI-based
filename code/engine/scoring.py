def compute_final_score(lexical, semantic, skills_score, experience_score):
    """
    Hybrid scoring formula (stable version for CVision project)
    """

    # normalize safety
    lexical = min(max(lexical, 0), 100)
    semantic = min(max(semantic, 0), 100)
    skills_score = min(max(skills_score, 0), 100)
    experience_score = min(max(experience_score, 0), 100)

    final_score = 0.20 * lexical + 0.40 * semantic + 0.30 * skills_score + 0.10 * experience_score

    return round(final_score, 2)
