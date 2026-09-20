# AI StudyMate

AI StudyMate is an AI-powered document question-answering application built with Python and Streamlit.

It uses a Retrieval-Augmented Generation (RAG) workflow to answer questions based on uploaded PDF or TXT documents.

## Features

- Upload PDF and TXT documents
- Extract text from documents
- Split documents into smaller chunks
- Create document embeddings
- Find relevant document sections using similarity search
- Generate answers using a local AI model
- Display retrieved source context
- Basic validation for empty questions and invalid documents
- Simple Streamlit user interface

## RAG Workflow

1. Upload a PDF or TXT document
2. Extract the document text
3. Split the text into chunks
4. Create embeddings using `nomic-embed-text`
5. Convert the question into an embedding
6. Find the most relevant document chunks
7. Send the retrieved context to the AI model
8. Generate a grounded answer
9. Display the retrieved source context

## Technologies Used

- Python
- Streamlit
- Ollama
- PyPDF
- scikit-learn
- nomic-embed-text
- llama3.2:1b

## Project Files

- `app.py` — Main RAG application
- `beginner_app.py` — Backup of the beginner version
- `requirements.txt` — Python dependencies
- `README.md` — Project documentation

## How to Run

Install the required Python packages:

```bash
pip install -r requirements.txt
