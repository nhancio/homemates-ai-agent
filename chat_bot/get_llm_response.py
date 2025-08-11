
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_llm_response(question):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  
        "X-Title": "HomeMates Chatbot",     
        "Content-Type": "application/json",
    }

    data = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": question}
    ]
}


    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")




