import streamlit as st
from src.input.pdf_loader import load_pdf  
from src.input.document_router import doc_router
import pytesseract
from PIL import Image
import os
st.title("study buddy 📚")

uploaded_file = st.file_uploader(
    "Upload a PDF or Image file",
    type=["pdf", "jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    temp_file_path = f"temp_file.{file_extension}"
    raw_file= os.path.join("data/raw", temp_file_path)
    with open(raw_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        extracted_text = doc_router(raw_file)
        st.text_area("Extracted Text", extracted_text, height=300)
    except ValueError as e:
        st.error(str(e))