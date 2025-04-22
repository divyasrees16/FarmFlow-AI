# src/crop_recommendation.py

import streamlit as st
import numpy as np
import joblib
import os
from src.llm_utils import get_crop_explanation

def show_crop_recommendation():
    model = joblib.load(os.path.join("models", "crop_recommendation_model.pkl"))
    label_encoder = joblib.load(os.path.join("models", "label_encoder.pkl"))

    st.title("🌾 Crop Recommendation System")
    st.subheader("Get the top 3 suitable crops based on your field conditions")
    st.markdown("---")

    with st.form("crop_form"):
        col1, col2 = st.columns(2)
        with col1:
            N = st.number_input("Nitrogen (N)", min_value=0, max_value=140, value=90)
            P = st.number_input("Phosphorous (P)", min_value=0, max_value=140, value=42)
            K = st.number_input("Potassium (K)", min_value=0, max_value=140, value=43)
            ph = st.number_input("pH value", min_value=0.0, max_value=14.0, value=6.5)
        with col2:
            temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=80.0)
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=400.0, value=100.0)

        submitted = st.form_submit_button("Recommend Crops")

    if submitted:
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        probs = model.predict_proba(input_data)[0]
        top_3_idx = probs.argsort()[-3:][::-1]
        top_3_crops = label_encoder.inverse_transform(top_3_idx)

        st.success("✅ Based on your input, the top 3 recommended crops are:")
        for i, crop in enumerate(top_3_crops, 1):
            st.markdown(f"**{i}. {crop.capitalize()}**")

        explanation = get_crop_explanation(
            N, P, K, ph, temperature, humidity, rainfall, list(top_3_crops)
        )

        st.markdown("---")
        st.markdown("💬 Explanation")
        st.write(explanation)
        recommendations = []
        
        # Fertilizer based on NPK values
        if N < 50:
            recommendations.append("🟩 **Nitrogen is low** – Apply **Urea (46% N)** – *50 kg/acre*")
        if P < 40:
            recommendations.append("🟦 **Phosphorus is low** – Apply **Single Super Phosphate (SSP – 16% P₂O₅)** – *60 kg/acre*")
        if K < 40:
            recommendations.append("🟥 **Potassium is low** – Apply **Muriate of Potash (MOP – 60% K₂O)** – *40 kg/acre*")
        
        # Add more specific fertilizers based on soil type and crop needs
        if N < 30 and P < 30:
            recommendations.append("⚠️ **Soil is low in both Nitrogen and Phosphorus** – Consider applying a balanced fertilizer like **NPK 20:20:20** for better soil improvement.")
        
        if N >= 50 and P >= 40 and K >= 40:
            recommendations.append("✅ Your soil NPK values are sufficient. No major fertilizer needed.")

        # Additional fertilizers based on soil pH
        if ph < 5.5:
            recommendations.append("⚠️ **Soil pH is acidic** – Consider applying **lime** to raise pH to neutral.")
        elif ph > 7.5:
            recommendations.append("⚠️ **Soil pH is alkaline** – Apply **sulfur** to lower pH to neutral.")

        if not recommendations:
            st.success("✅ Your soil NPK values are sufficient. No major fertilizer needed.")
        else:
            for rec in recommendations:
                st.markdown(rec)
