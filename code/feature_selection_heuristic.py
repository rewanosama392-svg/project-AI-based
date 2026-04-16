import os

import pandas as pd

# ======= المسارات =======
jobs_file = "../results/all_jobs.txt"
resumes_file = "../results/all_resumes.txt"

processed_jobs_file = "../results/processed_jobs/selected_jobs_features.csv"
processed_resumes_file = "../results/processed_resumes/selected_resumes_features.csv"

# ======= تأكد وجود المجلدات =======
os.makedirs(os.path.dirname(processed_jobs_file), exist_ok=True)
os.makedirs(os.path.dirname(processed_resumes_file), exist_ok=True)

# ======= قراءة الملفات كسطر واحد لكل صف =======
with open(jobs_file, encoding="utf-8") as f:
    jobs_lines = f.readlines()
jobs = pd.DataFrame({"Job Description": [line.strip() for line in jobs_lines if line.strip()]})

with open(resumes_file, encoding="utf-8") as f:
    resumes_lines = f.readlines()
resumes = pd.DataFrame({"Resume Text": [line.strip() for line in resumes_lines if line.strip()]})

print("✅ الملفات اتقرت بنجاح")
print("Jobs shape:", jobs.shape)
print("Resumes shape:", resumes.shape)

# ======= حفظ الملفات =======
jobs.to_csv(processed_jobs_file, index=False)
resumes.to_csv(processed_resumes_file, index=False)

print("✅ الملفات جاهزة للـ final_matching.py")
