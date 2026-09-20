import streamlit as st
import ollama

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="🎓"
)

st.title("🎓 AI StudyMate")
st.write("Your free AI-powered student study assistant")

notes = st.text_area(
    "Enter your study notes",
    height=200,
    placeholder="Paste your notes here..."
)

col1, col2 = st.columns(2)

with col1:
    summary_button = st.button("📚 Generate Summary")

with col2:
    quiz_button = st.button("❓ Generate Quiz")


# ---------------- SUMMARY ----------------

if summary_button:

    if not notes.strip():
        st.warning("⚠️ Please enter your study notes first.")

    else:
        try:
            with st.spinner("AI is generating your summary..."):

                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
You are an AI study assistant.

Summarize these study notes for a beginner.

Requirements:
- Use simple language.
- Keep important concepts.
- Use bullet points.
- Only use information from the notes.

STUDY NOTES:
{notes}
"""
                        }
                    ]
                )

            st.subheader("📚 AI Summary")
            st.write(response["message"]["content"])

        except Exception as e:
            st.error(f"❌ AI error: {e}")


# ---------------- QUIZ ----------------

if quiz_button:

    if not notes.strip():
        st.warning("⚠️ Please enter your study notes first.")

    else:
        try:
            with st.spinner("AI is creating your quiz..."):

                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
Create a simple quiz from these study notes.

Requirements:
- Create 5 multiple-choice questions.
- Give 4 options for each question.
- Clearly show the correct answer.
- Use only information from the notes.
- Keep the questions beginner-friendly.

STUDY NOTES:
{notes}
"""
                        }
                    ]
                )

            st.subheader("❓ AI Quiz")
            st.write(response["message"]["content"])

        except Exception as e:
            st.error(f"❌ AI error: {e}")


# ---------------- ASK AI ----------------

st.divider()

st.subheader("💬 Ask AI About Your Notes")

question = st.text_input(
    "Ask a question",
    placeholder="Example: What is the role of chlorophyll?"
)

if st.button("💡 Ask AI"):

    if not notes.strip():
        st.warning("⚠️ Please enter your study notes first.")

    elif not question.strip():
        st.warning("⚠️ Please enter a question.")

    else:
        try:
            with st.spinner("AI is thinking..."):

                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
You are an AI study assistant.

Answer the student's question using ONLY the study notes below.

Use simple language.

If the answer is not present in the notes, say:
"Sorry, this information is not available in the provided notes."

STUDY NOTES:
{notes}

STUDENT QUESTION:
{question}
"""
                        }
                    ]
                )

            st.subheader("🤖 AI Answer")
            st.write(response["message"]["content"])

        except Exception as e:
            st.error(f"❌ AI error: {e}")


# ---------------- FLASHCARDS ----------------

st.divider()

st.subheader("🧠 Generate Flashcards")

if st.button("🃏 Create Flashcards"):

    if not notes.strip():
        st.warning("⚠️ Please enter your study notes first.")

    else:
        try:
            with st.spinner("AI is creating flashcards..."):

                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[
                        {
                            "role": "user",
                            "content": f"""
Create 5 simple study flashcards from these notes.

Format each flashcard like this:

Question: ...
Answer: ...

Requirements:
- Create exactly 5 flashcards.
- Keep questions beginner-friendly.
- Keep answers short and clear.
- Use only information from the notes.

STUDY NOTES:
{notes}
"""
                        }
                    ]
                )

            st.subheader("🃏 AI Flashcards")
            st.write(response["message"]["content"])

        except Exception as e:
            st.error(f"❌ AI error: {e}")