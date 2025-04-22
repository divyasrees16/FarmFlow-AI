import requests
import os
from dotenv import load_dotenv

load_dotenv()
HUGGINGFACE_API = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API}"}
print(HUGGINGFACE_API)
def get_irrigation_explanation(city, crop, temperature, humidity, rainfall, method):
    prompt = f"""[INST] You are an agricultural assistant. A farmer in {city} is growing {crop}. Today's weather: {temperature}°C, humidity {humidity}%, rainfall {rainfall} mm. You suggested {method} as the irrigation method. Explain clearly in simple words (about 50 words):
1. Why this method suits the current conditions.
2. What happens if rainfall decreases tomorrow. [/INST]"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 150}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        full_response = response.json()[0]['generated_text']
        if "[/INST]" in full_response:
            return full_response.split("[/INST]")[-1].strip()
        else:
            return full_response.strip()
    else:
        return "Could not get explanation from LLM."

def get_crop_explanation(N, P, K, ph, temperature, humidity, rainfall, crops):
    crop1, crop2, crop3 = crops[:3]
    prompt = f"""[INST] You are an expert agricultural advisor. A farmer has provided the following soil and weather data:
- Nitrogen: {N}
- Phosphorous: {P}
- Potassium: {K}
- pH value: {ph}
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Rainfall: {rainfall} mm

Based on this, the recommended crops are: {crop1}, {crop2}, and {crop3}.
Give a combined single-paragraph explanation in simple words (no bullet points or repetition) describing why these three crops are suitable for the current soil and weather conditions. [/INST]"""

    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 300}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        return response.json()[0]['generated_text'].split("[/INST]")[-1].strip()
    else:
        return "Could not get explanation from LLM for crop recommendations."
