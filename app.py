import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="MobileXpert", page_icon="📱")
st.title("📱 MobileXpert")
st.caption("தமிழ் / Tanglish Real-Time Smartphone Advisor")

api_key = st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

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
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are MobileXpert, a smartphone advisor. Always search the web "
                "for current Indian e-commerce prices (Amazon/Flipkart) in INR (₹). "
                "Respond concisely in Tamil or Tanglish."
            ),
            tools=[{"google_search": {}}],
        ),
    )

    reply = response.text
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
  
