import csv
import os
import json
from pathlib import Path

import numpy as np
import faiss
import openai

def load_chunks(csv_path):
    chunks = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chunks.append(row)
    return chunks

def embed_texts(texts, model="text-embedding-3-small"):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.embeddings.create(
        input=texts,
        model=model
    )
    embeddings = [item.embedding for item in response.data]
    return embeddings

def build_faiss_index(embeddings, dim):
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype='float32'))
    return index

def main():
    # Paths
    chunk_csv = "data/articles/chunks.csv"
    out_dir = Path("data/embeddings")
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load text chunks
    chunks = load_chunks(chunk_csv)
    texts = [chunk['text'] for chunk in chunks]

    # 2. Embed via OpenAI
    embeddings = embed_texts(texts)

    # 3. Build FAISS index
    dim = len(embeddings[0])
    index = build_faiss_index(embeddings, dim)

    # 4. Save FAISS index
    faiss.write_index(index, str(out_dir / "articles.index"))

    # 5. Save metadata alongside embeddings
    with open(out_dir / "metadata.jsonl", "w", encoding="utf-8") as f:
        for chunk in chunks:
            meta = {
                "url": chunk['url'],
                "title": chunk['title'],
                "publish_date": chunk['publish_date'],
                "chunk_id": chunk['chunk_id']
            }
            f.write(json.dumps(meta) + "\\n")

    print(f"FAISS index and metadata saved to {out_dir}")

if __name__ == "__main__":
    main()