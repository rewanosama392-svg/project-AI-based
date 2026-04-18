import pandas as pd

# افتح ملف النتائج
df = pd.read_csv(r"C:\Users\20100\Downloads\project\results\match_results.csv")

# نختار Top 5 لكل Job حسب Similarity Score
top_matches = df.groupby("Job Index", group_keys=False).apply(
    lambda x: x.nlargest(5, "Similarity Score")
)

# نحفظ النتائج في CSV جديد
top_matches.to_csv(r"C:\Users\20100\Downloads\project\results\top_matches.csv", index=False)

print("✅ تم حفظ أفضل 5 مطابقات لكل وظيفة في 'top_matches.csv'")
