from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_semantic_score(cv_text, job_text):
    cv_emb = model.encode([cv_text])
    job_emb = model.encode([job_text])

    score = cosine_similarity(cv_emb, job_emb)[0][0]

    return round(float(score), 3)
