from typing import TypedDict

import faiss
import numpy as np
import ollama
from langgraph.graph import StateGraph, START, END


class StudyMateState(TypedDict):
    question: str
    store: dict
    retrieved: list
    context: str
    answer: str


def retrieve_documents(state: StudyMateState):
    """Find the most relevant document chunks for the question."""
    question = state["question"]
    store = state["store"]

    response = ollama.embed(
        model="nomic-embed-text",
        input=question
    )

    query_vector = np.array(
        [response["embeddings"][0]],
        dtype="float32"
    )

    faiss.normalize_L2(query_vector)

    scores, indexes = store["index"].search(
        query_vector,
        min(8, len(store["chunks"]))
    )

    retrieved = []

    for score, index in zip(scores[0], indexes[0]):
        if index >= 0:
            retrieved.append({
                "text": store["chunks"][int(index)],
                "score": float(score)
            })

    context = "\n\n".join(
        f"Source {i + 1}:\n{item['text']}"
        for i, item in enumerate(retrieved)
    )

    return {
        "retrieved": retrieved,
        "context": context
    }


def generate_answer(state: StudyMateState):
    """Generate an answer using the retrieved document context."""
    question = state["question"]
    context = state["context"]

    if not context.strip():
        return {
            "answer": "I could not find the answer in the uploaded document."
        }

    prompt = f"""
You are AI StudyMate, a document-based study assistant.

Answer the question using ONLY the information explicitly supported
by the DOCUMENT CONTEXT.

Rules:
1. Do not invent technologies, libraries, frameworks, or features.
2. Do not assume a technology is used just because it is common.
3. List a technology only if the context explicitly identifies it.
4. Explain each technology's purpose only when the context supports it.
5. Do not call file formats, programming concepts, or model names libraries.
6. Do not describe Nomic as a text-generation library.
7. If the context does not provide enough information, say:
"I could not find enough information in the uploaded document to answer this question."
8. Keep the answer concise and avoid repetition.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    result = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "answer": result["message"]["content"]
    }


def build_study_graph():
    """Create the document retrieval and answer generation workflow."""
    graph = StateGraph(StudyMateState)

    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_node("generate_answer", generate_answer)

    graph.add_edge(START, "retrieve_documents")
    graph.add_edge("retrieve_documents", "generate_answer")
    graph.add_edge("generate_answer", END)

    return graph.compile()


study_graph = build_study_graph()


def answer_with_workflow(question: str, store: dict):
    """Run the question through the LangGraph workflow."""
    result = study_graph.invoke({
        "question": question,
        "store": store,
        "retrieved": [],
        "context": "",
        "answer": ""
    })

    return {
        "answer": result["answer"],
        "sources": [
            f"Relevance score: {item['score']:.3f}\n\n{item['text']}"
            for item in result["retrieved"]
        ]
    }