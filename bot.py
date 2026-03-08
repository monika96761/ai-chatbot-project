import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import time
import re

# Load environment variables
load_dotenv()

# Set Streamlit page config
st.set_page_config(page_title="AI Chatbot", page_icon="💬", layout="wide")

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("🔑 Please set your GROQ_API_KEY in the .env file")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Title
st.title("💬 AI Chatbot")
st.caption("Powered by Groq API")

# Model options
model_options = {
    "LLaMA 3.3 70B (Best)": "llama-3.3-70b-versatile",
    "LLaMA 3.1 8B (Fast)": "llama-3.1-8b-instant",
    "DeepSeek R1 Distill": "deepseek-r1-distill-llama-70b"
}

# Model selector
selected_model = st.selectbox(
    "🧠 Select AI Model",
    list(model_options.keys())
)

# Store selected model
model_name = model_options[selected_model]

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to clean AI response
def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Type your message here...")

if prompt:

    # Show user message
    st.chat_message("user").markdown(prompt)

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=st.session_state.messages,
                    max_tokens=500
                )

                ai_reply = response.choices[0].message.content

            except Exception as e:
                ai_reply = f"❌ Error: {e}"

        # Clean response
        ai_reply = clean_response(ai_reply)

        # Typing effect
        message_placeholder = st.empty()
        full_response = ""

        for char in ai_reply:
            full_response += char
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.01)

        message_placeholder.markdown(full_response)

    # Save AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )