"""Central configuration: paths, environment variables and constants."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# --- Paths -----------------------------------------------------------------
MODELS_DIR = ROOT_DIR / "models"
DATA_DIR = ROOT_DIR / "data"

CROP_MODEL_PATH = MODELS_DIR / "crop_recommendation_model.pkl"
LABEL_ENCODER_PATH = MODELS_DIR / "label_encoder.pkl"
DISEASE_MODEL_PATH = MODELS_DIR / "plant_disease_model.pth"
DISEASE_CLASSES_PATH = MODELS_DIR / "class_names.json"
BACKGROUND_IMAGE_PATH = DATA_DIR / "green-tea-bud-leaves-green-tea-plantations-morning.jpg"

# --- External services -----------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
WEATHER_API_BASE_URL = "https://api.weatherapi.com/v1"
HTTP_TIMEOUT_SECONDS = 10

# --- Domain constants ------------------------------------------------------
SUPPORTED_CROPS = ["Rice", "Wheat", "Sugarcane", "Maize", "Cotton", "Millets", "Groundnut"]
