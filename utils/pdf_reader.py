# utils/pdf_reader.py

import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts and returns clean text from a PDF file.
    """
    try:
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text() for page in doc])
        return text.strip()
    except Exception as e:
        raise RuntimeError(f"Failed to extract text: {e}")
