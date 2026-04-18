import random

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# 1. قراءة الملفات بشكل صحيح (سطر بسطر)
# -----------------------------
with open("../results/all_jobs.txt", "r", encoding="utf-8", errors="ignore") as f:
    jobs = pd.DataFrame(f.readlines(), columns=["Job"])

with open("../results/all_resumes.txt", "r", encoding="utf-8", errors="ignore") as f:
    resumes = pd.DataFrame(f.readlines(), columns=["Resume"])

print("Jobs shape:", jobs.shape)
print("Resumes shape:", resumes.shape)

# -----------------------------
# 2. تنظيف البيانات
# -----------------------------
jobs = jobs.dropna()
resumes = resumes.dropna()

jobs["Job"] = jobs["Job"].astype(str).str.strip()
resumes["Resume"] = resumes["Resume"].astype(str).str.strip()

# حذف الصفوف الفاضية
jobs = jobs[jobs["Job"] != ""]
resumes = resumes[resumes["Resume"] != ""]

# -----------------------------
# 3. TF-IDF
# -----------------------------
vectorizer = TfidfVectorizer(max_features=500)

all_text = pd.concat([jobs["Job"], resumes["Resume"]])
vectorizer.fit(all_text)

job_features = vectorizer.transform(jobs["Job"]).toarray()
resume_features = vectorizer.transform(resumes["Resume"]).toarray()

print("✅ TF-IDF جاهز")


# -----------------------------
# 4. Genetic Algorithm
# -----------------------------
def fitness(chromosome):
    idx = np.where(chromosome == 1)[0]

    if len(idx) == 0:
        return 0

    sims = cosine_similarity(job_features[:, idx], resume_features[:, idx])
    return np.mean(np.max(sims, axis=1))


def genetic_algorithm():
    num_features = job_features.shape[1]
    population_size = 10
    generations = 5

    population = [np.random.randint(2, size=num_features) for _ in range(population_size)]

    for gen in range(generations):
        scores = [fitness(ind) for ind in population]

        # اختيار الأفضل
        sorted_idx = np.argsort(scores)[::-1]
        population = [population[i] for i in sorted_idx[: population_size // 2]]

        # crossover
        children = []
        while len(children) < population_size - len(population):
            p1, p2 = random.sample(population, 2)
            point = random.randint(1, num_features - 1)
            child = np.concatenate([p1[:point], p2[point:]])
            children.append(child)

        population += children

        # mutation
        for ind in population:
            if random.random() < 0.1:
                idx = random.randint(0, num_features - 1)
                ind[idx] = 1 - ind[idx]

        print(f"Generation {gen + 1} done")

    # أفضل حل
    scores = [fitness(ind) for ind in population]
    best = population[np.argmax(scores)]

    return np.where(best == 1)[0]


# -----------------------------
# 5. تشغيل GA
# -----------------------------
best_features = genetic_algorithm()

print("عدد الميزات المختارة:", len(best_features))

# -----------------------------
# 6. حفظ النتائج
# -----------------------------
np.save("../results/ga_jobs_features.npy", job_features[:, best_features])
np.save("../results/ga_resumes_features.npy", resume_features[:, best_features])

print("✅ تم حفظ الميزات في results/")
