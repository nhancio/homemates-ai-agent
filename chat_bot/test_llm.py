from get_llm_response import get_llm_response

def test_openrouter():
    question = "What is the capital of India?"
    answer = get_llm_response(question)
    print("Answer:", answer)

if __name__ == "__main__":
    test_openrouter()




