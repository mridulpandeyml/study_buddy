import streamlit as st
import pandas as pd
import plotly.express as px
from src.processing.personalization import load_profile, get_weaknesses

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Learning Dashboard")

profile = load_profile()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Profile Info")
    st.write(f"**Name:** {profile.get('name', 'Student')}")
    st.write(f"**Preferred Mode:** {profile.get('mode', 'Standard')}")
    
    topics = profile.get("topics_studied", [])
    st.write("**Topics Discovered/Studied:**")
    if topics:
         st.write(", ".join(topics))
    else:
         st.write("None yet.")

with col2:
    st.subheader("Weak Areas")
    weaknesses = get_weaknesses()
    if weaknesses:
        st.warning(f"Needs Review: {', '.join(weaknesses)}")
    else:
        st.success("No weak areas detected yet! Keep taking quizzes.")

st.markdown("---")
st.subheader("Quiz Performance")

scores = profile.get("quiz_scores", [])
if not scores:
    st.info("Take some quizzes to see your performance charts!")
else:
    df = pd.DataFrame(scores)
    # Give quizzes an index ID for x-axis if we want trend over time
    df['Quiz_ID'] = df.index + 1
    
    # Line chart of scores over time
    fig_line = px.line(df, x='Quiz_ID', y='percentage', title="Score Trend Over Time", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Bar chart of average score per topic
    avg_scores = df.groupby('topic')['percentage'].mean().reset_index()
    fig_bar = px.bar(avg_scores, x='topic', y='percentage', title="Average Score by Topic", color='percentage')
    st.plotly_chart(fig_bar, use_container_width=True)
