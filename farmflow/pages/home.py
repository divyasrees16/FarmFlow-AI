import base64
import random

import streamlit as st

from farmflow import config

QUOTES = [
    "🌱 *Farming is the foundation of civilization.*",
    "🌾 *The future of farming is smart.*",
    "🚜 *To plant a seed is to believe in tomorrow.*",
    "🌤️ *Technology meets tradition in modern agriculture.*",
    "💧 *Water wisely, grow greatly.*",
]


@st.cache_data
def _encoded_background() -> str | None:
    path = config.BACKGROUND_IMAGE_PATH
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()


def _apply_theme() -> None:
    encoded = _encoded_background()
    background = (
        f"""
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        """
        if encoded
        else ""
    )
    st.markdown(
        f"""
        <style>
        .stApp {{ {background} }}
        [data-testid="stSidebar"] > div:first-child {{
            background-color: #2C562C;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render() -> None:
    _apply_theme()

    st.markdown(
        """
        <h1 style='text-align: center; color: #033503; font-size: 48px;'>🌿 Welcome to Farmflow AI 🌿</h1>
        <p style='text-align: center; font-size: 20px; color: #4CAF50;'>Your AI-powered farming assistant for smart agriculture!</p>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        f"<div style='text-align:center; font-size: 22px; color:#033503;'><em>{random.choice(QUOTES)}</em></div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color:#C1FBC1; padding: 25px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top: 30px;">
            <h3 style="color: #2E7D32; text-align: center;">🔍 What can I do for you?</h3>
            <ul style="font-size: 18px; color: #333; list-style-type: none; padding-left: 0;">
                <li style="margin-bottom: 10px;">🌱 <strong>Smart Crop Recommendation</strong> – Describe your farm and get the best crop match.</li>
                <li style="margin-bottom: 10px;">💧 <strong>Irrigation Suggestions</strong> – Get smart watering advice for your crops based on weather and crop type.</li>
                <li style="margin-bottom: 10px;">🌿 <strong>Plant Disease Prediction</strong> – Upload a leaf image and detect diseases with AI-powered explanation and guidance.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #033503;'>Use the sidebar to get started!</p>",
        unsafe_allow_html=True,
    )
