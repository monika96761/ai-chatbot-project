import os
import time
import re
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Load API Key from environment
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("🔑 Error: Please set your GROQ_API_KEY environment variable!")
    exit()

# Initialize Groq API client
client = Groq(api_key=api_key)

# Function to clean up AI response (remove <think> tags and unnecessary text)
def clean_response(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"(?:Alright|Okay|Hmm).*?Let me start by .*?", "", text, flags=re.IGNORECASE).strip()
    return text

# Chat session history
messages = []

print("\n💬 Welcome to AI Chatbot (Groq - LLaMA 70B)")
print("Type 'exit' to end the conversation.\n")

while True:
    # Get user input
    user_input = input("🧑 You: ")
    
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    # Add user message to history
    messages.append({
        "role": "user",
        "content": user_input
    })

    print("🤖 AI: ", end="", flush=True)

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages,
            max_tokens=500
        )

        ai_reply = response.choices[0].message.content

    except Exception as e:
        ai_reply = f"❌ Error: {e}"

    # Clean the AI response
    ai_reply = clean_response(ai_reply)

    # Typing effect
    for char in ai_reply:
        print(char, end="", flush=True)
        time.sleep(0.01)

    print("\n")

    # Save AI response to history
    messages.append({
        "role": "assistant",
        "content": ai_reply
    })