def load_pdf(file_path):
    import fitz  # PyMuPDF
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text