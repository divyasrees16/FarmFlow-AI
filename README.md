# 🌱 FarmFlow AI

An AI-powered farming assistant built with **Streamlit** and **scikit-learn**. Enter your soil and weather conditions and get crop suggestions, fertilizer advice and smart irrigation guidance, with plain-language explanations.


## ✨ Features

| Module | What it does |
|---|---|
| 🌾 **Crop Recommendation** | A trained ML model takes N, P, K, pH, temperature, humidity and rainfall and returns the **top 3 crops** with confidence scores |
| 🧪 **Fertilizer & soil advice** | Rule-based tips (urea / SSP / MOP / lime / sulfur) from your NPK and pH values |
| 💧 **Irrigation Recommendation** | Fetches **live weather** for your city, suggests an irrigation method for your crop, and shows a **7-day rain forecast** with alerts |
| 💬 **AI explanations** | An LLM explains each recommendation in simple words; a built-in summary is used if the AI service is unavailable |


## 📁 Project structure

```
FarmFlow-AI/
├── app.py                          # Streamlit entry point + navigation
├── src/
│   ├── home.py                     # Landing page
│   ├── crop_recommendation.py      # Crop model + fertilizer advice page
│   ├── irrigation_recommendation.py# Irrigation rules + page
│   ├── weather.py                  # WeatherAPI client
│   ├── llm_utils.py                # LLM explanations (with fallback)
│   └── config.py                   # Reads secrets from .env / Streamlit secrets
├── models/                         # Trained model + label encoder
├── data/                           # Dataset
├── notebooks/                      # Training / exploration notebooks
├── tests/                          # Unit tests
├── .env.example                    # Template for your API keys
└── requirements.txt
```

## 🚀 Getting started

```bash
git clone https://github.com/divyasrees16/FarmFlow-AI.git
cd FarmFlow-AI

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Add your API keys

```bash
cp .env.example .env               # Windows: copy .env.example .env
```

Then edit `.env`:

| Variable | Where to get it | Needed for |
|---|---|---|
| `WEATHER_API_KEY` | free key at [weatherapi.com](https://www.weatherapi.com/) | Irrigation page |
| `HF_TOKEN` | [Hugging Face settings → Tokens](https://huggingface.co/settings/tokens) | AI explanations (optional) |

The crop recommendation works without any keys. Without `HF_TOKEN`, a simple built-in explanation is shown.

### Run

```bash
streamlit run app.py
```

## 🧪 Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## ⚠️ Limitations

- Fertilizer and irrigation advice use general rules of thumb, not crop- or region-specific agronomy. Always confirm with a soil test or a local agriculture officer.
- Irrigation rules use *current* rainfall; a nutrient-and-weather model trained on a public dataset may not match your local conditions.
- Model files must be loaded with the same scikit-learn version they were trained with.

## 🗺️ Roadmap

- [ ] Show model accuracy and feature importance in the app
- [ ] Use the 7-day forecast inside the irrigation decision
- [ ] Add a training script (`train.py`) so the model can be reproduced
- [ ] Multi-language support (Malayalam / Hindi / Tamil)
- [ ] Deploy on Streamlit Community Cloud
