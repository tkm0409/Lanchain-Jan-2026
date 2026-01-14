import streamlit as st
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="LangChain Streamlit Demo", page_icon="🦜")

st.title("🦜🔗 LangChain Enterprise Chat")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("⚙️ Configuration")
    provider = st.selectbox("LLM Provider", ["OpenAI", "Anthropic", "Google"])
    model_name = st.text_input("Model Name", value="gpt-3.5-turbo")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    
    st.divider()
    if st.button("Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# --- BACKEND INIT ---
# Initialize Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mock Model for Demo Purposes (in real app, switch based on provider)
llm = ChatOpenAI(model=model_name, temperature=temperature)

# --- CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT HANDLING ---
if prompt := st.chat_input("What is up?"):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Assistant Response (Streaming)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate interaction with LangChain
        # In prod: for chunk in llm.stream(history): ...
        
        # Using raw invoke for simple demo, but simulating stream UI
        raw_response = llm.invoke(prompt).content
        
        for chunk in raw_response.split():
            full_response += chunk + " "
            time.sleep(0.05) # Typing effect
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
