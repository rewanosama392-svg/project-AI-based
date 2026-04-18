import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

# ==============================
# LOAD DATA
# ==============================
resumes_file = "../results/all_resumes.txt"

with open(resumes_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

resumes = pd.DataFrame(lines, columns=["Resume"])

resumes["Resume"] = (
    resumes["Resume"].astype(str).str.lower().str.replace("\n", " ", regex=False).str.strip()
)

resumes = resumes[resumes["Resume"] != ""]


# ==============================
# LABELING
# ==============================
def label_resume(text):
    if "senior" in text or "5+ years" in text or "6 years" in text:
        return "Senior"
    elif "junior" in text or "1 year" in text or "entry level" in text:
        return "Junior"
    else:
        return "Mid"


resumes["Level"] = resumes["Resume"].apply(label_resume)

# ==============================
# TRAINING
# ==============================
vectorizer = TfidfVectorizer(max_features=2000)
X = vectorizer.fit_transform(resumes["Resume"])
y = resumes["Level"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("\n✅ Model trained")

# ==============================
# SAVE MODEL
# ==============================
with open("../results/level_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("../results/level_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model saved")


# ==============================
# 🔥 NEW: LOAD FOR PREDICTION
# ==============================
def predict_level(text: str):
    """
    Predict candidate level from resume text
    """
    with open("../results/level_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("../results/level_vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]

    return prediction
