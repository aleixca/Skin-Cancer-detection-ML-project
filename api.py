"""
api.py — FastAPI inference server with RAG chatbot.
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning)   # suppress sklearn version mismatch

import os
import json
import cv2
import numpy as np
import pandas as pd
import joblib
from skimage.feature import hog as skimage_hog
from sentence_transformers import SentenceTransformer

from fastapi import FastAPI, File, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(__file__)
MODEL_PATH  = os.path.join(BASE_DIR, "model.pkl")
EMBED_FILE  = os.path.join(BASE_DIR, "rag", "embeddings.npy")
DOCS_FILE   = os.path.join(BASE_DIR, "rag", "docs.json")

# ── Load ML model ─────────────────────────────────────────────────────────────
print("Loading ML model...")
bundle     = joblib.load(MODEL_PATH)
rf         = bundle["model"]
columns    = bundle["columns"]
age_median = bundle["age_median"]
threshold  = bundle["threshold"]

# ── Load RAG index ────────────────────────────────────────────────────────────
print("Loading RAG index...")
embeddings  = np.load(EMBED_FILE)                          # (N, 384)
with open(DOCS_FILE, encoding="utf-8") as f:
    docs = json.load(f)

print("Loading sentence-transformer...")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="DermaScan ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "ok", "model": "HAM10000 Random Forest", "threshold": threshold}


# ── Predict ───────────────────────────────────────────────────────────────────
@app.post("/predict")
async def predict(
    file:         UploadFile = File(...),
    age:          float      = Form(default=45),
    sex:          str        = Form(default="male"),
    localization: str        = Form(default="back"),
):
    contents = await file.read()
    nparr    = np.frombuffer(contents, np.uint8)
    img      = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Could not decode image"}

    img     = cv2.resize(img, (128, 128))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    feat = skimage_hog(
        img_rgb,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=False,
        channel_axis=-1,
    )

    meta_df  = pd.DataFrame([{
        "age":          float(age) if age else age_median,
        "sex":          sex,
        "localization": localization,
    }])
    meta_enc = pd.get_dummies(meta_df, columns=["sex", "localization"])
    meta_enc = meta_enc.reindex(columns=columns, fill_value=0)

    X           = np.concatenate([feat.reshape(1, -1), meta_enc.values], axis=1)
    prob_cancer = float(rf.predict_proba(X)[0][0])
    prediction  = "cancerous" if prob_cancer >= threshold else "non_cancerous"

    return {
        "prediction":  prediction,
        "probability": round(prob_cancer, 4),
        "threshold":   threshold,
        "label":       "Potentially Cancerous" if prediction == "cancerous" else "Non-Cancerous",
    }


# ── Chat (RAG) ────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    query = req.message.strip()
    if not query:
        return {"reply": "Please ask a question about skin lesions, scanning tips, or your results."}

    # 1. Embed query
    q_emb = embed_model.encode(query, normalize_embeddings=True)  # (384,)

    # 2. Cosine similarity (embeddings are already L2-normalised → dot product = cosine sim)
    scores = embeddings @ q_emb  # (N,)

    # 3. Top 3 chunks
    top_idx   = np.argsort(scores)[::-1][:3]
    top_docs  = [(docs[i], float(scores[i])) for i in top_idx]

    # 4. Build reply from retrieved chunks
    best_doc, best_score = top_docs[0]

    # If confidence is very low, give a fallback
    if best_score < 0.25:
        return {
            "reply": (
                "I'm not sure I have specific information about that. "
                "I can help with photo tips, understanding your results, "
                "the ABCD rule, or when to see a doctor. What would you like to know?"
            ),
            "sources": [],
        }

    # Compose response using top 1–2 retrieved chunks
    reply_parts = [best_doc["content"]]

    # Add second chunk if highly relevant and from a different topic
    if len(top_docs) > 1:
        second_doc, second_score = top_docs[1]
        if second_score > 0.40 and second_doc["id"] != best_doc["id"]:
            reply_parts.append("\n\n" + second_doc["content"])

    reply = "".join(reply_parts)

    return {
        "reply":   reply,
        "sources": [{"title": d["title"], "score": round(s, 3)} for d, s in top_docs[:2]],
    }
