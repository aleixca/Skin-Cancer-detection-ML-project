"""
Train the DermaScan Random Forest model.

This script rebuilds the `model.pkl` bundle consumed by `api.py`. It expects a
pre-split image dataset:

    images/
      train/
        cancerous/
        non_cancerous/
      test/
        cancerous/
        non_cancerous/

It also expects the HAM10000 metadata CSV with at least these columns:
`image_id`, `age`, `sex`, and `localization`.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_curve
from skimage.feature import hog


CLASSES = ("cancerous", "non_cancerous")
METADATA_COLUMNS = ["age", "sex", "localization"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the DermaScan ML model.")
    parser.add_argument(
        "--train-dir",
        type=Path,
        default=Path("images/train"),
        help="Directory containing cancerous/non_cancerous training folders.",
    )
    parser.add_argument(
        "--test-dir",
        type=Path,
        default=Path("images/test"),
        help="Directory containing cancerous/non_cancerous test folders.",
    )
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path("HAM10000_metadata.csv"),
        help="Path to the HAM10000 metadata CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("model.pkl"),
        help="Where to write the trained model bundle.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="Classification threshold. Defaults to the Youden-optimal threshold.",
    )
    return parser.parse_args()


def image_id_from_path(path: Path) -> str:
    return path.stem


def load_split(split_dir: Path, metadata_by_id: dict[str, dict]) -> tuple[list[np.ndarray], list[str], list[dict]]:
    images: list[np.ndarray] = []
    labels: list[str] = []
    metadata_rows: list[dict] = []

    for label in CLASSES:
        class_dir = split_dir / label
        if not class_dir.exists():
            raise FileNotFoundError(f"Missing class directory: {class_dir}")

        for image_path in sorted(class_dir.iterdir()):
            if not image_path.is_file():
                continue

            image = cv2.imread(str(image_path))
            if image is None:
                print(f"Skipping unreadable image: {image_path}")
                continue

            metadata = metadata_by_id.get(image_id_from_path(image_path))
            if metadata is None:
                print(f"Skipping image without metadata: {image_path.name}")
                continue

            images.append(cv2.resize(image, (128, 128)))
            labels.append(label)
            metadata_rows.append(metadata)

    return images, labels, metadata_rows


def encode_metadata(
    train_rows: list[dict],
    test_rows: list[dict],
) -> tuple[np.ndarray, np.ndarray, list[str], float]:
    train_df = pd.DataFrame(train_rows)[METADATA_COLUMNS].copy()
    test_df = pd.DataFrame(test_rows)[METADATA_COLUMNS].copy()

    age_median = float(train_df["age"].median())
    train_df["age"] = train_df["age"].fillna(age_median)
    test_df["age"] = test_df["age"].fillna(age_median)

    for column in ["sex", "localization"]:
        train_df[column] = train_df[column].fillna("unknown")
        test_df[column] = test_df[column].fillna("unknown")

    all_metadata = pd.concat([train_df, test_df], axis=0)
    all_encoded = pd.get_dummies(all_metadata, columns=["sex", "localization"])

    train_encoded = all_encoded.iloc[: len(train_df)].to_numpy()
    test_encoded = all_encoded.iloc[len(train_df) :].to_numpy()

    return train_encoded, test_encoded, all_encoded.columns.tolist(), age_median


def extract_hog_features(images: list[np.ndarray]) -> np.ndarray:
    features = []

    for image in images:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        features.append(
            hog(
                image_rgb,
                orientations=9,
                pixels_per_cell=(16, 16),
                cells_per_block=(2, 2),
                visualize=False,
                channel_axis=-1,
            )
        )

    return np.array(features)


def choose_youden_threshold(labels: list[str], cancer_probabilities: np.ndarray) -> float:
    fpr, tpr, thresholds = roc_curve(
        labels,
        cancer_probabilities,
        pos_label="cancerous",
    )
    best_index = int(np.argmax(tpr - fpr))
    return float(thresholds[best_index])


def main() -> None:
    args = parse_args()

    metadata_df = pd.read_csv(args.metadata)
    metadata_by_id = metadata_df.set_index("image_id").to_dict(orient="index")

    print("Loading training images...")
    train_images, train_labels, train_metadata = load_split(args.train_dir, metadata_by_id)

    print("Loading test images...")
    test_images, test_labels, test_metadata = load_split(args.test_dir, metadata_by_id)

    print(f"Training images: {len(train_images)}")
    print(f"Test images: {len(test_images)}")

    if not train_images or not test_images:
        raise ValueError("Both train and test splits must contain readable images.")

    metadata_train, metadata_test, columns, age_median = encode_metadata(
        train_metadata,
        test_metadata,
    )

    print("Extracting HOG features...")
    hog_train = extract_hog_features(train_images)
    hog_test = extract_hog_features(test_images)

    x_train = np.concatenate([hog_train, metadata_train], axis=1)
    x_test = np.concatenate([hog_test, metadata_test], axis=1)

    print("Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=15,
        min_samples_split=5,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    model.fit(x_train, train_labels)

    predictions = model.predict(x_test)
    print(f"Accuracy: {accuracy_score(test_labels, predictions):.4f}")
    print(classification_report(test_labels, predictions))

    if list(model.classes_) != ["cancerous", "non_cancerous"]:
        raise ValueError(f"Unexpected class order: {model.classes_}")

    cancer_probabilities = model.predict_proba(x_test)[:, 0]
    threshold = (
        float(args.threshold)
        if args.threshold is not None
        else choose_youden_threshold(test_labels, cancer_probabilities)
    )
    threshold_predictions = [
        "cancerous" if probability >= threshold else "non_cancerous"
        for probability in cancer_probabilities
    ]

    print(f"Selected threshold: {threshold:.5f}")
    print("Classification report with selected threshold:")
    print(classification_report(test_labels, threshold_predictions))

    bundle = {
        "model": model,
        "columns": columns,
        "age_median": age_median,
        "threshold": threshold,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, args.output)
    print(f"Model saved to {args.output}")


if __name__ == "__main__":
    main()
