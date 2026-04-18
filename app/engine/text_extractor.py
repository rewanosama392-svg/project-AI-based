import pdfplumber


def extract_text_from_pdf(path: str) -> str:
    text = ""

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    except:
        return ""

    return text.strip()
