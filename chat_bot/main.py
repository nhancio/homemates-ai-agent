from classify import classify_text
from greeting_response import generate_greeting_response
from property_search_response import generate_property_search_response as property_search
from unrelated_info import handle_user_input as unrelated_info
from store_feedback import store_feedback

def handle_user_input(user_input):
    category = classify_text(user_input)
    print(f"[Intent Detected]: {category}")

    if category == "greeting":
        return generate_greeting_response(user_input)
    if category == "property_search":
        return property_search(user_input)
    if category == "UnrelatedKnowledge":
        return unrelated_info(user_input)
    if category == "feedback":
        return store_feedback(user_input)
    if category == "Nonsense":
        return "I'm here to assist with property-related queries. How can I help you with that?"
    else:
        return f"Intent '{category}' detected. (Handler not implemented yet.)"
