import streamlit as st
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ollama


st.set_page_config(
    page_title="AI StudyMate RAG",
    page_icon="📚",
    layout="wide"
)


st.title("📚 AI StudyMate — Intermediate RAG")
st.write(
    "Upload a PDF and ask questions. The application searches "
    "relevant information from your document before answering."
)


def extract_pdf_text(uploaded_file):
    """Extract text from all pages of a PDF."""
    reader = PdfReader(uploaded_file)

    all_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            all_text.append(page_text)

    return "\n".join(all_text)


def split_text(text, chunk_size=800, overlap=100):
    """Split long text into smaller overlapping chunks."""
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def retrieve_relevant_chunks(question, chunks, top_k=3):
    """Find the most relevant chunks using TF-IDF similarity."""
    if not chunks:
        return []

    documents = chunks + [question]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    chunk_vectors = vectors[:-1]
    question_vector = vectors[-1]

    similarities = cosine_similarity(
        question_vector,
        chunk_vectors
    ).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    relevant_chunks = [
        chunks[index]
        for index in top_indices
        if similarities[index] > 0
    ]

    return relevant_chunks


def ask_ollama(question, context):
    """Generate an answer using the local Ollama model."""
    prompt = f"""
You are an AI study assistant.

Answer the user's question using only the provided document context.

If the answer is not available in the context, say:
"I could not find this information in the uploaded document."

Explain the answer clearly and simply.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


if uploaded_file is not None:
    with st.spinner("Reading your PDF..."):
        pdf_text = extract_pdf_text(uploaded_file)

    if not pdf_text.strip():
        st.error(
            "No readable text was found in this PDF. "
            "Try uploading a text-based PDF."
        )
        st.stop()

    chunks = split_text(pdf_text)

    st.success(
        f"PDF processed successfully. Created {len(chunks)} text chunks."
    )

    with st.expander("Preview extracted text"):
        st.write(pdf_text[:3000])

    st.divider()

    st.subheader("Ask a question about your PDF")

    question = st.text_input(
        "Enter your question",
        placeholder="Example: What are the main topics discussed in this document?"
    )

    top_k = st.slider(
        "Number of relevant sections to retrieve",
        min_value=1,
        max_value=5,
        value=3
    )

    if st.button("🔍 Search and Answer"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Searching the document..."):
                relevant_chunks = retrieve_relevant_chunks(
                    question,
                    chunks,
                    top_k
                )

            if not relevant_chunks:
                st.warning(
                    "No relevant information was found in the document."
                )
            else:
                context = "\n\n---\n\n".join(relevant_chunks)

                with st.expander("Retrieved document sections"):
                    for number, chunk in enumerate(
                        relevant_chunks,
                        start=1
                    ):
                        st.markdown(
                            f"**Section {number}**\n\n{chunk}"
                        )

                with st.spinner("Generating answer with Ollama..."):
                    try:
                        answer = ask_ollama(
                            question,
                            context
                        )

                        st.subheader("🤖 AI Answer")
                        st.write(answer)

                    except Exception as error:
                        st.error(
                            "Ollama could not generate an answer. "
                            "Make sure Ollama is running and the model "
                            "llama3.2:1b is installed."
                        )

                        st.code(str(error))

else:
    st.info(
        "Please upload a PDF file to begin."
    )

st.divider()

st.caption(
    "Built with Python, Streamlit, PyPDF, TF-IDF, and Ollama."
)