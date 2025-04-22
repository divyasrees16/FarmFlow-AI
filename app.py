# src/app.py

import streamlit as st
from src.home import show_home
from src.crop_recommendation import show_crop_recommendation
from src.irrigation_recommendation import show_irrigation_system

st.set_page_config(page_title="Farmflow", layout="centered")

st.sidebar.title("🌱 Farmflow Navigation")
option = st.sidebar.radio("Go to", ["Home", "Crop Recommendation", "Irrigation System"])

if option == "Home":
    show_home()
elif option == "Crop Recommendation":
    show_crop_recommendation()
elif option == "Irrigation System":
    show_irrigation_system()
