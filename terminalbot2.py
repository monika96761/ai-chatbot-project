import os
import time
import re  
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("error occured in api key....")
    exit()

client = Groq(api_key = api_key)

def clean_response(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    text = re.sub(r"(?:Alright|Okay|Hmm).*?Let me start by .*?", "", text, flags=re.IGNORECASE).strip()
    return text

message = []
print("\n💬 Welcome to AI Chatbot (Groq - LLaMA 70B)")
print("Type 'exit' to end the conversation.\n")

while(True):

    user_input = input("You: ")
    if user_input.lower == "exit":
        print("Byee")
        break
    message.append({"role": "user", "content": user_input})
    print("🤖 AI: ", end="", flush=True)
    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=message,
            max_tokens=500,
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"❌ Error: {e}"
    
    # Clean AI response
    ai_reply = clean_response(ai_reply)
    
    full_response = ""
    for char in ai_reply:
        full_response += char
        print(char, end="",flush=True)
        time.sleep(0.01)
    print("\n")
    message.append({"role": "assistant", "content": ai_reply})