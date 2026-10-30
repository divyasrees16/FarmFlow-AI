"""Train the XGBoost crop-recommendation model.

Expects a CSV with columns: N, P, K, temperature, humidity, ph, rainfall, label
(the standard "Crop Recommendation" dataset layout).

Usage:
    python training/train_crop_model.py --data data/crop_recommendation.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier

ROOT = Path(__file__).resolve().parent.parent
# The app feeds features in exactly this order (see farmflow/models.py).
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "data" / "crop_recommendation.csv")
    parser.add_argument("--out", type=Path, default=ROOT / "models")
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    X, y = df[FEATURES], df["label"]

    encoder = LabelEncoder()
    y_enc = encoder.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

    model = XGBClassifier(n_estimators=200, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, pred))
    print(classification_report(y_test, pred, target_names=encoder.classes_))

    args.out.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.out / "crop_recommendation_model.pkl")
    joblib.dump(encoder, args.out / "label_encoder.pkl")
    print(f"Saved model + label encoder to {args.out}")


if __name__ == "__main__":
    main()
