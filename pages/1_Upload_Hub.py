import streamlit as st
import os
from src.input.document_router import doc_router
from src.processing.chunking import chunk_text
from src.processing.vector_store import VectorStore
from src.processing.knowledge_engine import extract_topics_and_keywords
from src.processing.personalization import add_topic_studied

st.set_page_config(page_title="Upload Hub", page_icon="📤", layout="wide")

st.title("📤 Upload Hub")
st.markdown("Upload your study materials (PDF, JPG, PNG) to extract knowledge and prepare for learning.")

if "vector_store" not in st.session_state or st.session_state.vector_store is None:
    st.session_state.vector_store = VectorStore()

uploaded_file = st.file_uploader("Upload a document or image", type=["pdf", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    if st.button("Process Document"):
        with st.spinner("Processing document..."):
            # 1. Save temp file
            file_extension = uploaded_file.name.split(".")[-1].lower()
            temp_file_path = f"temp_file.{file_extension}"
            raw_dir = "data/raw"
            os.makedirs(raw_dir, exist_ok=True)
            raw_file = os.path.join(raw_dir, temp_file_path)
            
            with open(raw_file, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                # 2. Extract and Clean Text
                st.info("Extracting text...")
                extracted_text = doc_router(raw_file)
                
                # 3. Knowledge Engine Extraction
                st.info("Analyzing knowledge and topics...")
                knowledge = extract_topics_and_keywords(extracted_text)
                topics = knowledge.get("topics", [])
                keywords = knowledge.get("keywords", [])
                
                for t in topics:
                    add_topic_studied(t)
                
                st.success(f"Discovered Topics: {', '.join(topics)}")
                
                # 4. Chunking
                st.info("Chunking text for vector search...")
                chunks = chunk_text(extracted_text, chunk_size=300, overlap=50)
                
                # 5. Embedding & Vector Store
                st.info(f"Generating embeddings for {len(chunks)} chunks and saving to FAISS...")
                st.session_state.vector_store.add_chunks(chunks)
                
                # Save extracted text to session for quiz generation
                if "extracted_text" not in st.session_state:
                    st.session_state.extracted_text = ""
                st.session_state.extracted_text += "\n\n" + extracted_text
                
                st.success("Document successfully processed and indexed! You can now Ask AI or take a Quiz.")
                
                with st.expander("View Extracted Text (Preview)"):
                    st.write(extracted_text[:1000] + "... (truncated)")
                    
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")
