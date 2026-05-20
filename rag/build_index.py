"""
build_index.py — Run once to embed the knowledge base and save the index.
Called automatically during Docker build.
"""

import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# Import knowledge base from sibling file
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from rag.knowledge_base import DOCUMENTS

INDEX_DIR   = os.path.dirname(__file__)
EMBED_FILE  = os.path.join(INDEX_DIR, "embeddings.npy")
DOCS_FILE   = os.path.join(INDEX_DIR, "docs.json")
MODEL_NAME  = "all-MiniLM-L6-v2"   # 90 MB, fast, great semantic search

def build():
    print(f"Loading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    texts = [f"{d['title']}. {d['content']}" for d in DOCUMENTS]

    print(f"Embedding {len(texts)} documents...")
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    np.save(EMBED_FILE, embeddings)
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(DOCUMENTS, f, ensure_ascii=False, indent=2)

    print(f"Saved embeddings → {EMBED_FILE}")
    print(f"Saved docs       → {DOCS_FILE}")
    print("RAG index ready.")

if __name__ == "__main__":
    build()
