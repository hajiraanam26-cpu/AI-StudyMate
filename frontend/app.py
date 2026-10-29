import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI StudyMate",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI StudyMate")
st.subheader("Ask questions about your study documents")
st.write(
    "Upload a PDF, TXT, or Markdown file and get answers "
    "based on its content."
)

# Keep the uploaded document ID during the session.
if "document_id" not in st.session_state:
    st.session_state.document_id = None

if "document_name" not in st.session_state:
    st.session_state.document_name = None

# Check whether the backend is running.
try:
    health = requests.get(f"{API_URL}/health", timeout=5)

    if health.status_code == 200:
        st.success("Backend connected successfully.")
    else:
        st.warning("The backend responded, but its health check failed.")
except requests.RequestException:
    st.error(
        "Cannot connect to the backend. "
        "Start FastAPI in your terminal before using this page."
    )

st.divider()

st.header("1. Upload your document")

uploaded_file = st.file_uploader(
    "Choose a PDF, TXT, or Markdown file",
    type=["pdf", "txt", "md"]
)

if st.button("Upload and process document", type="primary"):
    if uploaded_file is None:
        st.warning("Please choose a document first.")
    else:
        try:
            file_data = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream"
                )
            }

            with st.spinner("Processing document..."):
                response = requests.post(
                    f"{API_URL}/upload",
                    files=file_data,
                    timeout=300
                )

            if response.status_code == 200:
                result = response.json()
                st.session_state.document_id = result["document_id"]
                st.session_state.document_name = result["filename"]

                st.success("Document uploaded successfully!")
                st.write(f"**File:** {result['filename']}")
                st.write(f"**Chunks created:** {result['chunks_created']}")
                st.write(f"**Document ID:** {result['document_id']}")
            else:
                try:
                    error_message = response.json().get(
                        "detail", response.text
                    )
                except ValueError:
                    error_message = response.text

                st.error(f"Upload failed: {error_message}")

        except requests.RequestException as error:
            st.error(f"Could not upload the document: {error}")

if st.session_state.document_id:
    st.info(
        f"Current document: {st.session_state.document_name}"
    )

st.divider()

st.header("2. Ask a question")

question = st.text_area(
    "Enter your question",
    placeholder="Example: What technologies are used in this project?"
)

if st.button("Get answer"):
    if not st.session_state.document_id:
        st.warning("Please upload a document first.")
    elif not question.strip():
        st.warning("Please enter a question.")
    else:
        request_data = {
            "question": question.strip(),
            "document_id": st.session_state.document_id
        }

        try:
            with st.spinner("Searching the document and generating an answer..."):
                response = requests.post(
                    f"{API_URL}/ask",
                    json=request_data,
                    timeout=300
                )

            if response.status_code == 200:
                result = response.json()

                st.subheader("Answer")
                st.write(result["answer"])

                st.subheader("Sources")
                sources = result.get("sources", [])
                if sources:
                    for index, source in enumerate(sources, start=1):
                        with st.expander(f"Source {index}", expanded=(index == 1)):
                            if isinstance(source, str):
                                if source.startswith("Relevance score:"):
                                    score_line, separator, source_text = source.partition("\n\n")
                                    st.caption(score_line)
                                    st.markdown(source_text if separator else source)
                                else:
                                    st.markdown(source)
                            else:
                                st.write(source)
                else:
                    st.info("No source text was returned.")
            else:
                try:
                    error_message = response.json().get(
                        "detail", response.text
                    )
                except ValueError:
                    error_message = response.text

                st.error(f"Question failed: {error_message}")

        except requests.RequestException as error:
            st.error(f"Could not contact the backend: {error}")

st.divider()
st.caption("AI StudyMate | FastAPI + Streamlit + FAISS + Ollama")