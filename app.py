import streamlit as st
import firestore_agent

st.set_page_config(page_title="Real Estate Property Search", layout="centered")
st.title("🏠 Real Estate Property Search AI Agent")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "filters" not in st.session_state:
    st.session_state.filters = {}
if "results" not in st.session_state:
    st.session_state.results = None
if "last_question" not in st.session_state:
    st.session_state.last_question = None

st.write("Enter your property search query below:")
user_input = st.text_input("Your search query", "")

if st.button("Search") and user_input.strip():
    analysis = firestore_agent.analyze_query(user_input, st.session_state.conversation_history)
    st.session_state.conversation_history.append({"role": "user", "content": user_input})

    if analysis.get("status") == "error":
        st.error("Sorry, there was an error understanding your request.")
        st.write(analysis.get("raw_response", "No response received."))
        st.stop()

    if analysis.get("status") == "incomplete":
        st.session_state.last_question = analysis["question"]
        st.session_state.results = None
    elif analysis.get("status") == "complete" and "filters" in analysis:
        st.session_state.filters = analysis["filters"]
        st.session_state.results = firestore_agent.search_properties_firestore(st.session_state.filters)
        st.session_state.last_question = None
    else:
        st.error("Sorry, I could not process your request. Please try again.")
        st.session_state.last_question = None
        st.session_state.results = None

if st.session_state.last_question:
    st.info(st.session_state.last_question)
    clarification = st.text_input("Clarify your requirements", "", key="clarify")
    if st.button("Submit Clarification") and clarification.strip():
        analysis = firestore_agent.analyze_query(clarification, st.session_state.conversation_history)
        st.session_state.conversation_history.append({"role": "user", "content": clarification})
        if analysis.get("status") == "incomplete":
            st.session_state.last_question = analysis["question"]
            st.session_state.results = None
        elif analysis.get("status") == "complete" and "filters" in analysis:
            st.session_state.filters = analysis["filters"]
            st.session_state.results = firestore_agent.search_properties_firestore(st.session_state.filters)
            st.session_state.last_question = None
        else:
            st.error("Sorry, I could not process your request. Please try again.")
            st.session_state.last_question = None
            st.session_state.results = None

if st.session_state.results is not None:
    st.subheader("Search Results")
    if st.session_state.results:
        for prop in st.session_state.results:
            st.markdown(f"**Building Name:** \"{prop.get('address', {}).get('buildingName', 'N/A')}\"\n")
            st.write(f"**Flat Type:** \"{prop.get('propertyType', 'N/A')}\"\n")
            st.write(f"**Locality:** \"{prop.get('address', {}).get('locality', 'N/A')}\"\n")
            st.write(f"**Rent:** \"{prop.get('rentDetails', {}).get('costs', {}).get('rent', 'N/A')}\"\n")
            st.write("---")
    else:
        st.warning("No properties found matching your criteria.")

