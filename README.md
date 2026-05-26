# DermaScan ML

DermaScan ML is a full-stack university prototype for skin-lesion screening. It combines a FastAPI inference backend, a browser-based mobile UI, and a small retrieval chatbot that explains scan results, photo quality tips, and basic dermatology concepts.

The project is designed as a learning prototype, not a medical device. It should never be used as a substitute for professional dermatological diagnosis.

## What It Demonstrates

- Image classification pipeline using HOG features, patient metadata, and a Random Forest model
- FastAPI backend with lazy model loading to keep free-tier deployments responsive
- Static React frontend with upload/camera flow, result view, and chat interface
- Retrieval-augmented FAQ assistant using a local TF-IDF index
- Production-oriented deployment split between Render for the API and Vercel/static hosting for the frontend
- Practical debugging around model serialization, dependency versions, and cold-start memory limits

## Tech Stack

| Layer | Tools |
| --- | --- |
| Backend | FastAPI, Uvicorn, Pydantic |
| ML | scikit-learn, scikit-image, OpenCV, joblib, NumPy |
| Frontend | React 18 UMD, Babel standalone, HTML/CSS |
| Chat/RAG | TF-IDF retrieval over a curated local knowledge base |
| Deployment | Docker, Render, Vercel/static hosting |

## Repository Structure

```text
.
|-- api.py                 # FastAPI app, prediction endpoint, chat endpoint
|-- train_model.py         # Rebuilds the model.pkl bundle from a prepared dataset
|-- model.pkl              # Serialized Random Forest model bundle
|-- rag/
|   `-- knowledge_base.py  # Local documents used by the chatbot retriever
|-- frontend/
|   |-- index.html         # Static React app shell
|   |-- screens.jsx        # UI screens
|   |-- ios-frame.jsx      # Phone-style frame component
|   `-- design-canvas.jsx  # Design/prototype support
|-- Dockerfile.backend     # Backend container for Render
|-- render.yaml            # Render service config
|-- vercel.json            # Static frontend hosting config
|-- requirements.txt       # Runtime Python dependencies
|-- requirements-training.txt
`-- tests/
    `-- test_api.py        # Lightweight API smoke tests
```

## API

### `GET /health`

Returns a simple health check.

```json
{ "status": "ok" }
```

### `POST /predict`

Accepts a lesion image plus metadata and returns a binary prediction.

Form fields:

- `file`: uploaded JPG/PNG image
- `age`: patient age, default `45`
- `sex`: `male`, `female`, or `unknown`
- `localization`: body location, default `back`

Example response:

```json
{
  "prediction": "non_cancerous",
  "probability": 0.1372,
  "threshold": 0.21448,
  "label": "Non-Cancerous"
}
```

### `POST /chat`

Answers questions about scan quality, result interpretation, warning signs, and model limitations using a local retrieval index.

```json
{
  "message": "How do I take a better photo?"
}
```

## Run Locally

### 1. Create a Python environment

Use Python 3.11. The Dockerfile and CI both target 3.11, and the pinned ML dependencies are not guaranteed to install cleanly on newer Python versions such as 3.14.

```bash
python3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Linux/macOS, activate with:

```bash
source .venv/bin/activate
```

### 2. Start the backend

```bash
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

Check that it is alive:

```bash
curl http://127.0.0.1:8000/health
```

### 3. Open the frontend

Open `frontend/index.html` in a browser. When running locally, the frontend automatically calls:

```text
http://localhost:8000
```

## Testing

Install development dependencies and run the smoke tests:

```bash
python -m pip install -r requirements-dev.txt
pytest
```

The tests intentionally avoid loading `model.pkl`; they verify that the FastAPI app imports correctly and exposes the health/root endpoints. This keeps CI fast and catches broken imports or missing runtime dependencies.

## Training

The repository includes `train_model.py` so the serialized model can be rebuilt from the prepared HAM10000 dataset.

Expected local dataset layout:

```text
images/
|-- train/
|   |-- cancerous/
|   `-- non_cancerous/
`-- test/
    |-- cancerous/
    `-- non_cancerous/
HAM10000_metadata.csv
```

Install the training dependencies:

```bash
python -m pip install -r requirements-training.txt
```

Train with default paths:

```bash
python train_model.py
```

Or pass explicit paths:

```bash
python train_model.py --train-dir images/train --test-dir images/test --metadata HAM10000_metadata.csv --output model.pkl
```

The output bundle contains:

- `model`: trained Random Forest classifier
- `columns`: metadata feature columns used at inference time
- `age_median`: training median used to fill missing age values
- `threshold`: probability threshold for the final cancerous/non-cancerous decision

## Model Notes

- Dataset: HAM10000 dermatoscopic image dataset
- Classes: binary mapping of malignant-like labels to `cancerous` and benign labels to `non_cancerous`
- Features: HOG image descriptors plus patient age, sex, and lesion localization metadata
- Classifier: Random Forest
- Threshold: tuned for high recall so suspicious cases are more likely to be flagged

The raw image dataset is not included because it is large. The serialized model bundle is included so the API can run without retraining, while `train_model.py` documents how the bundle is produced.

## Deployment

The backend is configured for Render using `Dockerfile.backend` and `render.yaml`.

The API is currently expected at:

```text
https://skin-cancer-detection-ml-project.onrender.com
```

The frontend can be hosted as static files. In production, `frontend/index.html` points API calls to the Render backend.

## Limitations

- This is a university prototype and not a clinical diagnostic system.
- Smartphone images differ from dermatoscopic images used in the dataset.
- The model is sensitive to lighting, focus, and framing.
- Dataset bias can affect accuracy across skin tones and lesion types.
- A low threshold improves recall but increases false positives.

Always consult a dermatologist for any lesion that changes, bleeds, itches, grows quickly, or looks unusual.
