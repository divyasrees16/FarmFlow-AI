import streamlit as st
import requests
from src.llm_utils import get_irrigation_explanation

WEATHER_API_KEY = "7c7882b873d742d1bba101243251104"

def get_weather_data(city):
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
    response = requests.get(url)
    data = response.json()
    temperature = data["current"]["temp_c"]
    humidity = data["current"]["humidity"]
    rainfall = data["current"].get("precip_mm", 0)
    return temperature, humidity, rainfall

def get_7_day_forecast(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={city}&days=7"
    response = requests.get(url)
    if response.status_code == 200:
        forecast_data = response.json()["forecast"]["forecastday"]
        return [(day["date"], day["day"].get("totalprecip_mm", 0)) for day in forecast_data]
    return []

def analyze_forecast_rain(rain_data):
    alerts = []
    for date, rain in rain_data:
        if rain > 50:
            alerts.append(f"📅 {date}: ⚠️ Heavy rain expected – avoid irrigation.")
        elif rain < 1:
            alerts.append(f"📅 {date}: 💧 Low rain – consider increasing irrigation.")
    return alerts

def show_irrigation_system():
    st.title("💧 Irrigation Recommendation System")

    city = st.text_input("Enter your city or district name")
    crop = st.selectbox("Select your crop", ["Rice", "Wheat", "Sugarcane", "Maize", "Cotton", "Millets", "Groundnut"])

    if st.button("Get Irrigation Recommendation"):
        if not city:
            st.warning("Please enter a location.")
            return

        try:
            temperature, humidity, rainfall = get_weather_data(city)

            st.markdown(f"### 📍 Weather in `{city.title()}`")
            st.markdown(f"- 🌡️ Temperature: `{temperature} °C`")
            st.markdown(f"- 💧 Humidity: `{humidity}%`")
            st.markdown(f"- 🌧️ Rainfall: `{rainfall} mm`")

            crop_lower = crop.lower()
            if crop_lower == "rice":
                method = "Flood Irrigation" if rainfall > 100 else "Drip Irrigation" if rainfall > 50 and humidity > 60 else "Sprinkler Irrigation"
            elif crop_lower == "wheat":
                method = "Sprinkler Irrigation" if rainfall < 30 else "Drip Irrigation" if rainfall <= 70 else "Flood Irrigation"
            elif crop_lower == "sugarcane":
                method = "Furrow Irrigation" if rainfall > 120 else "Drip Irrigation" if rainfall > 60 else "Sprinkler Irrigation"
            elif crop_lower == "maize":
                method = "Flood Irrigation" if humidity > 65 and rainfall > 80 else "Drip Irrigation" if humidity > 50 else "Sprinkler Irrigation"
            elif crop_lower == "cotton":
                method = "Drip Irrigation" if humidity < 40 or rainfall < 30 else "Sprinkler Irrigation"
            elif crop_lower == "millets":
                method = "Drip Irrigation" if rainfall < 40 else "Sprinkler Irrigation"
            elif crop_lower == "groundnut":
                method = "Drip Irrigation" if rainfall < 50 and humidity < 50 else "Sprinkler Irrigation"
            else:
                method = "Sprinkler Irrigation"

            # LLM-based explanation
            explanation = get_irrigation_explanation(city, crop, temperature, humidity, rainfall, method)

            st.success(f"✅ Recommended Irrigation Method: **{method}**")
            st.markdown("💬 Explanation from AI")
            st.write(explanation)

            # 🌦️ Weather Forecast Advisory Section
            st.markdown("### 🌦️ 7-Day Weather Forecast Advisory")
            forecast = get_7_day_forecast(city)
            if forecast:
                avg_rain = sum(r for _, r in forecast) / len(forecast)
                for date, rain in forecast:
                    st.write(f"📅 {date}: 🌧️ {rain} mm rain expected")
                
                alerts = analyze_forecast_rain(forecast)
                for alert in alerts:
                    st.warning(alert)

                if avg_rain < 5:
                    st.info("📢 Low rainfall expected this week. Increase irrigation frequency or use drip system.")
                elif avg_rain > 40:
                    st.info("📢 Heavy rainfall expected. Avoid overwatering. Ensure field drainage.")
                else:
                    st.info("✅ Weather conditions are moderate. Continue usual irrigation practice.")
            else:
                st.warning("Could not fetch 7-day forecast data.")

        except Exception as e:
            st.error(f"Could not fetch weather data. Error: {e}")
