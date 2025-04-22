import streamlit as st
import random

def add_bg_image():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-photo/green-tea-bud-leaves-green-tea-plantations-morning_335224-955.jpg?t=st=1744393797~exp=1744397397~hmac=9cf4eab0b82665aadd3b48a342df35f5916aaa5cad4c05bc5e3347530b59aee9&w=1380");
             background-size: cover;
             background-repeat: no-repeat;
             background-attachment: fixed;
         }}

         /* Sidebar styling */
         [data-testid="stSidebar"] > div:first-child {{
             background-color: #2C562C;
             color: white;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


def show_home():
    add_bg_image()

    st.markdown(
        """
        <h1 style='text-align: center; color: #033503; font-size: 48px;'>🌿 Welcome to Farmflow AI 🌿</h1>
        <p style='text-align: center; font-size: 20px; color: #4CAF50;'>Your AI-powered farming assistant for smart agriculture!</p>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")

 

    # Random quote
    quotes = [
        "🌱 *Farming is the foundation of civilization.*",
        "🌾 *The future of farming is smart.*",
        "🚜 *To plant a seed is to believe in tomorrow.*",
        "🌤️ *Technology meets tradition in modern agriculture.*",
        "💧 *Water wisely, grow greatly.*"
    ]
    st.markdown(
        f"<div style='text-align:center; font-size: 22px; color:#033503;'><em>{random.choice(quotes)}</em></div>", 
        unsafe_allow_html=True
    )

    st.markdown("---")

   # Feature highlights with inline CSS
    st.markdown("""
    <div style="background-color:#C1FBC1; padding: 25px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-top: 30px;">
        <h3 style="color: #2E7D32; text-align: center;">🔍 What can I do for you?</h3>
        <ul style="font-size: 18px; color: #333; list-style-type: none; padding-left: 0;">
            <li style="margin-bottom: 10px;">🌱 <strong>Smart Crop Recommendation</strong> – Describe your farm and get best crop match.</li>
            <li>💧 <strong>Irrigation Suggestions</strong> – Get smart watering advice for your crops.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)


    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #033503;'>Use the sidebar to get started!</p>", unsafe_allow_html=True)
