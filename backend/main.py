from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from pathlib import Path
import ollama
import faiss
import numpy as np

from backend.documents import extract_text, split_into_chunks
from backend.workflow import answer_with_workflow


app = FastAPI(
    title="AI StudyMate Advanced API",
    description="Document-based question answering using RAG and FAISS",
    version="1.0.0"
)

# In-memory document storage for this first version
document_stores = {}


class HealthResponse(BaseModel):
    status: str


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    document_id: str = Field(..., min_length=1)


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]


@app.get("/", response_model=HealthResponse)
def home():
    return {"status": "AI StudyMate Advanced API is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {"status": "healthy"}


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = file.filename or "document.txt"
    extension = Path(filename).suffix.lower()

    if extension not in {".pdf", ".txt", ".md"}:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, TXT, and MD files are supported."
        )

    try:
        file_bytes = await file.read()
        text = extract_text(filename, file_bytes)
        chunks = split_into_chunks(text)

        if not chunks:
            raise ValueError("No usable text chunks were created.")

        vectors = []

        for chunk in chunks:
            response = ollama.embed(
                model="nomic-embed-text",
                input=chunk
            )
            vectors.append(response["embeddings"][0])

        embeddings = np.array(vectors, dtype="float32")
        faiss.normalize_L2(embeddings)

        index = faiss.IndexFlatIP(embeddings.shape[1])
        index.add(embeddings)

        document_id = str(len(document_stores) + 1)

        document_stores[document_id] = {
            "filename": filename,
            "chunks": chunks,
            "embeddings": embeddings,
            "index": index
        }

        return {
            "message": "Document processed successfully.",
            "document_id": document_id,
            "filename": filename,
            "chunks_created": len(chunks)
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed. Check Ollama is running and the required models are installed. Details: {error}"
        )


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid question."
        )

    store = document_stores.get(request.document_id)

    if store is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found. Upload the document first."
        )

    try:
        result = answer_with_workflow(question, store)

        return {
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed. Check Ollama is running. Details: {error}"
        )