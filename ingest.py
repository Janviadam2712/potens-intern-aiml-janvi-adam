import os
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

DOCS_FOLDER = "docs"

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

for filename in os.listdir(DOCS_FOLDER):
    if not filename.endswith(".pdf"):
        continue
    filepath = os.path.join(DOCS_FOLDER, filename)

    try:
        doc = fitz.open(filepath)
    except Exception as e:
        print(f"SKIPPED (broken file): {filename} — {e}")
        continue

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text or len(text.strip()) < 20:
            continue
        chunks = splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            chunk_id = f"{filename}_p{page_num}_c{i}"
            collection.add(
                documents=[chunk],
                ids=[chunk_id],
                metadatas=[{"source_file": filename, "page": page_num}]
            )
    print(f"Done: {filename}")

print("Total chunks stored:", collection.count())
