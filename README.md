# DermaScan ML

A mobile-style web app that uses a Random Forest trained on the HAM10000 dataset to classify skin lesion images as **cancerous** or **non-cancerous**.

Built for the Machine Learning university course (V0 delivery).

---

## Project Structure

```
Project/
├── images/
│   ├── train/
│   │   ├── cancerous/
│   │   └── non_cancerous/
│   └── test/
│       ├── cancerous/
│       └── non_cancerous/
├── HAM10000_metadata       # CSV with image labels and patient info
├── dataset_images.zip      # Pre-sorted image archive (train/test split)
├── train_model.py          # Step 1 — trains and saves the ML model
├── app.py                  # Step 2 — Streamlit web app
├── sort_images.py          # Utility: sorts raw images into cancerous/non_cancerous
└── train_test_split.py     # Utility: splits images 70% train / 30% test
```

---

## Requirements

- Python 3.10+
- The following packages (install with the command below):

```bash
C:\Python314\python.exe -m pip install streamlit opencv-python scikit-learn scikit-image joblib numpy pandas matplotlib seaborn
```

---

## Setup & Running

### Step 1 — Extract the dataset

If the `images/` folder does not exist yet, extract `dataset_images.zip`:

```bash
C:\Python314\python.exe -c "import zipfile; zipfile.ZipFile('dataset_images.zip').extractall('.')"
```

This creates `images/train/cancerous`, `images/train/non_cancerous`, `images/test/cancerous`, and `images/test/non_cancerous`.

---

### Step 2 — Train the model (run once, ~5–10 min)

```bash
C:\Python314\python.exe train_model.py
```

This will:
1. Load all images at 128×128 resolution
2. Train a baseline Random Forest on raw pixels
3. Extract HOG features + encode patient metadata (age, sex, localization)
4. Train an optimized Random Forest (500 trees, balanced class weights)
5. Evaluate both models and print classification reports
6. Save the final model to **`model.pkl`**

You only need to run this once. The app loads `model.pkl` at startup.

---

### Step 3 — Launch the app

```bash
C:\Python314\python.exe -m streamlit run app.py
```

Then open your browser at **http://localhost:8501**

---

## How It Works

### ML Model
| | Details |
|---|---|
| **Dataset** | HAM10000 — 10,015 dermatoscopic images |
| **Split** | 70% train / 30% test (stratified by class) |
| **Classes** | `cancerous` (mel, bcc, akiec) · `non_cancerous` (nv, bkl, df, vasc) |
| **Features** | HOG (9 orientations, 16×16 cells) + patient age, sex, localization |
| **Classifier** | Random Forest — 500 trees, max_depth=15, balanced class weights |
| **Threshold** | 0.21448 (Youden-optimal, tuned for high cancer recall) |

### App Pages
- **Home** — recent scan history
- **Scan** — upload or photograph a lesion, enter patient info, run analysis
- **Result** — real model prediction with cancer probability bar
- **AI Chat** — assistant with photo tips and result explanations
- **Info** — project overview and version roadmap

---

## Dataset Label Mapping

| Code | Diagnosis | Class |
|---|---|---|
| `mel` | Melanoma | Cancerous |
| `bcc` | Basal Cell Carcinoma | Cancerous |
| `akiec` | Actinic Keratoses / Bowen's disease | Cancerous |
| `nv` | Melanocytic Nevi (moles) | Non-cancerous |
| `bkl` | Benign Keratosis-like Lesions | Non-cancerous |
| `df` | Dermatofibroma | Non-cancerous |
| `vasc` | Vascular Lesions | Non-cancerous |

---

## Disclaimer

This tool is a university prototype and does **not** constitute professional medical advice. Always consult a qualified dermatologist for any skin concerns.
