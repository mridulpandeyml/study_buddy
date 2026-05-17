import streamlit as st
from src.processing.vector_store import VectorStore
from src.processing.llm_layer import generate_answer

st.set_page_config(page_title="Ask AI", page_icon="💬", layout="wide")

st.title("💬 Ask AI")
st.markdown("Ask questions about the materials you've uploaded.")

if "vector_store" not in st.session_state or st.session_state.vector_store is None:
    st.session_state.vector_store = VectorStore()

mode = st.radio("Select Difficulty Level:", ["Beginner", "Standard", "Advanced"], horizontal=True)

query = st.text_input("Enter your question here:")

if st.button("Ask") and query:
    with st.spinner("Searching for context and generating answer..."):
        # Retrieve context
        chunks = st.session_state.vector_store.search(query, top_k=3)
        
        if not chunks:
            st.warning("No context found. Please ensure you have uploaded and processed documents.")
        else:
            context = "\n\n".join(chunks)
            answer = generate_answer(query, context, mode=mode)
            
            st.markdown("### Answer")
            st.write(answer)
            
            with st.expander("View Retrieved Context"):
                for i, chunk in enumerate(chunks):
                    st.markdown(f"**Chunk {i+1}:**")
                    st.write(chunk)
