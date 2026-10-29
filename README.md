# 📚 AI StudyMate

AI StudyMate is a document-based Question and Answer application built using Python, Streamlit, FastAPI, Ollama, LangGraph, and FAISS. It uses Retrieval-Augmented Generation (RAG) to answer questions using information from uploaded study documents.

## ✨ Features

- Upload PDF, TXT, and Markdown documents.
- Extract text and divide it into smaller chunks.
- Generate embeddings for document chunks.
- Retrieve relevant information using FAISS similarity search.
- Generate answers using a local language model.
- Display answers and relevant source information.
- Provide a simple Streamlit user interface.
- Validate uploaded documents and empty questions.

## 🔄 How It Works

1. Upload a study document.
2. Extract text from the document.
3. Divide the extracted text into smaller chunks.
4. Generate embeddings using the `nomic-embed-text` model.
5. Retrieve relevant chunks using FAISS.
6. Send the retrieved context to the `llama3.2:1b` language model through Ollama.
7. Display the generated answer and source information.

## 🛠️ Technologies Used

- Python
- Streamlit
- FastAPI
- Ollama
- LangGraph
- FAISS
- Llama 3.2 1B
- Nomic Embed Text

## 📄 Supported Documents

- PDF (`.pdf`)
- Text (`.txt`)
- Markdown (`.md`)

## ⚙️ Requirements

- Python
- Ollama
- The required Ollama models
- Python packages listed in `requirements.txt`

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/hajiraanam26-cpu/AI-StudyMate.git
cd AI-StudyMate
```

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Install and start Ollama

Install Ollama from its official website:

https://ollama.com/

Download the required models:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

Ensure Ollama is running before using the application.

## ▶️ Running the Application

Open two terminals in the project folder and activate the virtual environment in both.

### Terminal 1: Start the FastAPI backend

```powershell
python -m uvicorn backend.main:app --reload
```

Backend address:

http://127.0.0.1:8000

Health check:

http://127.0.0.1:8000/health

### Terminal 2: Start the Streamlit frontend

```powershell
python -m streamlit run frontend/app.py --server.port 8505
```

Open the application in your browser:

http://localhost:8505

## 📁 Project Structure

```text
AI-StudyMate/
├── backend/
│   ├── main.py
│   ├── documents.py
│   ├── workflow.py
│   └── .gitignore
├── frontend/
│   └── app.py
├── app.py
├── beginner_app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## 🎯 Project Objective

The objective of AI StudyMate is to demonstrate how document processing, vector similarity search, and a language model can work together to answer questions based on uploaded study materials.

## 👩‍💻 Author

Hajira Anam

## 🔮 Future Improvements

- Improve retrieval accuracy and answer grounding.
- Support additional document formats.
- Add persistent document storage.
- Improve error handling and testing.
- Add Docker support.
- Improve the user interface.