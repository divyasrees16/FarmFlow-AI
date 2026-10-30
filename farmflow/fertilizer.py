"""Rule-based soil / fertilizer advice (pure functions, no I/O)."""

from __future__ import annotations


def soil_recommendations(n: float, p: float, k: float, ph: float) -> list[str]:
    """Return markdown-formatted soil advice for the given N, P, K values and pH."""
    advice: list[str] = []

    if n < 50:
        advice.append("🟩 **Nitrogen is low** – Apply **Urea (46% N)** – *50 kg/acre*")
    if p < 40:
        advice.append(
            "🟦 **Phosphorus is low** – Apply **Single Super Phosphate (SSP – 16% P₂O₅)** – *60 kg/acre*"
        )
    if k < 40:
        advice.append(
            "🟥 **Potassium is low** – Apply **Muriate of Potash (MOP – 60% K₂O)** – *40 kg/acre*"
        )

    if n < 30 and p < 30:
        advice.append(
            "⚠️ **Soil is low in both Nitrogen and Phosphorus** – Consider applying a balanced "
            "fertilizer like **NPK 20:20:20** for better soil improvement."
        )

    if n >= 50 and p >= 40 and k >= 40:
        advice.append("✅ Your soil NPK values are sufficient. No major fertilizer needed.")

    if ph < 5.5:
        advice.append("⚠️ **Soil pH is acidic** – Consider applying **lime** to raise pH to neutral.")
    elif ph > 7.5:
        advice.append("⚠️ **Soil pH is alkaline** – Apply **sulfur** to lower pH to neutral.")

    return advice
