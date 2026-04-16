import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ملفات الإدخال
jobs_file = "../results/all_jobs.txt"
resumes_file = "../results/all_resumes.txt"

# قراءة كل سطر كسلسلة نصية واحدة
with open(jobs_file, "r", encoding="utf-8") as f:
    jobs_list = [line.strip() for line in f if line.strip()]

with open(resumes_file, "r", encoding="utf-8") as f:
    resumes_list = [line.strip() for line in f if line.strip()]

# تحويلها إلى DataFrame
jobs = pd.DataFrame(jobs_list, columns=["Job Description"])
resumes = pd.DataFrame(resumes_list, columns=["Resume Text"])

print(f"Jobs shape: {jobs.shape}")
print(f"Resumes shape: {resumes.shape}")

# TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
all_texts = pd.concat([jobs["Job Description"], resumes["Resume Text"]])
vectorizer.fit(all_texts)

jobs_tfidf = vectorizer.transform(jobs["Job Description"])
resumes_tfidf = vectorizer.transform(resumes["Resume Text"])

# Cosine similarity
similarity_matrix = cosine_similarity(jobs_tfidf, resumes_tfidf)

# أفضل 5 سير لكل وظيفة
top_n = 5
results = []

for job_idx, job_row in jobs.iterrows():
    sim_scores = similarity_matrix[job_idx]
    top_resume_indices = sim_scores.argsort()[::-1][:top_n]

    for rank, resume_idx in enumerate(top_resume_indices, 1):
        results.append(
            {"Job Index": job_idx, "Resume Index": resume_idx, "Similarity": sim_scores[resume_idx]}
        )

results_df = pd.DataFrame(results)
results_df.to_csv("../results/top_matches.csv", index=False)

print("✅ Top matches saved to '../results/top_matches.csv'")
