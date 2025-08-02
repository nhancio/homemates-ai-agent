import json
import openai
from typing import Dict, Any
from dotenv import load_dotenv
from google.cloud import firestore

load_dotenv()

# Create Firestore client
db = firestore.Client.from_service_account_json('homemates-app-firebase-adminsdk-nbjyj-5242f136f5.json')

SYSTEM_PROMPT = """
You are an expert real estate assistant that converts search queries into Firestore filters.

Your tasks:
1. Analyze if the query has complete information for a property search
2. If incomplete, ask specific clarifying questions
3. If complete, convert to Firestore filter

Required fields for a complete search:
- Property type (flat, house, etc.) or BHK
- Location (area, city, etc.)

Rules for conversion:
1. Return JSON with "status" ("complete" or "incomplete")
2. If "incomplete", include "question" to ask for missing info
3. If "complete", include "filters" with Firestore query
4. Use proper field names: propertyType, address.locality, rentDetails.costs.rent
5. For numbers, ensure numeric values (not strings)

Example outputs:
User: "I want a flat"
{
  "status": "incomplete",
  "question": "What BHK configuration are you looking for, and in which area?"
}

User: "3BHK in Gachibowli under 20000"
{
  "status": "complete",
  "filters": {
    "propertyType": "3 BHK",
    "address.locality": "Gachibowli",
    "rentDetails.costs.rent": {"$lte": 20000}
  }
} 

User: "luxury apartments"
{
  "status": "incomplete",
  "question": "In which area are you looking for luxury apartments? What's your preferred BHK size and budget?"
}
"""

def analyze_query(query: str, conversation_history: list = []) -> Dict[str, Any]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        *conversation_history,
        {"role": "user", "content": query}
    ]
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
    )
    
    try:
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {"status": "error", "error": str(e), "raw_response": getattr(response.choices[0].message, 'content', response)}

def search_properties_firestore(filters: Dict[str, Any]) -> list:
    """Search Firestore with the provided filters"""
    collection_ref = db.collection('r')
    
    query = collection_ref
    for key, value in filters.items():
        if isinstance(value, dict):
            if "$lte" in value:
                query = query.where(key, "<=", value["$lte"])
            elif "$gte" in value:
                query = query.where(key, ">=", value["$gte"])
            elif "$eq" in value:
                query = query.where(key, "==", value["$eq"])
            # Add more conditions here if needed
        else:
            query = query.where(key, "==", value)

    return [doc.to_dict() for doc in query.get()]

def format_results(properties: list) -> str:
    if not properties:
        return "No properties found matching your criteria."

    result = []
    for prop in properties:
        addr = prop.get("address", {})
        rent = prop.get("rentDetails", {}).get("costs", {}).get("rent")

        prop_str = (
            f"Building Name : \"{addr.get('buildingName', 'N/A')}\"\n"
            f"Flat Type     : \"{prop.get('propertyType', 'N/A')}\"\n"
            f"Locality      : \"{addr.get('locality', 'N/A')}\"\n"
            f"Rent          : {rent}\n"
            "-----"
        )
        result.append(prop_str)

    return "\n".join(result)

def property_search_flow():
    conversation_history = []

    print("Welcome to Property Search! How can I help you?")
    
    while True:
        user_input = input("\nYour search query: ").strip()

        if user_input.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break

        analysis = analyze_query(user_input, conversation_history)
        conversation_history.append({"role": "user", "content": user_input})

        if analysis.get("status") == "error":
            print("\n[Error] Could not understand your request:\n")
            print(analysis.get("raw_response", "No response received."))
            continue

        if analysis.get("status") == "incomplete":
            print("\n" + analysis["question"])
            conversation_history.append({"role": "assistant", "content": analysis["question"]})
            continue

        if analysis.get("status") == "complete" and "filters" in analysis:
            filters = analysis["filters"]
            print("\nSearching properties...")
            results = search_properties_firestore(filters)
            print("\n" + format_results(results))

            refine = input("\nWould you like to refine your search? (yes/no): ").lower()
            if refine in ('y', 'yes'):
                print("Please provide additional filters or modifications")
            else:
                print("Thank you for using Property Search!")
                break
        else:
            print("\nSorry, I could not process your request. Please try again.")

if __name__ == "__main__":
    property_search_flow()
