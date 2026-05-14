def doc_router(file_path):
    import os
    from .pdf_loader import load_pdf
    from .image_ext import extract_from_image
    from .cleaner import clean_text

    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.pdf':
        raw_text = load_pdf(file_path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        raw_text = extract_from_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
    
    cleaned_text = clean_text(raw_text)
    
    return cleaned_text