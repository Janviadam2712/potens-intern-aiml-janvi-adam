import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from groq import Groq

load_dotenv()
app = FastAPI()

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Question(BaseModel):
    query: str
def translate_text(text, target_language_instruction):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"{target_language_instruction}\n\nText: {text}\n\nRespond with ONLY the translated text, nothing else."
        }]
    )
    return response.choices[0].message.content.strip()

@app.post("/ask")
def ask(q: Question):
    # Step A: detect language + translate to English
    detect_prompt = f"""Detect the language of this text, then translate it to English.

IMPORTANT: This text is a question about AI/ML/NLP research topics (e.g., "context engineering", "prompt engineering", "RAG", "retrieval"). Translate technical terms using their standard AI/ML English meaning, not a generic dictionary translation.

Text: {q.query}

Respond in this exact format:
LANGUAGE: <detected language name>
TRANSLATED: <English translation>
"""
    detect_response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": detect_prompt}]
    )
    detect_output = detect_response.choices[0].message.content

    detected_language = "English"
    english_query = q.query
    for line in detect_output.split("\n"):
        if line.startswith("LANGUAGE:"):
            detected_language = line.replace("LANGUAGE:", "").strip()
        if line.startswith("TRANSLATED:"):
            english_query = line.replace("TRANSLATED:", "").strip()
            print("DEBUG — English query used:", english_query)

    # Step B: run retrieval + answer generation in English (existing logic)
    results = collection.query(query_texts=[english_query], n_results=6)
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0] if "distances" in results and results["distances"] else []

    if not chunks:
        answer = "Not covered in the provided documents."
        confidence = "low"
        citations = []
    else:
        confidence = "high" if distances and distances[0] < 0.8 else "low"
        context_text = "\n\n".join(
            f"[{m['source_file']} p{m['page']}]: {c}" for c, m in zip(chunks, metadatas)
        )
        print("DEBUG — context_text:", context_text)
        prompt = f"""Answer the question using ONLY the information in the context below.

IMPORTANT: If the context contains information related to the topic of the question — even if it doesn't state a single perfect definition — synthesize an answer from what IS there. Only respond "Not covered in the provided documents." if the context is completely unrelated to the question's topic.

Context:
{context_text}

Question: {english_query}
"""
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response.choices[0].message.content
        citations = [
            {"source_file": m["source_file"], "page": m["page"], "snippet": c[:150]}
            for c, m in zip(chunks, metadatas)
        ]

    # Step C: translate answer back to original language (skip if already English)
    if detected_language.lower() != "english":
        answer = translate_text(answer, f"Translate this text to {detected_language}.")
    return {
        "detected_language": detected_language,
        "answer": answer,
        "citations": citations,
        "confidence": confidence
    }
class ContradictRequest(BaseModel):
    doc_id_1: str
    doc_id_2: str
    topic: str

@app.post("/contradict")
def contradict(req: ContradictRequest):
    results_1 = collection.get(where={"source_file": req.doc_id_1}, limit=10)
    results_2 = collection.get(where={"source_file": req.doc_id_2}, limit=10)

    text_1 = "\n".join(results_1["documents"]) if results_1["documents"] else ""
    text_2 = "\n".join(results_2["documents"]) if results_2["documents"] else ""

    if not text_1 or not text_2:
        return {"conflict": None, "reasoning": "One or both document IDs not found in the store."}

    prompt = f"""Compare these two passages on the topic: "{req.topic}"

Passage from {req.doc_id_1}:
{text_1[:2000]}

Passage from {req.doc_id_2}:
{text_2[:2000]}

Do these two passages agree or conflict on this topic? Answer with:
1. Conflict: Yes or No
2. Reasoning: explain clearly why, quoting or referencing specific claims from each passage
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "doc_1": req.doc_id_1,
        "doc_2": req.doc_id_2,
        "topic": req.topic,
        "analysis": response.choices[0].message.content
    }