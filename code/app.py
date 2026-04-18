import os
import shutil
import uuid

from engine.pipeline import run_pipeline
from engine.text_extractor import extract_text
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# Root test
# =========================
@app.get("/")
def home():
    return {"message": "CVision API is running 🚀"}


# =========================
# Analyze raw text
# =========================
@app.post("/analyze")
def analyze(data: dict):
    cv_text = data.get("cv_text", "")
    job_text = data.get("job_text", "")

    if not cv_text or not job_text:
        return {"error": "cv_text and job_text are required"}

    result = run_pipeline(cv_text, job_text)
    return result


# =========================
# Upload file (PDF / DOCX)
# =========================
@app.post("/analyze-upload")
async def analyze_upload(cv_file: UploadFile = File(...), job_text: str = ""):
    if not job_text:
        return {"error": "job_text is required"}

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, file_id + "_" + cv_file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(cv_file.file, buffer)

    try:
        cv_text = extract_text(file_path)
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}

    result = run_pipeline(cv_text, job_text)

    return {"filename": cv_file.filename, "result": result}
