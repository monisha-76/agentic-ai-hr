import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using pdfplumber
    """

    extracted_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + "\n"

    except Exception as e:
        raise RuntimeError(f"Failed to read PDF: {e}")

    return extracted_text.strip()
