import os

# مجلد النتائج
resumes_folder = r"C:\Users\20100\Downloads\project\results\processed_resumes"
jobs_folder = r"C:\Users\20100\Downloads\project\results\processed_jobs"


# دمج كل ملفات نصوص في ملف واحد
def merge_files(folder, output_file):
    with open(output_file, "w", encoding="utf-8") as outfile:
        for filename in os.listdir(folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder, filename)
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read() + "\n\n")  # فصل كل ملف بمسطرتين


merge_files(resumes_folder, r"C:\Users\20100\Downloads\project\results\all_resumes.txt")
merge_files(jobs_folder, r"C:\Users\20100\Downloads\project\results\all_jobs.txt")

print("✅ تم دمج كل الملفات في ملفات نصية واحدة لكل نوع")
