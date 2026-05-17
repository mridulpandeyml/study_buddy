import streamlit as st
from src.processing.assessment import generate_quiz
from src.processing.personalization import record_quiz_score

st.set_page_config(page_title="Quiz Center", page_icon="📝", layout="wide")

st.title("📝 Quiz Center")
st.markdown("Test your knowledge based on the documents you've uploaded.")

if "extracted_text" not in st.session_state or not st.session_state.extracted_text.strip():
    st.warning("No document text available. Please go to the Upload Hub and process a document first.")
else:
    topic_name = st.text_input("Enter the topic of the quiz (e.g., 'Machine Learning', 'History'):", value="General")
    num_q = st.slider("Number of questions", min_value=1, max_value=10, value=3)
    
    if st.button("Generate Quiz"):
        with st.spinner("Generating quiz using AI..."):
            # Limit context size to avoid exceeding token limits
            context = st.session_state.extracted_text[:10000] 
            quiz_data = generate_quiz(context, num_questions=num_q)
            if quiz_data:
                st.session_state.current_quiz = quiz_data
                st.session_state.quiz_topic = topic_name
                st.session_state.quiz_submitted = False
            else:
                st.error("Failed to generate quiz. Please check API keys and try again.")

    if "current_quiz" in st.session_state and st.session_state.current_quiz:
        st.markdown("---")
        st.subheader("Quiz")
        
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(st.session_state.current_quiz):
                st.markdown(f"**Q{i+1}: {q['question']}**")
                # Handle cases where options might be duplicated or missing
                options = q.get("options", [])
                if not options:
                    st.warning("Invalid options for this question.")
                    continue
                user_answers[i] = st.radio("Select an answer:", options, key=f"q_{i}")
                
            submitted = st.form_submit_button("Submit Answers")
            
            if submitted and not st.session_state.get("quiz_submitted", False):
                score = 0
                st.markdown("### Results")
                for i, q in enumerate(st.session_state.current_quiz):
                    correct_answer = str(q.get("answer", "")).strip()
                    user_ans = str(user_answers.get(i, "")).strip()
                    
                    if user_ans == correct_answer:
                        score += 1
                        st.success(f"Q{i+1}: Correct!")
                    else:
                        st.error(f"Q{i+1}: Incorrect. You chose '{user_ans}'. The correct answer is '{correct_answer}'.")
                
                st.session_state.quiz_submitted = True
                total = len(st.session_state.current_quiz)
                st.info(f"You scored {score} out of {total} ({(score/total)*100:.1f}%)")
                
                record_quiz_score(st.session_state.quiz_topic, score, total)
                st.success("Score saved to your profile!")
