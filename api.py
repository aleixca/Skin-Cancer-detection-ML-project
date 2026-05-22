"""
FastAPI inference server for DermaScan ML.

Render must see an open port quickly. Keep app startup lightweight and load
the ML model/RAG index lazily when the corresponding endpoint is called.
"""

import os
import threading
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.knowledge_base import DOCUMENTS

BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

model_state = {}
rag_state = {}
model_lock = threading.Lock()
rag_lock = threading.Lock()

app = FastAPI(title="DermaScan ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_model():
    """Load the random forest bundle once, only when /predict needs it."""
    if model_state:
        return model_state

    with model_lock:
        if not model_state:
            import joblib

            bundle = joblib.load(MODEL_PATH)
            model_state.update(
                {
                    "rf": bundle["model"],
                    "columns": bundle["columns"],
                    "age_median": bundle["age_median"],
                    "threshold": bundle["threshold"],
                }
            )
    return model_state


def get_rag_index():
    """Build a small local retrieval index without transformer/torch overhead."""
    if rag_state:
        return rag_state

    with rag_lock:
        if not rag_state:
            from sklearn.feature_extraction.text import TfidfVectorizer

            texts = [
                f"{doc['title']}. {doc['content']} {' '.join(doc.get('tags', []))}"
                for doc in DOCUMENTS
            ]
            vectorizer = TfidfVectorizer(
                stop_words="english",
                ngram_range=(1, 2),
                max_features=5000,
                sublinear_tf=True,
                norm="l2",
            )
            matrix = vectorizer.fit_transform(texts)
            rag_state.update(
                {"vectorizer": vectorizer, "matrix": matrix, "docs": DOCUMENTS}
            )
    return rag_state


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "DermaScan ML API",
        "model_loaded": bool(model_state),
        "rag_loaded": bool(rag_state),
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    age: float = Form(default=45),
    sex: str = Form(default="male"),
    localization: str = Form(default="back"),
):
    state = get_model()
    import cv2
    import numpy as np
    from skimage.feature import hog as skimage_hog

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Could not decode image"}

    img = cv2.resize(img, (128, 128))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    feat = skimage_hog(
        img_rgb,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=False,
        channel_axis=-1,
    )

    clean_age = float(age) if age else state["age_median"]
    meta_values = []
    for column in state["columns"]:
        if column == "age":
            meta_values.append(clean_age)
        elif column.startswith("sex_"):
            meta_values.append(1 if column.removeprefix("sex_") == sex else 0)
        elif column.startswith("localization_"):
            expected = column.removeprefix("localization_")
            meta_values.append(1 if expected == localization else 0)
        else:
            meta_values.append(0)

    X = np.concatenate([feat.reshape(1, -1), np.array([meta_values])], axis=1)
    prob_cancer = float(state["rf"].predict_proba(X)[0][0])
    prediction = "cancerous" if prob_cancer >= state["threshold"] else "non_cancerous"

    return {
        "prediction": prediction,
        "probability": round(prob_cancer, 4),
        "threshold": state["threshold"],
        "label": "Potentially Cancerous"
        if prediction == "cancerous"
        else "Non-Cancerous",
    }


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    query = req.message.strip()
    if not query:
        return {
            "reply": "Please ask a question about skin lesions, scanning tips, or your results.",
            "sources": [],
        }

    index = get_rag_index()
    q_vec = index["vectorizer"].transform([query])
    scores = (index["matrix"] @ q_vec.T).toarray().ravel()
    top_idx = [
        i
        for i, _ in sorted(
            enumerate(scores), key=lambda item: item[1], reverse=True
        )[:3]
    ]
    top_docs = [(index["docs"][i], float(scores[i])) for i in top_idx]

    best_doc, best_score = top_docs[0]
    if best_score < 0.08:
        return {
            "reply": (
                "I'm not sure I have specific information about that. "
                "I can help with photo tips, understanding your results, "
                "the ABCD rule, or when to see a doctor. What would you like to know?"
            ),
            "sources": [],
        }

    reply_parts = [best_doc["content"]]
    if len(top_docs) > 1:
        second_doc, second_score = top_docs[1]
        if second_score > 0.12 and second_doc["id"] != best_doc["id"]:
            reply_parts.append("\n\n" + second_doc["content"])

    return {
        "reply": "".join(reply_parts),
        "sources": [
            {"title": doc["title"], "score": round(score, 3)}
            for doc, score in top_docs[:2]
            if score > 0
        ],
    }
