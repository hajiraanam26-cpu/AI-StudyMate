import streamlit as st
import ollama
from pypdf import PdfReader
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="AI StudyMate - RAG",
    page_icon="📚"
)

st.title("📚 AI StudyMate")
st.write("Intermediate Document Q&A using RAG")


# -----------------------------
# Functions
# -----------------------------

def extract_text(uploaded_file):
    """Extract text from PDF or TXT files."""

    if uploaded_file.name.lower().endswith(".pdf"):
        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    elif uploaded_file.name.lower().endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    return ""


def create_chunks(text, chunk_size=800, overlap=100):
    """Split document text into smaller chunks."""

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def create_embeddings(chunks):
    """Create embeddings using Ollama."""

    embeddings = []

    for chunk in chunks:
        response = ollama.embed(
            model="nomic-embed-text",
            input=chunk
        )

        embeddings.append(response["embeddings"][0])

    return embeddings


def retrieve_chunks(question, chunks, embeddings, top_k=3):
    """Retrieve the most relevant document chunks."""

    question_response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    question_embedding = question_response["embeddings"][0]

    similarities = cosine_similarity(
        [question_embedding],
        embeddings
    )[0]

    ranked_indexes = similarities.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indexes:
        results.append({
            "text": chunks[index],
            "score": float(similarities[index])
        })

    return results


def generate_answer(question, retrieved_chunks):
    """Generate an answer using retrieved document context."""

    context = "\n\n".join(
        [
            f"Source {i + 1}:\n{item['text']}"
            for i, item in enumerate(retrieved_chunks)
        ]
    )

    prompt = f"""
You are an AI study assistant.

Answer the user's question using ONLY the information
provided in the document context below.

If the answer is not available in the context,
say:

"I could not find the answer in the uploaded document."

Do not use outside knowledge.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

Give a clear and concise answer.
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


# -----------------------------
# File Upload
# -----------------------------

st.header("📄 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True
)


if uploaded_files:

    all_text = ""

    for uploaded_file in uploaded_files:

        try:
            text = extract_text(uploaded_file)

            if text.strip():
                all_text += f"\n\n--- {uploaded_file.name} ---\n\n"
                all_text += text

            else:
                st.warning(
                    f"Could not extract text from {uploaded_file.name}"
                )

        except Exception as e:
            st.error(
                f"Error reading {uploaded_file.name}: {e}"
            )

    if all_text.strip():

        # -----------------------------
        # Chunking
        # -----------------------------

        chunks = create_chunks(all_text)

        st.success(
            f"Documents loaded successfully. "
            f"Created {len(chunks)} text chunks."
        )

        # -----------------------------
        # Embeddings
        # -----------------------------

        with st.spinner("Creating document embeddings..."):

            try:
                embeddings = create_embeddings(chunks)

                st.success(
                    "Document embeddings created successfully."
                )

            except Exception as e:

                st.error(
                    f"Embedding error: {e}"
                )

                st.stop()

        # Store information in session
        st.session_state["chunks"] = chunks
        st.session_state["embeddings"] = embeddings


# -----------------------------
# Question Answering
# -----------------------------

st.header("💬 Ask Questions")

question = st.text_input(
    "Ask a question about your uploaded document:"
)


if st.button("🔎 Search and Answer"):

    if not uploaded_files:
        st.warning(
            "Please upload a PDF or TXT document first."
        )

    elif not question.strip():
        st.warning(
            "Please enter a question."
        )

    elif "chunks" not in st.session_state:
        st.warning(
            "Please wait until the document is processed."
        )

    else:

        with st.spinner("Finding relevant document sections..."):

            try:

                retrieved_chunks = retrieve_chunks(
                    question,
                    st.session_state["chunks"],
                    st.session_state["embeddings"],
                    top_k=3
                )

                # -----------------------------
                # Answer
                # -----------------------------

                answer = generate_answer(
                    question,
                    retrieved_chunks
                )

                st.subheader("🤖 Answer")

                st.write(answer)

                # -----------------------------
                # Retrieved Context
                # -----------------------------

                st.subheader("📖 Retrieved Source Context")

                for i, result in enumerate(
                    retrieved_chunks
                ):

                    with st.expander(
                        f"Source {i + 1} "
                        f"(similarity: {result['score']:.2f})"
                    ):

                        st.write(result["text"])

            except Exception as e:

                st.error(
                    f"❌ Error while answering: {e}"
                )


# -----------------------------
# Information
# -----------------------------

st.sidebar.header("ℹ️ About")

st.sidebar.write(
    """
AI StudyMate uses a Retrieval-Augmented Generation
(RAG) workflow.

1. Upload a document
2. Extract the text
3. Split the text into chunks
4. Create embeddings
5. Search for relevant chunks
6. Send retrieved context to the AI
7. Generate a grounded answer
"""
)

st.sidebar.write(
    "Embedding model: nomic-embed-text"
)

st.sidebar.write(
    "AI model: llama3.2:1b"
)