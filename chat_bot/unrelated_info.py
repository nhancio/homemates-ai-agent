from get_llm_response import get_llm_response

def handle_user_input(user_input):
    prompt = f"""
You are a real estate assistant.  
If the user's question is about real estate, property prices, availability, or locations, then answer normally.  
If the question is unrelated to real estate (like general knowledge, math, politics, etc.), reply politely:  
"Sorry, I can only help with real estate-related queries."

User Question:
"{user_input}"
"""
    response = get_llm_response(prompt)
    return response
