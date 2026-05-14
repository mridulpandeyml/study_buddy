def clean_text(text):
    import re
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text