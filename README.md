# 🌾 Farmflow AI

An AI-powered farming assistant built with Streamlit. Farmflow combines classical ML, deep learning,
live weather data and an LLM to give farmers simple, actionable guidance.

## Features

| Feature | How it works |
|---------|--------------|
| 🌱 **Crop recommendation** | XGBoost classifier on soil (N, P, K, pH) and climate (temperature, humidity, rainfall) returns the top 3 crops, plus rule-based fertilizer / pH advice and an LLM explanation. |
| 💧 **Irrigation guidance** | Pulls live weather and a 7-day forecast from WeatherAPI, picks an irrigation method per crop with transparent rules, and flags heavy-rain / dry days. |
| 🦠 **Plant disease detection** | MobileNetV2 (transfer learning) classifies leaf images across 15 pepper, potato and tomato classes, with an LLM-written explanation of symptoms, treatment and prevention. |

## Tech stack

PyTorch / torchvision · XGBoost / scikit-learn · pandas / NumPy · Streamlit · Pillow ·
Groq-hosted Llama (via the OpenAI-compatible API) · WeatherAPI

## Project structure

```
farmflow-ai/
├── app.py                  # Streamlit entry point
├── farmflow/               # Application package
│   ├── config.py           # Paths, env vars, constants
│   ├── models.py           # Model loading + inference
│   ├── llm.py              # LLM explanations (Groq)
│   ├── weather.py          # WeatherAPI client
│   ├── irrigation.py       # Irrigation rules (pure logic)
│   ├── fertilizer.py       # Soil / fertilizer rules (pure logic)
│   └── pages/              # One Streamlit page per feature
├── training/               # Reproducible training scripts
├── notebooks/              # Original exploratory notebooks
├── data/                   # Datasets (git-ignored, see data/README.md)
├── models/                 # Trained artifacts (git-ignored, see models/README.md)
├── .env.example                    # Template for your API keys
└── requirements.txt
```

## Getting started

```bash
git clone https://github.com/divyasrees16/farmflow-ai.git
cd farmflow-ai

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then add your API keys
```

### 1. Get the models

The app needs trained models in `models/`. Train the models using the notebooks available in /notebooks

```bash
python training/train_crop_model.py
python training/train_disease_model.py --epochs 5
```

### 2. Run

```bash
streamlit run app.py
```

### Configuration

| Variable | Required | Purpose |
|----------|----------|---------|
| `GROQ_API_KEY` | For AI explanations | Get one at [console.groq.com](https://console.groq.com/keys) |
| `GROQ_MODEL` | No | Override the default LLM (`openai/gpt-oss-20b`) |
| `WEATHER_API_KEY` | For irrigation page | Get one at [weatherapi.com](https://www.weatherapi.com/) |

If the LLM is unreachable, the app still shows predictions and falls back gracefully.


## Results

| Model | Metric | Value |
|-------|--------|-------|
| Crop recommendation (XGBoost) | Test accuracy | ~98.6% |
| Plant disease (MobileNetV2, 5 epochs, frozen backbone) | Validation accuracy | ~94.9% |
