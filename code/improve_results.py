import pandas as pd

# ======= الملفات =======
jobs_file = "../results/all_jobs.txt"
resumes_file = "../results/all_resumes.txt"
matches_file = "../results/top_matches.csv"

# ======= قراءة البيانات =======
with open(jobs_file, "r", encoding="utf-8") as f:
    jobs = [line.strip() for line in f if line.strip()]

with open(resumes_file, "r", encoding="utf-8") as f:
    resumes = [line.strip() for line in f if line.strip()]

matches = pd.read_csv(matches_file)

# ======= تحسين النتائج =======
results = []

for _, row in matches.iterrows():
    job_idx = int(row["Job Index"])
    resume_idx = int(row["Resume Index"])
    score = row["Similarity"]

    job_text = jobs[job_idx]
    resume_text = resumes[resume_idx]

    # ❌ شيل التطابق الكامل (نفس النص)
    if score >= 0.99:
        continue

    # ❌ شيل النتائج الضعيفة
    if score < 0.4:
        continue

    # ❌ شيل الداتا الفارغة أو غير المفيدة
    if "job title description" in job_text.lower():
        continue

    # ❌ شيل النصوص القصيرة (غالبًا مش Job حقيقية)
    if len(job_text) < 50:
        continue

    # إضافة النتيجة
    results.append(
        {"Job": job_text[:200], "Best Candidate": resume_text[:200], "Match Score": round(score, 2)}
    )

# ======= تحويل لـ DataFrame =======
df = pd.DataFrame(results)

# ⭐ أفضل 3 لكل وظيفة
df = df.groupby("Job").head(3)

# ======= حفظ النتيجة =======
df.to_csv("../results/final_clean_results.csv", index=False)

print("🔥 تم إنشاء نسخة نظيفة واحترافية 100%!")
