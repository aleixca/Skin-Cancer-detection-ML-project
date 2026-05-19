"""
api.py — FastAPI inference server.
Replaces Streamlit as the backend; serves the ML model over HTTP.
"""

import os
import cv2
import numpy as np
import pandas as pd
import joblib
from skimage.feature import hog as skimage_hog

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

# ── Load model once at startup ────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
bundle     = joblib.load(MODEL_PATH)
rf         = bundle["model"]
columns    = bundle["columns"]
age_median = bundle["age_median"]
threshold  = bundle["threshold"]

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="DermaScan ML API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Vercel frontend + local dev
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "model": "HAM10000 Random Forest", "threshold": threshold}


@app.post("/predict")
async def predict(
    file:         UploadFile = File(...),
    age:          float      = Form(default=45),
    sex:          str        = Form(default="male"),
    localization: str        = Form(default="back"),
):
    # ── Decode image ──────────────────────────────────────────────────────────
    contents = await file.read()
    nparr    = np.frombuffer(contents, np.uint8)
    img      = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return {"error": "Could not decode image"}, 400

    img     = cv2.resize(img, (128, 128))
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ── HOG features ──────────────────────────────────────────────────────────
    feat = skimage_hog(
        img_rgb,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=False,
        channel_axis=-1,
    )

    # ── Metadata encoding ─────────────────────────────────────────────────────
    meta_df  = pd.DataFrame([{
        "age":          float(age) if age else age_median,
        "sex":          sex,
        "localization": localization,
    }])
    meta_enc = pd.get_dummies(meta_df, columns=["sex", "localization"])
    meta_enc = meta_enc.reindex(columns=columns, fill_value=0)

    # ── Inference ─────────────────────────────────────────────────────────────
    X            = np.concatenate([feat.reshape(1, -1), meta_enc.values], axis=1)
    prob_cancer  = float(rf.predict_proba(X)[0][0])   # classes_[0] == 'cancerous'
    prediction   = "cancerous" if prob_cancer >= threshold else "non_cancerous"

    return {
        "prediction":  prediction,
        "probability": round(prob_cancer, 4),
        "threshold":   threshold,
        "label":       "Potentially Cancerous" if prediction == "cancerous" else "Non-Cancerous",
    }
