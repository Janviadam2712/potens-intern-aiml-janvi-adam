import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="documents")

all_data = collection.get(limit=2000)
unique_sources = set(m["source_file"] for m in all_data["metadatas"])

print("Source files actually stored in Chroma:")
for s in sorted(unique_sources):
    print(" -", s)