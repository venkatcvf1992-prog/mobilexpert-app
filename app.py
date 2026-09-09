import streamlit as st
from google import genai

st.set_page_config(page_title="MobileXpert", page_icon="📱")
st.title("📱 MobileXpert")
st.caption("தமிழ் / Tanglish Real-Time Smartphone Advisor")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("எந்த போன் பத்தி தெரிஞ்சுக்கணும்?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "system_instruction": (
                "You are MobileXpert, a smartphone advisor. Help users with smartphone specs, "
                "recommendations, and estimated Indian pricing in INR (₹). "
                "Respond concisely and helpfully in Tamil or Tanglish."
            ),
        },
    )

    reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
    
