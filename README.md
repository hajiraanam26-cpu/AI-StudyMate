# 📚 AI StudyMate

AI StudyMate is an intermediate-level document-based Question & Answer application built using Python, Streamlit, Ollama, embeddings, and Retrieval-Augmented Generation (RAG).

## 🚀 Features

- Upload PDF and TXT documents
- Extract text from documents
- Split documents into smaller chunks
- Generate document embeddings
- Search for relevant document sections
- Generate answers using retrieved context
- Display retrieved source context
- Handle empty questions
- Handle invalid or unreadable documents
- Simple and beginner-friendly Streamlit interface

## 🔄 RAG Workflow

1. Upload a PDF or TXT document
2. Extract text from the document
3. Split the text into chunks
4. Generate embeddings for the chunks
5. Convert the user's question into an embedding
6. Find the most relevant chunks using cosine similarity
7. Send the retrieved context to the AI model
8. Generate a grounded answer
9. Display the retrieved source context

## 🛠️ Technologies Used

- Python
- Streamlit
- Ollama
- Llama 3.2 1B
- Nomic Embed Text
- PyPDF
- Scikit-learn
- NumPy

## 🤖 AI Models

### Generation Model
`llama3.2:1b`

### Embedding Model
`nomic-embed-text`

## 📄 Supported Files

- PDF
- TXT

## ▶️ How to Run

Install the required packages:

```bash
pip install -r requirements.txt
