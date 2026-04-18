import tempfile

from fastapi import FastAPI, File, Form, UploadFile

from app.engine.pipeline import run_pipeline
from app.engine.text_extractor import extract_text_from_pdf

app = FastAPI()


@app.post("/analyze")
def analyze(cv_text: str = Form(...), job_text: str = Form(...)):
    return run_pipeline(cv_text, job_text)


@app.post("/analyze-pdf")
async def analyze_pdf(cv: UploadFile = File(...), job_text: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await cv.read())
        pdf_path = tmp.name

    cv_text = extract_text_from_pdf(pdf_path)

    return run_pipeline(cv_text, job_text)
