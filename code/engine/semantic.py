def semantic_score(resume_text: str, job_text: str) -> float:
    # simple fallback بدون تحميل model (عشان الإنترنت عندك مشاكل)
    resume_words = set(resume_text.split())
    job_words = set(job_text.split())

    if not job_words:
        return 0.0

    overlap = len(resume_words & job_words)
    return (overlap / len(job_words)) * 100
