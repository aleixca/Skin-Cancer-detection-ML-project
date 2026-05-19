"""
train_model.py — Run this ONCE to train and save the model to disk.
The Streamlit app loads the saved model; it does NOT retrain on each run.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from skimage.feature import hog

# ── Paths (replaces Google Colab drive mount) ─────────────────────────────────
train_path = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project\images\train"
test_path  = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project\images\test"
csv_path   = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project\HAM10000_metadata"
MODEL_PATH = r"C:\Users\bsama\OneDrive - La Salle\2n IA\ML\Project\model.pkl"

df = pd.read_csv(csv_path)

def image_id(file):
    return os.path.splitext(file)[0]

metadata_dict = df.set_index("image_id").to_dict(orient="index")

images = []
labels = []
metadata_rows = []

print("Loading training images at 128x128...")
for label in ["cancerous", "non_cancerous"]:
    folder = os.path.join(train_path, label)
    for file in os.listdir(folder):
        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # IMPROVEMENT 1: Double resolution (128x128)
        img = cv2.resize(img, (128,128))

        current_id = image_id(file)
        metadata = metadata_dict.get(current_id)
        if metadata is None:
            continue
        images.append(img)
        labels.append(label)
        metadata_rows.append(metadata)

# ============================
# Load test images
# ============================

images_test = []
labels_test = []
metadata_rows_test = []

print("Loading test images at 128x128...")
for label in ["cancerous", "non_cancerous"]:
    folder = os.path.join(test_path, label)
    for file in os.listdir(folder):
        img_path = os.path.join(folder, file)
        img = cv2.imread(img_path)
        if img is None:
            continue

        # IMPROVEMENT 1: Double resolution (128x128)
        img = cv2.resize(img, (128,128))

        current_id = image_id(file)
        metadata = metadata_dict.get(current_id)
        if metadata is None:
            continue
        images_test.append(img)
        labels_test.append(label)
        metadata_rows_test.append(metadata)

print("Training images:", len(images))
print("Test images:", len(images_test))

# Convert data to numerical values
metadata_train_df = pd.DataFrame(metadata_rows)
metadata_test_df = pd.DataFrame(metadata_rows_test)

selected_columns = ["age", "sex", "localization"]

metadata_train_df = metadata_train_df[selected_columns]
metadata_test_df = metadata_test_df[selected_columns]

metadata_train_df["age"] = metadata_train_df["age"].fillna(metadata_train_df["age"].median())
metadata_test_df["age"] = metadata_test_df["age"].fillna(metadata_train_df["age"].median())

metadata_train_df["sex"] = metadata_train_df["sex"].fillna("unknown")
metadata_test_df["sex"] = metadata_test_df["sex"].fillna("unknown")

metadata_train_df["localization"] = metadata_train_df["localization"].fillna("unknown")
metadata_test_df["localization"] = metadata_test_df["localization"].fillna("unknown")

metadata_all = pd.concat([metadata_train_df, metadata_test_df], axis=0)

metadata_all_encoded = pd.get_dummies(
    metadata_all,
    columns=["sex", "localization"]
)

X_metadata_train = metadata_all_encoded.iloc[:len(metadata_train_df)].values
X_metadata_test = metadata_all_encoded.iloc[len(metadata_train_df):].values

print(X_metadata_train.shape)
print(X_metadata_test.shape)

# ============================
# Baseline model (raw pixels)
# ============================

X_train_pixels = np.array(images).reshape(len(images), -1)
X_test_pixels = np.array(images_test).reshape(len(images_test), -1)

rf_pixels = RandomForestClassifier(n_estimators=100, random_state=42)
rf_pixels.fit(X_train_pixels, labels)

y_pred_pixels_rf = rf_pixels.predict(X_test_pixels)
accuracy_pixels_rf = accuracy_score(labels_test, y_pred_pixels_rf)

print("Accuracy with raw pixels (Random Forest):", accuracy_pixels_rf)

# ============================
# Extract HOG features
# ============================

def extract_color_hog(img_list):
    hog_features = []
    for img in img_list:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        fd = hog(
            img_rgb,
            orientations=9,
            pixels_per_cell=(16, 16), # IMPROVEMENT 2: Larger cells to detect asymmetries
            cells_per_block=(2, 2),
            visualize=False,
            channel_axis=-1
        )
        hog_features.append(fd)
    return np.array(hog_features)

print("Extracting HOG features... (This may take a few minutes)")
hog_train = extract_color_hog(images)
hog_test = extract_color_hog(images_test)
print("HOG features extracted successfully.")

# ============================
# Train Random Forest
# ============================

X_train_combined = np.concatenate([hog_train, X_metadata_train], axis=1)
X_test_combined = np.concatenate([hog_test, X_metadata_test], axis=1)

print("Training the new Optimized Random Forest...")
# IMPROVEMENT 3: Tuned hyperparameters
rf_hog_metadata = RandomForestClassifier(
    n_estimators=500,        # More trees (from 200 to 500)
    max_depth=15,            # Limit depth to prevent overfitting
    min_samples_split=5,     # Higher threshold for splitting nodes
    random_state=42,
    class_weight="balanced",
    n_jobs=-1                # Use all CPU cores to speed up training
)

rf_hog_metadata.fit(X_train_combined, labels)

y_pred_hog_metadata = rf_hog_metadata.predict(X_test_combined)
accuracy_hog_metadata = accuracy_score(labels_test, y_pred_hog_metadata)

print("Overall accuracy with optimized model:", accuracy_hog_metadata)

# ============================
# Final comparison
# ============================

print("\nComparison:")
print("Raw pixels accuracy:", accuracy_pixels_rf)
print("HOG features accuracy:", accuracy_hog_metadata)

from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns

print("HOG + metadata diagnostics")
print(classification_report(labels_test, y_pred_hog_metadata))
print("\n\n")
print("Raw Pixels diagnostics")
print(classification_report(labels_test, y_pred_pixels_rf))

from sklearn.metrics import roc_curve, precision_recall_curve

y_probs = rf_hog_metadata.predict_proba(X_test_combined)[:, 0]

fpr, tpr, thresholds_roc = roc_curve(labels_test, y_probs, pos_label='cancerous')
precision, recall, thresholds_pr = precision_recall_curve(labels_test, y_probs, pos_label='cancerous')

j_scores = tpr - fpr
best_idx = np.argmax(j_scores)
best_threshold = thresholds_roc[best_idx]

print(f"The optimal threshold according to Youden is: {best_threshold}")

target_recall = 0.80
idx_target = np.where(recall >= target_recall)[0][-1]
threshold_for_80_recall = thresholds_pr[idx_target]

print(f"To achieve an 80% recall, the threshold must be: {threshold_for_80_recall}")

threshold = 0.21448
y_pred_custom = ["cancerous" if p >= threshold else "non_cancerous" for p in y_probs]

print(f"Results with safety threshold ({threshold}):")
print(classification_report(labels_test, y_pred_custom))

# ============================
# Save model for the app
# ============================

# Verify class order: rf.classes_ must be ['cancerous', 'non_cancerous']
# so that predict_proba[:, 0] == P(cancerous)
assert list(rf_hog_metadata.classes_) == ["cancerous", "non_cancerous"], (
    f"Unexpected class order: {rf_hog_metadata.classes_}"
)

age_median = metadata_train_df["age"].median()

payload = {
    "model":      rf_hog_metadata,
    "columns":    metadata_all_encoded.columns.tolist(),
    "age_median": age_median,
    "threshold":  threshold,
}
joblib.dump(payload, MODEL_PATH)
print(f"\nModel saved → {MODEL_PATH}")
print("Run the Streamlit app: streamlit run app.py")
