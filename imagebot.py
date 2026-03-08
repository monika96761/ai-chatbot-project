import os
import streamlit as st
from huggingface_hub import InferenceClient

# Set Streamlit page config
st.set_page_config(page_title="Multimodal AI Chatbot", page_icon="🖼️", layout="wide")

# Load API Key from environment
api_key = os.getenv("HF_API_KEY")  # Store your HF key in env variables
if not api_key:
    st.error("🔑 Please set your HF_API_KEY environment variable!")
    st.stop()

# Initialize Hugging Face Inference API Client
client = InferenceClient(provider="fireworks-ai", api_key=api_key)

# Streamlit UI
st.title("🖼️ Chat with AI (Text + Image)")
st.caption("Powered by Llama-3.2-11B-Vision-Instruct")

# User Input
user_input = st.text_area("Enter your message:")
uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "png", "jpeg"])

if st.button("Generate Response"):
    if user_input or uploaded_image:
        # Convert image to URL if uploaded
        image_url = None
        if uploaded_image:
            from PIL import Image
            import base64
            import io

            # Convert image to base64 URL (since API doesn't support direct upload)
            img = Image.open(uploaded_image)
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode()

            image_url = f"data:image/jpeg;base64,{img_b64}"

        # Prepare messages payload
        messages = [{"role": "user", "content": [{"type": "text", "text": user_input}]}]
        if image_url:
            messages[0]["content"].append({"type": "image_url", "image_url": {"url": image_url}})

        # Call the Hugging Face Inference API
        with st.spinner("Generating response..."):
            try:
                completion = client.chat.completions.create(
                    model="meta-llama/Llama-3.2-11B-Vision-Instruct",
                    messages=messages,
                    max_tokens=500,
                )
                ai_reply = completion.choices[0].message.content
            except Exception as e:
                ai_reply = f"❌ Error: {e}"

        # Display AI Response
        st.subheader("AI Response:")
        st.write(ai_reply)
