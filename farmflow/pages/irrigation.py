import streamlit as st

from farmflow import config, irrigation, llm, weather


def _show_forecast(city: str) -> None:
    st.markdown("### 🌦️ 7-Day Weather Forecast Advisory")
    try:
        forecast = weather.get_forecast(city)
    except weather.WeatherError:
        forecast = []
    if not forecast:
        st.warning("Could not fetch 7-day forecast data.")
        return

    for day in forecast:
        st.write(f"📅 {day.date}: 🌧️ {day.rainfall_mm} mm rain expected")
    for alert in irrigation.rain_alerts(forecast):
        st.warning(alert)
    st.info(irrigation.weekly_advisory(forecast)[1])


def render() -> None:
    st.title("💧 Irrigation Recommendation System")

    city = st.text_input("Enter your city or district name")
    crop = st.selectbox("Select your crop", config.SUPPORTED_CROPS)

    if not st.button("Get Irrigation Recommendation"):
        return
    if not city:
        st.warning("Please enter a location.")
        return

    try:
        current = weather.get_current_weather(city)
    except weather.WeatherError as exc:
        st.error(f"Could not fetch weather data. {exc}")
        return

    st.markdown(f"### 📍 Weather in `{city.title()}`")
    st.markdown(f"- 🌡️ Temperature: `{current.temperature_c} °C`")
    st.markdown(f"- 💧 Humidity: `{current.humidity}%`")
    st.markdown(f"- 🌧️ Rainfall: `{current.rainfall_mm} mm`")

    method = irrigation.recommend_method(crop, current.humidity, current.rainfall_mm)
    st.success(f"✅ Recommended Irrigation Method: **{method}**")

    explanation = llm.irrigation_explanation(
        city, crop, current.temperature_c, current.humidity, current.rainfall_mm, method
    )
    st.markdown("💬 Explanation from AI")
    st.write(explanation or "AI explanation is currently unavailable.")

    _show_forecast(city)
