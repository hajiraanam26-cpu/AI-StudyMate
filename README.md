# 📚 AI StudyMate

AI StudyMate is a document-based Question & Answer application built with Python, Streamlit, FastAPI, Ollama, and Retrieval-Augmented Generation (RAG).

It allows users to upload PDF or TXT documents, ask questions about their content, and receive answers based on relevant document sections.

## ✨ Features

- Upload PDF and TXT documents.
- Extract and split document text into smaller chunks.
- Generate embeddings for document sections.
- Retrieve relevant text for user questions.
- Generate answers using a local AI model.
- Display retrieved source context.
- Handle empty questions and invalid documents.
- Provide a simple user interface using Streamlit.

## 🔄 How It Works

1. Upload a PDF or TXT document.
2. Extract text from the document.
3. Divide the text into smaller chunks.
4. Generate embeddings for the chunks.
5. Retrieve relevant chunks for the user's question.
6. Send the retrieved context to the AI model.
7. Display the answer and source information.

## 🛠️ Technologies Used

- Python
- Streamlit
- FastAPI
- Ollama
- LangGraph
- FAISS
- Llama 3.2 1B
- Nomic Embed Text

## 🤖 AI Models

**Generation model:** `llama3.2:1b`

**Embedding model:** `nomic-embed-text`

## 📄 Supported Documents

- PDF
- TXT

## ⚙️ Requirements

- Python
- Ollama
- The AI models listed above
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

Open a terminal and download the required models:

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

Make sure Ollama is running before using the application.

## ▶️ Running the Application

Open two terminals in the project folder and activate the virtual environment in each terminal.

### Terminal 1: Start the FastAPI backend

```powershell
python -m uvicorn backend.main:app --reload
```

The backend should be available at:

`http://127.0.0.1:8000`

Health check:

`http://127.0.0.1:8000/health`

### Terminal 2: Start the Streamlit frontend

```powershell
python -m streamlit run frontend/app.py --server.port 8505
```

Open the application in your browser:

`http://localhost:8505`

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

The objective of AI StudyMate is to demonstrate how document retrieval and a language model can work together to answer questions using information from uploaded documents.

## 👩‍💻 Author

Hajira Anam

## 📌 Future Improvements

- Improve answer-grounding and retrieval accuracy.
- Add more document formats.
- Add document-specific retrieval and filtering.
- Improve error handling and user feedback.
- Add Docker support and automated tests.