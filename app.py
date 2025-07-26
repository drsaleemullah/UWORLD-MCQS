
import streamlit as st
import pandas as pd
import time

# Load MCQs
df = pd.read_csv("Streamlit_Ready_MCQs.csv")

# Streamlit page setup
st.set_page_config(page_title="MCQ Quiz App", layout="centered")
st.title("🧠 AI-Based MCQ Quiz App")
st.markdown("Test your knowledge. Get instant feedback. Learn smarter!")

# Subject Filter
subjects = df['Subject'].dropna().unique()
selected_subject = st.selectbox("📚 Select Subject", sorted(subjects))

# Filter based on subject
filtered_df = df[df['Subject'] == selected_subject].reset_index(drop=True)

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Timer settings
TIME_LIMIT = 30  # seconds

# Load current question
q = st.session_state.question_index
if q < len(filtered_df):
    row = filtered_df.iloc[q]

    st.markdown(f"### Q{q+1}: {row['Question']}")

    # Show image
    if pd.notna(row['Image URL']) and row['Image URL'].startswith("http"):
        st.image(row['Image URL'], width=400)

    # Timer
    elapsed = int(time.time() - st.session_state.start_time)
    time_left = TIME_LIMIT - elapsed
    if time_left > 0:
        st.info(f"⏳ Time left: {time_left} seconds")
    else:
        st.warning("⏰ Time's up! Moving to next question.")
        st.session_state.question_index += 1
        st.session_state.start_time = time.time()
        st.experimental_rerun()

    # Show options
    options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
    if pd.notna(row['Option E']) and row['Option E']:
        options.append(row['Option E'])

    selected = st.radio("Choose one:", options, key=f"radio_{q}")

    # Check answer
    if st.button("✅ Submit Answer"):
        correct = row[f"Option {row['Correct Answer']}"]
        if selected == correct:
            st.success("🎉 Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Incorrect! Correct answer: {row['Correct Answer']}")

        st.info(f"💡 Explanation: {row['Explanation']}")

        st.session_state.question_index += 1
        st.session_state.start_time = time.time()
        st.experimental_rerun()
else:
    st.success(f"🏁 Quiz completed! Your final score is {st.session_state.score}/{len(filtered_df)}")
    if st.button("🔄 Restart"):
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.experimental_rerun()
