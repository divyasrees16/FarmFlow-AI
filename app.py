"""Farmflow AI - Streamlit entry point.

Run with:  streamlit run app.py
"""

import os
import sys

# Streamlit's file watcher trips over torch.classes; keep it away from torch internals.
os.environ.setdefault("STREAMLIT_WATCH_DIRECTORIES", "")


class _SafeModule:
    def __getattr__(self, name):
        raise AttributeError(f"Module attribute {name} is not accessible")


sys.modules.setdefault("torch.classes", _SafeModule())

import streamlit as st  # noqa: E402

from farmflow.pages import crop, disease, home, irrigation  # noqa: E402

PAGES = {
    "Home": home.render,
    "Crop Recommendation": crop.render,
    "Irrigation System": irrigation.render,
    "Plant Disease Prediction": disease.render,
}

st.set_page_config(page_title="Farmflow", layout="centered")
st.sidebar.title("🌱 Farmflow Navigation")
choice = st.sidebar.radio("Go to", list(PAGES))
PAGES[choice]()
