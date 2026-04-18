import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1️⃣ تحديد مسار الملفات المدموجة
resumes_file = "../results/all_resumes.txt"
jobs_file = "../results/all_jobs.txt"

# 2️⃣ قراءة الملفات
with open(resumes_file, "r", encoding="utf-8") as f:
    resumes_text = f.read().split("\n\n")  # افترضنا كل سيرة فصلناها بسطرين فاضيين

with open(jobs_file, "r", encoding="utf-8") as f:
    jobs_text = f.read().split("\n\n")  # افترضنا كل وظيفة فصلناها بسطرين فاضيين

# 3️⃣ تحويل النصوص لتمثيل رقمي باستخدام TF-IDF
vectorizer = TfidfVectorizer(stop_words="english")  # إزالة الكلمات الشائعة
resumes_vectors = vectorizer.fit_transform(resumes_text)
jobs_vectors = vectorizer.transform(jobs_text)

# 4️⃣ حساب التشابه بين كل وظيفة وكل سيرة ذاتية
similarity_matrix = cosine_similarity(jobs_vectors, resumes_vectors)

# 5️⃣ تجهيز النتائج في جدول
results = []
for i, job in enumerate(jobs_text):
    # ترتيب السير الذاتية حسب التشابه الأعلى
    similarity_scores = similarity_matrix[i]
    top_indices = similarity_scores.argsort()[::-1]  # من الأعلى للأقل
    for rank, idx in enumerate(top_indices[:5], start=1):  # أفضل 5 مرشحين
        results.append(
            {
                "Job Index": i + 1,
                "Resume Index": idx + 1,
                "Similarity Score": round(similarity_scores[idx], 3),
            }
        )

df = pd.DataFrame(results)

# 6️⃣ حفظ النتائج
df.to_csv("../results/match_results.csv", index=False)
print("✅ تم حفظ نتائج المطابقة في 'match_results.csv' داخل مجلد results")
