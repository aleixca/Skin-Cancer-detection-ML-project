"""
Optional helper for exporting the DermaScan chatbot knowledge base.

The production API builds its lightweight TF-IDF retrieval index in memory, so
Render does not need a build-time embedding step or sentence-transformers.
"""

import json
import os

try:
    from rag.knowledge_base import DOCUMENTS
except ModuleNotFoundError:
    from knowledge_base import DOCUMENTS

INDEX_DIR = os.path.dirname(__file__)
DOCS_FILE = os.path.join(INDEX_DIR, "docs.json")


def build():
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(DOCUMENTS, f, ensure_ascii=False, indent=2)

    print(f"Saved docs -> {DOCS_FILE}")
    print("No embedding file is needed; api.py builds the TF-IDF index at runtime.")


if __name__ == "__main__":
    build()
