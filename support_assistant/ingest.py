import chromadb

from sentence_transformers import SentenceTransformer

from pathlib import Path

embedder = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="zepto_collection"
)

docs_folder = Path("docs")

for file in docs_folder.glob("*.txt"):

    text = file.read_text(
        encoding="utf-8"
    )

    embedding = embedder.encode(
        text
    ).tolist()

    collection.add(
        ids=[file.stem],
        documents=[text],
        embeddings=[embedding]
    )

print("Documents embedded successfully.")