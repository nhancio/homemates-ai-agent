from get_llm_response import get_llm_response

def generate_greeting_response(user_input):
    prompt = f"""
You are a warm, kind, and helpful assistant.

The user has greeted you with:
"{user_input}"

Respond with a friendly, welcoming message that feels human. Be short, warm, and natural.

Examples:
User: "Hi"
Assistant: "Hey there! How can I help you today?"

User: "Good morning!"
Assistant: "Good morning! Hope your day is off to a great start. How can I assist you today?"

User: "Hello, can you help me?"
Assistant: "Hello! Absolutely, I'm here to help. What do you need assistance with?"

User: "Hey, what's up?"
Assistant: "Hey! Not much, just here to help you out. What can I do for you?"

User: "Hi, I have a question."
Assistant: "Hi! I'm all ears. What question do you have?"


User: "{user_input}"
Assistant:
"""
    return get_llm_response(prompt).strip()
