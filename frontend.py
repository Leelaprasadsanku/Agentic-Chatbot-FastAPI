import streamlit as st

st.set_page_config(page_title="LangGraph Agent AI", page_icon=":robot_face:", layout="centered")
st.title("AI Agent Chatbot")
st.write("Create and interact with an AI agent using LangGraph.")


system_prompt = st.text_area("Define your Agent AI:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "llama3-8b-8192", "deepseek-r1-distill-llama-70b"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Model Provider", ["Groq", "OpenAI"])
if provider == "Groq":
    model_name = st.selectbox("Select Model Name", MODEL_NAMES_GROQ)
elif provider == "OpenAI":
    model_name = st.selectbox("Select Model Name", MODEL_NAMES_OPENAI)

allow_WebSearch = st.checkbox("Allow Web Search", value=False)

user_query = st.text_area("Enter your query:", height=150, placeholder="Ask anything ..")
if st.button("Ask Agent"):
    if not user_query:
        st.warning("Please enter a message.")
    else:
        with st.spinner("Generating response..."):
            # Call the backend API
            import requests
            url = "http://127.0.0.1:9999/chat"
            headers = {"Content-Type": "application/json"}
            payload = {
                "model_name": model_name,
                "model_provider": provider,
                "system_prompt": system_prompt,
                "messages": [user_query],
                "allow_search": allow_WebSearch
            }
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                response_data = response.json()
                st.success("Response received!")
                st.text_area("AI Response:", value=response_data["response"], height=200)
            else:
                st.error("Error: " + response.text)
            