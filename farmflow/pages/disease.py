import streamlit as st
from PIL import Image

from farmflow import llm, models


def render() -> None:
    st.title("🌿 Plant Disease Prediction")

    uploaded = st.file_uploader("Upload a leaf image", type=["jpg", "png", "jpeg"])
    if not uploaded:
        return

    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Uploaded Leaf", width="stretch")

    try:
        class_name, confidence = models.predict_disease(image)
    except models.ModelsNotFoundError as exc:
        st.error(str(exc))
        return

    st.success(f"✅ Predicted: **{models.pretty_label(class_name)}** ({confidence:.0%} confidence)")

    explanation = llm.disease_explanation(models.pretty_label(class_name))
    st.markdown("### 🩺 Disease Explanation & Recommendations:")
    st.write(explanation or llm.unavailable_message())