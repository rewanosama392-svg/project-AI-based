import csv
import os
from pathlib import Path

import docx
import PyPDF2

# === مسارات المجلدات ===
resumes_path = Path("../data/resumes")
jobs_path = Path("../data/job_descriptions")
results_path = Path("../results")

processed_resumes_path = results_path / "processed_resumes"
processed_jobs_path = results_path / "processed_jobs"

# إنشاء المجلدات لو مش موجودة
processed_resumes_path.mkdir(parents=True, exist_ok=True)
processed_jobs_path.mkdir(parents=True, exist_ok=True)


# === دوال قراءة الملفات ===
def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text


def read_csv(file_path):
    text = ""
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            text += " ".join(row) + "\n"
    return text


# === دالة حفظ النصوص ===
def save_text(text, output_path, file_name):
    out_file = output_path / f"{file_name}.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(text)


# === معالجة الملفات ===
def process_folder(input_path, output_path):
    count = 0
    for file in input_path.rglob("*"):  # يشمل كل الملفات داخل المجلدات الفرعية
        if file.suffix.lower() == ".txt":
            text = read_txt(file)
        elif file.suffix.lower() == ".docx":
            text = read_docx(file)
        elif file.suffix.lower() == ".pdf":
            text = read_pdf(file)
        elif file.suffix.lower() == ".csv":
            text = read_csv(file)
        else:
            print(f"⚠️ تم تجاهل الملف '{file.name}' (نوع غير مدعوم)")
            continue

        save_text(text, output_path, file.stem)
        print(f"✅ تم معالجة وحفظ '{file}'")
        count += 1
    return count


# === تنفيذ المعالجة ===
print("📄 معالجة ملفات Resumes:")
resumes_count = process_folder(resumes_path, processed_resumes_path)
print(f"\nعدد الملفات المعالجة في 'resumes': {resumes_count}\n")

print("💼 معالجة ملفات Job Descriptions:")
jobs_count = process_folder(jobs_path, processed_jobs_path)
print(f"\nعدد الملفات المعالجة في 'job_descriptions': {jobs_count}\n")

print("🎉 تم حفظ كل النصوص المعالجة في مجلد results.")
