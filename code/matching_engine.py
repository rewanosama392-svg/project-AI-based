import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ==============================
# 1. تحميل البيانات
# ==============================
jobs_file = "../results/all_jobs.txt"
resumes_file = "../results/all_resumes.txt"

with open(jobs_file, "r", encoding="utf-8", errors="ignore") as f:
    jobs = [line.strip() for line in f.readlines() if line.strip()]

with open(resumes_file, "r", encoding="utf-8", errors="ignore") as f:
    resumes = [line.strip() for line in f.readlines() if line.strip()]

print("Jobs:", len(jobs))
print("Resumes:", len(resumes))

# ==============================
# 2. اختيار Job معين (للتجربة)
# ==============================
job_index = 0
job_text = jobs[job_index]

print("\n📌 Job Sample:")
print(job_text[:200])

# ==============================
# 3. TF-IDF Vectorization
# ==============================
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)

all_texts = [job_text] + resumes
tfidf_matrix = vectorizer.fit_transform(all_texts)

job_vector = tfidf_matrix[0]
resume_vectors = tfidf_matrix[1:]

# ==============================
# 4. حساب التشابه
# ==============================
similarities = cosine_similarity(job_vector, resume_vectors)[0]

# ==============================
# 5. ترتيب النتائج
# ==============================
results = pd.DataFrame({"Resume Index": range(len(resumes)), "Similarity Score": similarities})

results = results.sort_values(by="Similarity Score", ascending=False)

# ==============================
# 6. أفضل 10 مرشحين
# ==============================
top_k = 10
top_matches = results.head(top_k)

print("\n🏆 Top Matches:")
print(top_matches)

# ==============================
# 7. حفظ النتائج
# ==============================
top_matches.to_csv("../results/top_matches.csv", index=False)

print("\n✅ Saved: top_matches.csv")
