import os
import streamlit as st
import requests
import time
import re
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

st.set_page_config(page_title="Chat with DeepSeek", page_icon="💬", layout="wide")

st.title("💬 Chat with DeepSeek (Ollama - GPU)")
st.caption("Running locally on **GPU** - `deepseek-r1:1.5b`")

if "messages" not in st.session_state:
    st.session_state.messages = []

def clean_response(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking... (Streaming Enabled)"):
            try:
                response = requests.post(
                    OLLAMA_URL,
                    json={"model": "deepseek-r1:1.5b", "prompt": user_input, "stream": True},
                    headers={"OLLAMA_GPU": "true"},
                    stream=True
                )

                ai_reply = ""
                response_container = st.empty()
                buffer = []  # Buffer to collect meaningful chunks

                for chunk in response.iter_lines():
                    if chunk:
                        try:
                            chunk_data = json.loads(chunk.decode("utf-8"))  # Parse JSON
                            text_chunk = chunk_data.get("response", "")
                            
                            if text_chunk.strip():  # Only buffer meaningful data
                                buffer.append(text_chunk)
                            
                            if len(buffer) >= 3:  # Render in batches instead of per token
                                ai_reply += "".join(buffer)
                                response_container.markdown(f"**{clean_response(ai_reply)}**")
                                buffer.clear()  # Clear the buffer
                        except json.JSONDecodeError:
                            pass  # Ignore invalid JSON chunks

                # Final render
                if buffer:
                    ai_reply += "".join(buffer)
                    response_container.markdown(f"**{clean_response(ai_reply)}**")

            except Exception as e:
                ai_reply = f"❌ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
