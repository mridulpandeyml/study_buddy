import streamlit as st

st.set_page_config(
    page_title="Study Buddy 📚",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Welcome to Study Buddy 📚")
st.markdown("""
### Your Adaptive AI Learning System

**How to use this app:**
1. **Upload Hub**: Upload your PDFs or images to extract text, process knowledge, and build your personalized learning database.
2. **Ask AI**: Ask questions about your uploaded documents. Choose your difficulty level (Beginner, Standard, Advanced) and get context-aware answers.
3. **Quiz Center**: Test your knowledge! The AI will dynamically generate multiple-choice quizzes based on your documents.
4. **Dashboard**: Track your progress, view your quiz scores, and see your weak areas.

👈 Select a page from the sidebar to get started!
""")

# Optional: Initialize session state variables if needed across pages
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None