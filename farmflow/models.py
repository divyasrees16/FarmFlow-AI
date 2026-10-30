"""Loading and running the trained ML models.

Heavy dependencies (torch, joblib, xgboost) are imported lazily so the pure-logic
modules and their tests stay lightweight.
"""

from __future__ import annotations

import json
from functools import lru_cache

import numpy as np

from farmflow import config

# Fallback label list, used only if models/class_names.json is missing.
# torchvision's ImageFolder assigns indices in *sorted* folder-name order, so the
# fallback is sorted too. Re-running training/train_disease_model.py writes the
# authoritative class_names.json next to the weights.
_FALLBACK_DISEASE_CLASSES = sorted(
    [
        "Pepper__bell___Bacterial_spot",
        "Pepper__bell___healthy",
        "Potato___Early_blight",
        "Potato___healthy",
        "Potato___Late_blight",
        "Tomato___Target_Spot",
        "Tomato___Tomato_mosaic_virus",
        "Tomato___Tomato_YellowLeaf_Curl_Virus",
        "Tomato___Bacterial_spot",
        "Tomato___Early_blight",
        "Tomato___healthy",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Spider_mites_Two_spotted_spider_mite",
    ]
)


class ModelsNotFoundError(FileNotFoundError):
    """Raised when a trained model artifact is missing."""


def _require(path) -> None:
    if not path.exists():
        raise ModelsNotFoundError(
            f"Missing model file: {path.relative_to(config.ROOT_DIR)}. "
            "See models/README.md for how to train or obtain it."
        )


# --- Crop recommendation ---------------------------------------------------
@lru_cache(maxsize=1)
def load_crop_model():
    import joblib

    _require(config.CROP_MODEL_PATH)
    _require(config.LABEL_ENCODER_PATH)
    return joblib.load(config.CROP_MODEL_PATH), joblib.load(config.LABEL_ENCODER_PATH)


def recommend_crops(
    n: float,
    p: float,
    k: float,
    temperature: float,
    humidity: float,
    ph: float,
    rainfall: float,
    top_k: int = 3,
) -> list[str]:
    """Return the top-k most suitable crops, best first."""
    model, label_encoder = load_crop_model()
    features = np.array([[n, p, k, temperature, humidity, ph, rainfall]])
    probabilities = model.predict_proba(features)[0]
    top_idx = probabilities.argsort()[-top_k:][::-1]
    return list(label_encoder.inverse_transform(top_idx))


# --- Plant disease ---------------------------------------------------------
@lru_cache(maxsize=1)
def disease_class_names() -> list[str]:
    if config.DISEASE_CLASSES_PATH.exists():
        return json.loads(config.DISEASE_CLASSES_PATH.read_text(encoding="utf-8"))
    return list(_FALLBACK_DISEASE_CLASSES)


@lru_cache(maxsize=1)
def load_disease_model():
    import torch
    from torchvision.models import mobilenet_v2

    _require(config.DISEASE_MODEL_PATH)
    model = mobilenet_v2(weights=None)
    model.classifier = torch.nn.Sequential(
        torch.nn.Dropout(0.2),
        torch.nn.Linear(model.last_channel, len(disease_class_names())),
    )
    state = torch.load(config.DISEASE_MODEL_PATH, map_location="cpu")
    model.load_state_dict(state)
    model.eval()
    return model


def predict_disease(image) -> tuple[str, float]:
    """Classify a PIL leaf image. Returns (class_name, confidence in 0..1)."""
    import torch
    from torchvision import transforms

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    model = load_disease_model()
    with torch.no_grad():
        probs = torch.softmax(model(transform(image).unsqueeze(0)), dim=1)[0]
    confidence, index = torch.max(probs, dim=0)
    return disease_class_names()[index.item()], confidence.item()


def pretty_label(class_name: str) -> str:
    """'Tomato___Late_blight' -> 'Tomato - Late blight'."""
    plant, _, condition = class_name.replace("__bell", "").partition("___")
    return f"{plant} - {condition.replace('_', ' ')}" if condition else class_name
