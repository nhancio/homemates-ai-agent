from get_llm_response import get_llm_response
from classify import classify_text

test_inputs = [
    "Hi there!",
    "Can you show me a 2BHK in Mumbai under 20000?",
    "Tell me a joke.",
    "Blah blah blah blah",
    "Your service is really helpful, thank you!",
    "How to get a rent agreement?",
    "I want to buy a flat in Delhi",
    "Who won the IPL 2023?",
]

for input_text in test_inputs:
    prompt = classify_text(input_text)
    category = get_llm_response(prompt)
    print(f"Input: {input_text}")
    print(f"Predicted Category: {category.strip()}")
    print("------")
