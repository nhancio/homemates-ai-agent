from get_llm_response import get_llm_response

def classify_text(user_input):
    prompt = f"""
    ## Role:
     You are a text classification model.

    ## Task:
     Classify the following user input into **one of the categories**: "property_search", "general_query", "feedback", "greeting", 
     "UnrelatedKnowledge", "Nonsense".
     1. "property_search": The user is looking for information about properties, such as rent, location, or type.
     2. "general_query": The user is asking a general question that does not fit into the other categories.
     3. "feedback": The user is providing feedback or suggestions.
     4. "greeting": The user is greeting the chatbot or starting a conversation.
     5. "UnrelatedKnowledge": The user is asking about topics unrelated to property search or general queries.
     6. "Nonsense": The user input is nonsensical or does not convey a clear meaning.

     ## Output Format:
     Provide the classification as a single word, without any additional text or explanation.
     Example: "property_search"

     ##Examples:

    Input: "What is the rent for a 2BHK in Gachibowli?"
    Output: "property_search"

    Input: "Can you tell me about the weather today?"
    Output: "UnrelatedKnowledge"

    Input: "I would like to know the price of a 3BHK flat in Hyderabad."
    Output: "property_search"

    Input: "I think the chatbot could be improved with more features."
    Output: "feedback"

    Input: "Hello, can you help me with my property search?"
    Output: "greeting"

    Input: "What is the best way to invest in real estate?"
    Output: "general_query"

    Input: "Hello, how are you?"
    Output: "greeting"

    Input: "I have a suggestion for the chatbot."
    Output: "feedback"

    Input: "What is the capital of India?"
    Output: "UnrelatedKnowledge"

    Input: "What is the capital of France?"
    Output: "UnrelatedKnowledge"

    Input: "What is the meaning of life?"
    Output: "UnrelatedKnowledge"

    Input: "What is the weather like today?"
    Output: "UnrelatedKnowledge"

    Input: "Tell me a joke."
    Output: "UnrelatedKnowledge"

    Input: "I want to buy a house in Bangalore."
    Output: "property_search"

    Input: "Tell me about the history of the Roman Empire."
    Output: "UnrelatedKnowledge"

    Input: "Blah blah blah"
    Output: "Nonsense"

    Input: "{user_input}"

"""
    
    return prompt