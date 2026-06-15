import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read API key from .env
API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(
    page_title="AI Chatbot with Memory",
    page_icon="🤖"
)

st.title("🤖 AI Chatbot with Memory")

# Stop if API key is missing
if not API_KEY:
    st.error("API Key not found. Check your .env file.")
    st.stop()

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        }
    ]

# Display chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask something...")

if prompt:

    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": st.session_state.messages
            }
        )

        data = response.json()

        if "choices" in data:
            reply = data["choices"][0]["message"]["content"]
        else:
            reply = f"API Error: {data}"

    except Exception as e:
        reply = f"Error: {str(e)}"

    # Store assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)