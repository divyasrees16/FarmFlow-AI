import streamlit as st

from farmflow import fertilizer, llm, models


def render() -> None:
    st.title("🌾 Crop Recommendation System")
    st.subheader("Get the top 3 suitable crops based on your field conditions")
    st.markdown("---")

    with st.form("crop_form"):
        col1, col2 = st.columns(2)
        with col1:
            n = st.number_input("Nitrogen (N)", min_value=0, max_value=140, value=90)
            p = st.number_input("Phosphorous (P)", min_value=0, max_value=140, value=42)
            k = st.number_input("Potassium (K)", min_value=0, max_value=140, value=43)
            ph = st.number_input("pH value", min_value=0.0, max_value=14.0, value=6.5)
        with col2:
            temperature = st.number_input("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
            humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=80.0)
            rainfall = st.number_input("Rainfall (mm)", min_value=0.0, max_value=400.0, value=100.0)
        submitted = st.form_submit_button("Recommend Crops")

    if not submitted:
        return

    try:
        top_crops = models.recommend_crops(n, p, k, temperature, humidity, ph, rainfall)
    except models.ModelsNotFoundError as exc:
        st.error(str(exc))
        return

    st.success("✅ Based on your input, the top 3 recommended crops are:")
    for rank, crop in enumerate(top_crops, 1):
        st.markdown(f"**{rank}. {crop.capitalize()}**")

    st.markdown("---")
    st.markdown("💬 Explanation")
    explanation = llm.crop_explanation(n, p, k, ph, temperature, humidity, rainfall, top_crops)
    st.write(explanation or llm.unavailable_message())

    for line in fertilizer.soil_recommendations(n, p, k, ph):
        st.markdown(line)